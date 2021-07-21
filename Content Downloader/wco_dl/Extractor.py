#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from cfscrape import create_scraper
from requests import session
from tqdm import tqdm


class Extractor(object):

    def __init__(self, logger, download_url, backup_url, hidden_url, output, header, user_agent, show_info, settings, quiet):

        self.sess = session()
        self.sess = create_scraper(self.sess)
        self.show_name = show_info[0]
        self.season = re.search(r'(\d+)', show_info[1]).group(1).zfill(settings.get_setting('seasonPadding'))
        try:
            if (show_info[2] == ""): self.episode = '{0}'.format(re.search(r'(\d+)', show_info[3]).group(1).zfill(settings.get_setting('episodePadding')))
            else: self.episode = '{0}'.format(re.search(r'(\d+)', show_info[2]).group(1).zfill(settings.get_setting('episodePadding')))
        except:
            self.episode = "xx"
        self.desc = show_info[3]
        self.header = header
        self.output = output
        self.backup_url = backup_url
        self.hidden_url = hidden_url
        self.user_agent = user_agent
        self.logger = logger
        self.quiet = quiet
        if settings.get_setting('includeShowDesc'): self.file_name = settings.get_setting('saveFormat').format(show=self.show_name, season=self.season, episode=self.episode, desc=self.desc)
        else: self.file_name = settings.get_setting('saveFormat').format(show=self.show_name, season=self.season, episode=self.episode)
        self.file_path = self.output + os.sep + "{0}.mp4".format(self.file_name)

        if (os.path.exists(self.file_path) and settings.get_setting('checkIfFileIsAlreadyDownloaded') and self.check_if_downloaded(download_url)):

            pass

        elif (settings.get_setting('allowToResumeDownloads') and os.path.exists(self.file_path) and os.path.getsize(self.file_path) != 0): 

            already_downloaded_bytes = os.path.getsize(self.file_path)

            while True:

                self.start_download(download_url, already_downloaded_bytes)

                if (os.path.getsize(self.file_path) == already_downloaded_bytes):

                    self.start_download(backup_url, already_downloaded_bytes)

                return 

        else:

            while True:

                if not self.start_download(download_url):

                    if not self.start_download(self.backup_url):

                        f_path = os.path.dirname(os.path.realpath(__file__)) + os.sep

                        with open(f_path + "failed.txt", "a+") as failed: 

                            failed.write("{0},{1},{2}".format(self.file_name, self.output, show_info[4]))

                        break

                    else:

                        break

                else:

                    break

    def check_if_downloaded(self, url):

        try:

            if (os.path.exists(self.file_path) and int(os.path.getsize(self.file_path)) == int(self.sess.get(url, headers=self.header).headers["content-length"])):

                return True

            else:

                return False

        except:

            return True

        return False

    def start_download(self, url, resume_bytes=None):

        while True:

            if (resume_bytes != None and os.path.exists(self.file_path) and os.path.getsize(self.file_path) != 0):

                host_url = self.sess.get(url).url
                resume_header = {'Host': host_url.split("//")[-1].split("/")[0].split('?')[0],
                                 'User-Agent': self.user_agent,
                                 'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                                 'Accept-Language': 'en-US,en;q=0.5',                                                                                                                      
                                 'Connection': 'keep-alive',
                                 'Referer': self.hidden_url.replace('https://wcostream.com', 'https://www.wcostream.com'),
                                 'Range': 'bytes={0}-'.format(resume_bytes),}
                dlr = self.sess.get(host_url, stream=True, headers=resume_header)

                try:

                    with open(self.file_path, 'ab') as handle:

                        if (self.quiet == 'False'):

                            with tqdm(unit_scale=1024, miniters=1, desc='Downloading', initial=int(resume_bytes), total=int(dlr.headers['content-length'], 0)) as pbar:

                                for data in dlr.iter_content(chunk_size=1024):

                                    handle.write(data)
                                    pbar.update(len(data))

                        else:

                            for data in dlr.iter_content(chunk_size=1024):

                                handle.write(data)

                except Exception as e:

                    if (self.logger == 'True'):

                        print('Error: {}'.format(e), end='\n\n')

                    return

                return

            else:

                dlr = self.sess.get(url, stream=True, headers=self.header)

                try: 

                    with open(self.file_path, "wb") as handle:

                        if (self.quiet == 'False'):

                            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading", total=int(dlr.headers['content-length'], 0)) as pbar:

                                for data in dlr.iter_content(chunk_size=1024):

                                    handle.write(data)
                                    pbar.update(len(data))

                        else:

                            for data in dlr.iter_content(chunk_size=1024):

                                handle.write(data)

                except Exception as e:

                    if (self.logger == 'True'):

                        print('Error: {}'.format(e), end='\n\n')

                    return False

            if os.path.getsize(self.file_path) == 0:

                return False

            else:

                return True
