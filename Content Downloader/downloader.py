import time
import shutil
import signal
import subprocess
import os, re, sys
import requests
import random
import warnings
import psutil
import urllib.request
from qbittorrent import Client
import unicodedata as ucd
import youtube_dl as ytdl
import img2pdf as converter
from selenium import webdriver
sys.stderr = open(os.devnull, "w")
from fuzzywuzzy import fuzz as fw
sys.stderr = sys.__stderr__
from youtube_search import YoutubeSearch
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from youtubesearchpython import PlaylistsSearch as playlist_search
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import DEVNULL, STDOUT
import concurrent.futures
from wco_dl.Settings import Settings


class Downloader(object):
    
    options = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e"]
    extensions = (".mp4", ".mkv", ".wav", ".avi", ".flv", ".mov", ".wmv", ".webm")
    standard = r"[^a-zA-Z0-9\s:]"
    restrictions = ["?", "/", "\\", ":", "*", ">", "<", "|", '"']
    ordinal = lambda self, index: "%d%s" % (index, "tsnrhtdd"[(index//10%10!=1)*(index%10<4)*index%10::4])
    numbers = lambda self, start, end: [str(index) for index in range(start, end + 1)]
    video_duration = lambda self, filename: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).stdout)

    def __init__(self, browser_path, qbit_admin, qbit_password):

        self.seasons, self.episodes = [f"s0{index}" for index in range(1, 9 + 1)], []
        for index in range(10, 100 + 1): self.seasons.append(f"s{index}")
        for item in self.seasons: self.episodes += [item + f"e0{index}" for index in range(1, 9 + 1)]
        for item in self.seasons: self.episodes += [item + f"e{index}" for index in range(10, 100 + 1)]
        self.qbit_admin = qbit_admin
        self.qbit_password = qbit_password
        self.directory = browser_path
        self.reset_browser()


    def reset_browser(self, status = True):

        subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE", stdout = DEVNULL, stderr = STDOUT)
        settings = webdriver.ChromeOptions()
        settings.headless = status
        settings.add_experimental_option("excludeSwitches", ["enable-logging"])

        try: 

            self.driver = webdriver.Chrome(executable_path = self.directory, options = settings)

        except:

            settings.add_argument("--remote-debugging-port=9222")
            self.driver = webdriver.Chrome(executable_path = self.directory, options = settings)

        self.driver.implicitly_wait(5)
        self.kill_chrome()


    def selector(self, indicator = 0):

        if (indicator == None):

            os.system("cls")
            category = input("\nWhat type of content are you downloading: \n\nA: audio \nB: video \nC: comic book \nD: torrent \nE: animated show \n\n")

            while category.lower().rstrip().lstrip() not in self.options:

                os.system("cls")
                category = input("\nInvalid entry, please select an available file type: \n\nA: audio \nB: video \nC: comic book \nD: torrent \nE: animated show \n\n")

            if (category.lower().rstrip().lstrip() == "a"): self.category = "audio"
            elif (category.lower().rstrip().lstrip() == "b"): self.category = "video"
            elif (category.lower().rstrip().lstrip() == "c"): self.category = "comic book"
            elif (category.lower().rstrip().lstrip() == "d"): self.category = "torrent"
            elif (category.lower().rstrip().lstrip() == "e"): self.category = "animation"

        elif ((self.category == "video") | (self.category == "audio")):

            os.system("cls")
            field = input("\nAre you downloading a playlist or a single file: \n\nA: single file \nB: playlist \n\n")

            while field.lower().rstrip().lstrip() not in self.options[0:4]:

                os.system("cls")
                field = input("\nInvalid entry, please select an available option: \n\nA: single file \nB: playlist \n\n")

            if (field.lower().rstrip().lstrip() == "a"): field = "single"
            elif (field.lower().rstrip().lstrip() == "b"): field = "playlist"
            return field

        elif (self.category == "comic book"):

            os.system("cls")
            field = input("\nAre you downloading an entire volume from a specific comic book title or a single issue: \n\nA: single issue \nB: one volume \n\n")

            while field.lower().rstrip().lstrip() not in self.options[0:4]:

                os.system("cls")
                field = input("\nInvalid entry, please select an available option: \n\nA: single issue \nB: one volume \n\n")
 
            if (field.lower().rstrip().lstrip() == "a"): field = "single"
            elif (field.lower().rstrip().lstrip() == "b"): field = "volume"
            return field

        elif (self.category == "torrent"):

            os.system("cls")
            field = input("\nAre you downloading a particular season, multiple seasons or one episode: \n\nA: single episode \nB: one season \nC: multiple seasons \n\n")

            while field.lower().rstrip().lstrip() not in self.options[0:6]:

                os.system("cls")
                field = input("\nInvalid entry, please select an available option: \n\nA: single episode \nB: one season \nC: multiple seasons \n\n")

            if (field.lower().rstrip().lstrip() == "a"): field = "episode"
            elif (field.lower().rstrip().lstrip() == "b"): field = "season"
            elif (field.lower().rstrip().lstrip() == "c"): field = "series"
            return field


    def search(self):

        self.selector(None)
        
        if (self.category == "audio"):

            tag, link, field, label = self.extractor()

            for index in range(len(link)):

                if (field[index] == "single"):

                    data = ytdl.YoutubeDL().extract_info(url = link[index], download = False)
                    file_name = f"{data['title']}"
                    for character in self.restrictions: file_name = file_name.replace(character, "-")
                    header = f"{file_name}.%(ext)s"
                    configuration = {"format": "bestaudio/best",
                                     "keepvideo": False,
                                     "outtmpl": header,
                                     "postprocessors": [{"key": "FFmpegExtractAudio",
                                                         "preferredcodec": "mp3",
                                                         "preferredquality": "192"}]}

                    try: 

                        with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])

                    except: 

                        pass

                    try: self.directory_manager(tag[index], file_name + ".mp3")
                    except: self.directory_manager(tag[index], self.slugify(file_name) + ".mp3")

                elif (field[index] == "playlist"):

                    folder = self.directory_manager(tag[index], title = label[index], field = field[index])
                    data = ytdl.YoutubeDL().extract_info(url = link[index], download = True)
                    configuration = {"format": "22", "keepvideo": True}

                    try: 

                        with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])

                    except: 

                        pass

                    for mp4 in os.listdir(folder):

                        if mp4.endswith(self.extensions):

                            mp3 = " ".join(mp4.split(".")[0:-1]) + ".mp3"
                            cmd = ["ffmpeg", "-n", "-i"] + [mp4] + ["-vn"] + [mp3]
                            subprocess.run(cmd, shell = True)

                    self.delete_copy(folder, field = field[index])

        elif (self.category == "video"):

            tag, link, field, label = self.extractor()

            for index in range(len(link)):

                folder = self.directory_manager(tag[index], title = label[index])
                data = ytdl.YoutubeDL().extract_info(url = link[index], download = True)
                configuration = {"format": "22", "keepvideo": True}

                try: 

                    with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])

                except: 

                    pass

                self.delete_copy(folder)

        elif (self.category == "comic book"):

            formats = (".txt", ".jpg")
            issues, paths, headers, fields = self.extractor()
            folder = os.listdir(os.getcwd())

            for index in range(len(issues)):

                path = paths[index]
                titles = headers[index]
                links = issues[index]
                folder = os.listdir(path)
                os.chdir(path), os.system("cls")
                for file in folder: os.remove(file) if file.endswith(formats) else None

                if (fields[index] == "single"):

                    print(f"\nCurrently downloading {titles} ({index + 1} / {len(issues)}) \n\n")
                    self.persist_search(links)
                    for character in self.restrictions: titles = titles.replace(character, "-")
                    self.process_file(titles)
                    folder = os.listdir(path)
                    for file in folder: os.remove(file) if file.endswith(formats) else None

                else:

                    for address in range(len(issues[index])):

                        if f"{titles[address]}.pdf" not in folder:

                            if (len(issues) > 1): print(f"\nCurrently downloading {titles[address]} [{address + 1} / {len(issues[index])} ({index + 1} / {len(issues)})] \n\n")
                            else: print(f"\nCurrently downloading {titles[address]} ({address + 1} / {len(issues[index])}) \n\n")
                            header = titles[address]
                            link = links[address]
                            self.persist_search(link)
                            for character in self.restrictions: header = header.replace(character, "-")
                            self.process_file(header)
                            folder = os.listdir(path)
                            for file in folder: os.remove(file) if file.endswith(formats) else None 

        elif (self.category == "torrent"):

            url = "http://samcloud.tplinkdns.com:50000"
            types = [["series", "show", "shows", "tv show", "tv shows"], ["movies", "films", "cinema", "movie", "film"]]
            getSites = "/getSites"
            getTorrents = "/getTorrents"
            websites = requests.get(url + getSites).json()["sites"]
            title, tag, field, initial, final = self.extractor()
            data, sites, done, skip = [], [], False, False
            if (type(initial) != list): count, counter = int(initial), int(initial)
            complete, torrent = False, ""
            qbt = Client("http://127.0.0.1:8080/")
            qbt.login(self.qbit_admin, self.qbit_password)

            if (tag.lower().rstrip().lstrip() in types[0]):

                for index in range(len(title)):

                    data, sites, done, skip = [], [], False, False
                    complete, count, counter, torrent = False, int(initial[index]), int(initial[index]), ""
                    folder = self.directory_manager(tag, title = title[index])

                    if (field[index] == "episode"):

                        pin = title[index].lower().split()[-1]
                        search_link = "?search_key=" + title[index] + "&site="
                        results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                        pages = [result[1] for result in results]
                        for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                        for result in results: data += result[0]
                        titles = [result["name"] for result in data]
                        seeders = [result["seeds"] for result in data]
                        leechers = [result["leeches"] for result in data]
                        sizes = [result["size"] for result in data]
                        links = [result["link"] for result in data]
                        torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites, pin)
                        if (torrent == "empty"): pass
                        else: qbt.download_from_link(torrent, savepath = folder)

                    elif (field[index] == "season"):

                        while not done:

                            torrent = ""
                            pin = title[index].lower().split()[-1]
                            search_link = "?search_key=" + title[index] + " complete" + "&site="
                            if (torrent != "empty"): results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                            data, sites = [], []
                            complete, skip = False, False
                            if (len(results) == 0): torrent, results = self.alternative(qbt, title[index], folder, websites, counter, 0, pin)

                            if ((len(results) == 0) | (count != 1) | (int(final[index]) != 0)):

                                while not complete:

                                    if ((int(final[index]) != 0) & (count == int(final[index]) + 1)): complete, done = True, True
                                    if ((int(final[index]) != 0) & (count == int(final[index]) + 1)): break
                                    prefix = "0" if (count < 10) else ""
                                    search_link = "?search_key=" + title[index] + "E" + prefix + str(count) + "&site="
                                    results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                                    files = os.listdir(folder)
                                    number = title[index][-3:] + "E" + prefix + str(count)
                                    count += 1

                                    for file in files:

                                        if number.lower() in file.lower():

                                            skip = True
                                            break

                                    if (skip != True):

                                        if (len(results) > 0):

                                            complete, skip = False, False
                                            pages = [result[1] for result in results]
                                            for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                                            for result in results: data += result[0]
                                            titles = [result["name"] for result in data]
                                            seeders = [result["seeds"] for result in data]
                                            leechers = [result["leeches"] for result in data]
                                            sizes = [result["size"] for result in data]
                                            links = [result["link"] for result in data]
                                            torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites, number)
                                            if (torrent == "empty"): complete, done = True, True
                                            else: qbt.download_from_link(torrent, savepath = folder)
                                            data, sites = [], []

                                        elif ((len(results) == 0) & (count == 2)):

                                            complete = True
                                            skip = False
                                            done = True
                                            break

                                        else:

                                            skip = False
                                            done = True
                                            complete = True
                                            break

                                    else:

                                        skip = False
                                        complete = False

                            elif ((torrent == "empty") | (torrent == "")):

                                done = True
                                pages = [result[1] for result in results]
                                for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                                for result in results: data += result[0]
                                titles = [result["name"] for result in data]
                                seeders = [result["seeds"] for result in data]
                                leechers = [result["leeches"] for result in data]
                                sizes = [result["size"] for result in data]
                                links = [result["link"] for result in data]
                                torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites, pin)
                                if (torrent == "empty"): torrent, results = self.alternative(qbt, title[index], folder, websites, counter, 0, pin)
                                if (torrent == "empty"): done, results = False, []
                                else: qbt.download_from_link(torrent, savepath = folder)

                    elif (field[index] == "series"):

                        while not done:

                            torrent = ""
                            if ((int(final[index]) != 0) & (counter == int(final[index]) + 1)): break
                            season = "0" if (counter < 10) else ""
                            search_link = "?search_key=" + title[index] + " S" + season + str(counter) + " complete" + "&site="
                            if (torrent != "empty"): results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                            ID = f"Season {counter}"
                            subfolder = folder + f"\\{ID}"
                            if (os.path.isdir(subfolder) == False): os.makedirs(subfolder)
                            complete, skip, count = False, False, 1
                            pin = "s" + season + str(counter)
                            data, sites = [], []
                            if (len(results) == 0): torrent, results = self.alternative(qbt, title[index], subfolder, websites, counter, 1, pin)
                            if ((torrent != "empty") & (torrent != "")): counter += 1

                            if (len(results) == 0):

                                while not complete:

                                    episode = "0" if (count < 10) else ""
                                    search_link = "?search_key=" + title[index] + " S" + season + str(counter) + "E" + episode + str(count) + "&site="
                                    results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                                    files = os.listdir(subfolder)
                                    number = "S" + season + str(counter) + "E" + episode + str(count)

                                    for file in files:

                                        if number.lower() in file.lower().rstrip().lstrip():

                                            skip = True
                                            break

                                    if (skip == False):

                                        if (len(results) > 0):

                                            pages = [result[1] for result in results]
                                            for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                                            for result in results: data += result[0]
                                            titles = [result["name"] for result in data]
                                            seeders = [result["seeds"] for result in data]
                                            leechers = [result["leeches"] for result in data]
                                            sizes = [result["size"] for result in data]
                                            links = [result["link"] for result in data]
                                            torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites, number)
                                            if (torrent == "empty"): complete, done, torrent = True, False, ""
                                            else: qbt.download_from_link(torrent, savepath = folder)
                                            data, sites = [], []
                                            skip = False
                                            count += 1

                                        elif ((len(results) == 0) & (count == 1)):

                                            complete = True 
                                            done = True
                                            os.rmdir(subfolder)
                                            break

                                        else:

                                            complete = True 
                                            skip = False
                                            done = False
                                            counter += 1
                                            count = 1
                                            torrent = ""
                                            break

                                    else:

                                        skip = False
                                        done = False
                                        complete = False
                                        torrent = ""
                                        count += 1

                            elif ((torrent == "empty") | (torrent == "")):

                                pages = [result[1] for result in results]
                                for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                                for result in results: data += result[0]
                                titles = [result["name"] for result in data]
                                seeders = [result["seeds"] for result in data]
                                leechers = [result["leeches"] for result in data]
                                sizes = [result["size"] for result in data]
                                links = [result["link"] for result in data]
                                torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites, pin)
                                if (torrent == "empty"): torrent, results = self.alternative(qbt, title[index], subfolder, websites, counter, 1, pin)
                                if (torrent == "empty"): done, results = False, []
                                else: qbt.download_from_link(torrent, savepath = subfolder)
                                if ((torrent != "empty") & (torrent != "")): counter += 1

            else:

                for index in range(len(title)):

                    data, sites, torrent = [], [], ""
                    folder = self.directory_manager(tag, title = title[index])
                    search_link = "?search_key=" + title[index] + "&site="
                    results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                    pages = [result[1] for result in results]
                    for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
                    for result in results: data += result[0]
                    titles = [result["name"] for result in data]
                    seeders = [result["seeds"] for result in data]
                    leechers = [result["leeches"] for result in data]
                    sizes = [result["size"] for result in data]
                    links = [result["link"] for result in data]
                    torrent = self.torrent_selector(title[index], links, titles, seeders, leechers, sizes, sites)
                    if (torrent == "empty"): pass
                    else: qbt.download_from_link(torrent, savepath = folder)

            subprocess.Popen(["C:\\Program Files\\qBittorrent\\qbittorrent.exe"], shell = True)

        elif (self.category == "animation"):

            title, link, chapter, tag = self.extractor()
            root = os.getcwd()
            os.chdir("wco_dl"), print()

            for index in range(len(title)):

                tests, folders = [], []
                for item in range(len(title[index])): tests.append(title[index][item].replace("&",  "and") + " anime") if (len(title[index][item].split()) == 1) else tests.append(title[index][item].replace("&",  "and"))
                for item in range(len(tests)): folders.append(self.directory_manager(tag.replace(" ", "_"), title = tests[item].replace(" ", "_"))) 

                for element in range(len(link[index])):

                    self.file_manager(folders[element], 0)

                    for item in range(len(link[index][element])):

                        os.system("cls")
                        if ((len(title) == 1) & (len(link[index][element]) == 1)): print(f"\nCurrently downloading '{chapter[index][element][item]}' from {title[index][0]} \n\n")
                        elif (len(title) == 1): print(f"\nCurrently downloading '{chapter[index][element][item]}' from {title[index][0]} ({item + 1} / {len(link[index][element])}) \n\n")
                        else: print(f"\nCurrently downloading '{chapter[index][element][item]}' from {title[index][0]} [{item + 1} / {len(link[index][element])} ({index + 1} / {len(title)})] \n\n")
                        settings = Settings()
                        header, season, episode, description, url = self.information(link[index][element][item])
                        season = re.search(r"(\d+)", season).group(1).zfill(settings.get_setting("seasonPadding"))

                        try:

                            if (episode == ""): episode = "{0}".format(re.search(r"(\d+)", description).group(1).zfill(settings.get_setting("episodePadding")))
                            else: episode = "{0}".format(re.search(r"(\d+)", episode).group(1).zfill(settings.get_setting("episodePadding")))

                        except:

                            episode = "xx"

                        if settings.get_setting("includeShowDesc"): file_name = settings.get_setting("saveFormat").format(show = header, season = season, episode = episode, desc = description) + ".mp4"
                        else: file_name = settings.get_setting("saveFormat").format(show = header, season = season, episode = episode) + ".mp4"
                        if int(season) < 10: append = "0"
                        else: append = ""
                        check = "s" + append + str(int(season))
                        ticket = self.check_page(folders[element])
                        if ((check in self.seasons) & (ticket in ["A", "B"])): folder = folders[element] + "\\" + folders[element].split("\\")[-1].replace(" ", "_") + f"_{check.replace(append, '').title()}"
                        else: folder = folders[element]
                        if (os.path.isdir(folder) == False): os.makedirs(folder)
                        subfolders = ["\\".join(folder.split("\\")[0:-1]) + "\\" + folder.split("\\")[-1].replace("_", " ").replace(" anime", ""), folder.replace("_", " ").replace(" anime", "")]
                        test = chapter[index][element][item] + ".mp4"

                        if ((os.path.isdir(subfolders[0]) == True) | (os.path.isdir(subfolders[1]) == True)):

                            for subfolder in subfolders:

                                if (os.path.isdir(subfolder) == True):

                                    if ((file_name not in os.listdir(subfolder)) & (test not in os.listdir(subfolder)) & 
                                        (file_name not in os.listdir(folder)) & (test not in os.listdir(folder))):

                                        self.wco_download(link[index][element][item], folder, file_name, test)
                                        break

                        else:

                            if ((file_name not in os.listdir(folder)) & (test not in os.listdir(folder))):

                                self.wco_download(link[index][element][item], folder, file_name, test)

                    self.file_manager(folders[element], 1)
                    parent = folders[element].replace("_", " ").replace(" anime", "")
                    self.delete_copy(folders[element], parent)
                    self.replace_folder(folders[element], parent)

            os.chdir(root)


    def file_manager(self, folder, indicator):

        for reference, path, items in os.walk(folder):

            if (indicator == 0):
    
                for item in items:

                    if item.endswith(self.extensions): 

                        file = reference + "\\" + item
                        self.inspect_file(file)

                for directory in path:
                    
                    for item in os.listdir(reference + "\\" + directory):

                        if item.endswith(self.extensions): 

                            file = reference + "\\" + directory + "\\" + item
                            self.inspect_file(file)

            elif (indicator == 1):

                for item in items:

                    if item.endswith(self.extensions): 

                        file = reference + "\\" + item
                        self.inspect_file(file)

                for directory in path:
                    
                    child = directory.replace("_", " ").replace(" anime", "")
                    self.replace_folder(reference + "\\" + directory, reference + "\\" + child)


    def inspect_file(self, file):

        try:

            duration = self.video_duration(file)
            bits = os.path.getsize(file)
            megabytes, minutes = bits / 1e6, duration / 60
            ratio = megabytes / minutes
            if (ratio < 2.5): os.remove(file)

        except:

            try: os.remove(file)
            except: pass


    def wco_download(self, link, folder, title, tag):

        process = subprocess.Popen(f"python crawler.py -i {link} -o {folder}", shell = True)
        self.monitor_download(link, folder, process, title)
        os.rename(folder + "\\" + title, folder + "\\" + tag)


    def alternative(self, server, title, folder, websites, indicator, pin = None):

        data, sites, results = [], [], []
        url = "http://samcloud.tplinkdns.com:50000"
        getTorrents = "/getTorrents"
        pin = pin.replace("s", "season ").replace(pin[1:], str(int(pin[1:])))
        if (indicator == 0): test = " ".join(title.lower().split()[0:-1]) + " " + title.lower().split()[-1].replace(title.lower().split()[-1].split("s")[-1], "").replace("s", "season ") + str(int(title.lower().split()[-1].split("s")[-1]))
        elif (indicator == 1): test = title.lower().rstrip().lstrip() + " season " + str(counter)
        search_link = "?search_key=" + test + " complete" + "&site="
        results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]

        if (len(results) > 0):

            pages = [result[1] for result in results]
            for result in range(len(results)): sites += [pages[result] for address in range(len(results[result][0]))]
            for result in results: data += result[0]
            titles = [result["name"] for result in data]
            seeders = [result["seeds"] for result in data]
            leechers = [result["leeches"] for result in data]
            sizes = [result["size"] for result in data]
            links = [result["link"] for result in data]
            torrent = self.torrent_selector(test, links, titles, seeders, leechers, sizes, sites, pin)
            if (torrent != "empty"): server.download_from_link(torrent, savepath = folder)
            else: torrent, results = "empty", []

        else:

            torrent = "empty"
            results = []

        return torrent, results


    def check_page(self, folder):

        header = folder.lower().split("\\")[-1].replace("_", " ").replace("-", " ").replace("anime", "").replace("!", "").rstrip().lstrip()
        if (len(header) > 40): header = header.replace("(", "") if ")" not in header else " ".join(header.split()[0:-1])
        labels, links = self.anime_search(header)
        if (len(links) == 0): labels, links = self.anime_search(header.replace("and", "&"))
        response = self.persist_search(links[0])
        anchors = self.driver.find_elements_by_css_selector("#catlist-listview li a")
        episodes = [item.text.lower() for item in anchors]
        episodes = list(reversed(episodes))
        count, number = 0, 0
        ticket, flag = "", None
        counter, variable = 0, 0
        season_count, episode_count = 0, 0
        block, unique = 0, 0
        number, value = -1, 0

        for title in episodes:

            variable = None
            text = title.lower().split()
            if "season" in title.lower(): address = text.index("season")
            elif "volume" in title.lower(): address = text.index("volume")
            elif "chapter" in title.lower(): address = text.index("chapter")
            elif "book" in title.lower(): address = text.index("book")
            else: address = None

            if ((address != None) & (address != len(text) - 1)):

                value = text[address + 1]
                if "-" in value: value = value.split("-")[0]
                if value.isdigit(): value = int(value)
                else: value = 0

            else: 

                value = 0

            for index in range(len(text)):

                if text[index].isdigit():

                    variable = text[index]
                    if (("episode" in text[index - 1].lower()) & (index > 0)): break

                elif "-" in text[index]:

                    if text[index].split("-")[0].isdigit():

                        variable = text[index].split("-")[0]
                        if (("episode" in text[index - 1].lower()) & (index > 0)): break

            if ("season" in title.lower()): season_count += 1
            elif ("book" in title.lower()): season_count += 1
            elif ("chapter" in title.lower()): season_count += 1
            elif ("volume" in title.lower()): season_count += 1
            if ("episode" in title.lower()): episode_count += 1
            elif (variable != None): episode_count += 1
            if ((value != number) & (value != 0)): unique += 1
            if (value != number): block += 1
            number = value

        if ((season_count != episode_count) & (unique != block) & (unique != 0)): ticket = "A"
        elif ((season_count == episode_count) & (unique == block) & (unique != 1)): ticket = "B"
        elif ((season_count == episode_count) & (unique == block) & (unique == 1)): ticket = "C"
        elif ((season_count != episode_count) & (unique != block) & (unique == 0)): ticket = "D"
        return ticket


    def information(self, url):

        url = re.sub("https://www.wcostream.com/", "", url)

        try:

            if "season" in url: 

                header, season, episode, description = re.findall(r"([a-zA-Z0-9].+)\s(season\s\d+\s?)(episode\s\d+\s)?(.+)", url.replace("-", " "))[0]

            else: 

                header, episode, description = re.findall(r"([a-zA-Z0-9].+)\s(episode\s\d+\s?)(.+)", url.replace("-", " "))[0]
                season = "season 1"

        except:

            header, season, episode, description = url, "Season 1", "Episode 0", ""

        return header.title().strip(), season.title().strip(), episode.title().strip(), description.title().strip(), url


    def show_results(self, label, link, channel, length):

        os.system("cls")
        choose = input("\nDo you want to select a video from the available search results?: \n\nA: yes \nB: no\n\n")

        while choose not in self.options[0:4]:

            os.system("cls")
            choose = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no\n\n")

        if (choose.lower().rstrip().lstrip() == "a"): choose = True
        elif (choose.lower().rstrip().lstrip() == "b"): choose = False

        if (choose == True): 

            os.system("cls")
            print("\nHere are all the results for your request input: \n")
            for index in range(len(label)): print(f"{index + 1}. {label[index]} (channel: {channel[index]})") if (len(length) == 0) else None
            for index in range(len(label)): print(f"{index + 1}. {label[index]} (duration: {length[index]}, channel: {channel[index]})")  if (len(length) > 0) else None
            number = input(f"\nWhich file are you downloading? (1 - {len(label)}): ")

            while number.rstrip().lstrip() not in self.numbers(1, len(label)):

                os.system("cls"), print()
                for index in range(len(label)): print(f"{index + 1}. {label[index]} (channel: {channel[index]})") if (len(length) == 0) else None
                for index in range(len(label)): print(f"{index + 1}. {label[index]} (duration: {length[index]}, channel: {channel[index]})")  if (len(length) > 0) else None
                number = input(f"\nInvalid entry, please select a value from the list above (1 - {len(label)}): ")

            url = link[int(number.rstrip().lstrip()) - 1]

        else:

            url = None

        return url


    def monitor_download(self, site, folder, process, file):

        before = os.listdir(folder)
        busy, kb, previous = True, 0, ""
        current, KB, after = previous, kb, before.copy()
        ratio = 3
        time.sleep(10)
        if (len(os.listdir(folder)) != 0): current = os.listdir(folder)[-1]

        while busy:

            time.sleep(20)
            after = os.listdir(folder)
            for item in after: current = item if item not in before else current

            if (len(after) == 0):

                time.sleep(30)
                after = os.listdir(folder)
                for item in after: current = item if item not in before else current

                if (len(after) == 0):

                    busy = False
                    break

            elif (current != ""):

                KB = os.path.getsize(folder + "\\" + current)

                if ((KB == kb) & (current == previous)):

                    duration = self.video_duration(folder + "\\" + current)
                    bits = os.path.getsize(folder + "\\" + current)
                    megabytes, minutes = bits / 1e6, duration / 60
                    ratio = megabytes / minutes
                    if (ratio < 2.5): process.kill(), os.remove(file), subprocess.Popen(f"python crawler.py -i {site} -o {folder}", shell = True)
                    else: busy = False

            kb = KB
            previous = current
            before = after.copy()


    def replace_folder(self, placeholder, folder):

        if ((os.path.isdir(folder) == False) & (os.path.isdir(placeholder) == True)):

            if (len(os.listdir(placeholder)) == 0): os.rmdir(placeholder)
            else: os.rename(placeholder, folder)

        else:

            if ((os.path.isdir(folder) == True) & (os.path.isdir(placeholder) == True)):

                for item in os.listdir(placeholder):

                    if item.endswith(self.extensions):

                        if item not in os.listdir(folder): shutil.move(placeholder + "\\" + item, folder)
                        else: os.remove(placeholder + "\\" + item)

                if (len(os.listdir(placeholder)) == 0): os.rmdir(placeholder)


    def anime_search(self, title):

        url = "https://www.wcostream.com/"
        self.persist_search(url)
        search = self.driver.find_element_by_id("searchbox")
        search.send_keys(title)
        search.send_keys(Keys.ENTER)
        response = self.driver.find_elements_by_css_selector(".aramadabaslik a")
        titles = [item.text for item in response]
        links = [item.get_attribute("href") for item in response]
        family = self.driver.find_elements_by_css_selector(".cerceve-tur-ve-genre")
        genres = [item.text for item in family]
        Genres, Titles, Links = genres.copy(), titles.copy(), links.copy()

        for index in range(len(links)):

            if "subbed" in genres[index].lower():

                address = Titles.index(titles[index])
                Genres.pop(address), Titles.pop(address), Links.pop(address)

        return Titles, Links


    def directory_manager(self, tag, file = None, title = None, field = None):

        current_directory = os.getcwd()
        component = re.split(self.standard, current_directory)
        admin = component[0:3]
        user = "\\".join(admin)
        path = f"{user}\\Documents"
        os.chdir(path)

        if ((self.category == "audio") & (field != "playlist")):

            audio = file
            if (os.path.isdir("Audio") == False): os.makedirs("Audio")
            directory = f"{user}\\Documents\\Audio"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            directory = f"{directory}\\{tag}"
            folder = os.listdir(directory)
            os.chdir(current_directory)

            if file not in folder:

                shutil.move(current_directory + "\\" + file, directory)

            else:

                while audio in folder: audio = audio.split(".")[0] + f" ({random.randint(0, 100)})" + ".mp3"
                os.rename(file, audio)
                shutil.move(current_directory + "\\" + audio, directory)

        elif ((self.category == "video") | (field == "playlist")):

            if (field != "playlist"): os.makedirs("Video") if (os.path.isdir("Video") == False) else None
            else: os.makedirs("Audio") if (os.path.isdir("Audio") == False) else None
            directory = f"{user}\\Documents\\{self.category.title()}"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)
            if ((os.path.isdir(title) == False) & (field == "playlist")): os.makedirs(title)
            if (field == "playlist"): folder = f"{folder}\\{title}"
            if (field == "playlist"): os.chdir(folder)
            return folder

        elif (self.category == "comic book"):

            if (os.path.isdir("Comic Books") == False): os.makedirs("Comic Books")
            directory = f"{user}\\Documents\\Comic Books"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)

        elif ((self.category == "torrent") | (self.category == "animation")):

            if (self.category == "torrent"): 

                if (os.path.isdir("TORRENTS") == False): os.makedirs("TORRENTS")
                directory = f"{user}\\Documents\\TORRENTS"
                tag, title = tag.title(), title.title()

            elif (self.category == "animation"):

                if (os.path.isdir("animation") == False): os.makedirs("animation")
                directory = f"{user}\\Documents\\animation"

            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)
            if (os.path.isdir(title) == False): os.makedirs(title)
            destination = f"{folder}\\{title}"
            os.chdir(current_directory)
            return destination


    def delete_copy(self, current_directory, directory = None, field = None):

        if ((self.category == "video") | (field == "playlist")):

            delete = []
            reference = os.listdir(current_directory)
            compare = [item.split(".")[0] for item in reference]

            for item in reference:

                if item.endswith(self.extensions):

                    count = compare.count(item.split(".")[0])
                    if ((count > 1) & (item.split(".")[0] not in delete)): delete.append(item.split(".")[0])

            for item in reference:

                if (((self.category == "video") & (item.endswith(".mp4") == False) & (item.split(".")[0] in delete)) |
                    ((self.category == "audio") & (item.endswith(".mp3") == False) & (item.split(".")[0] in delete))):

                    file = current_directory + "\\" + item
                    os.remove(file)

        elif (self.category == "audio"):

            reference = os.listdir(directory)
            compare = os.listdir(current_directory)
            holder = [element.split(".")[0] for element in reference]

            for item in compare:

                file = item.split(".")[0]
                data = current_directory + "\\" + item
                if file in holder: os.remove(data)

            for item in reference:

                if item.endswith(self.extensions):

                    file = directory + "\\" + item
                    os.remove(file)

        elif (self.category == "animation"):

            if (os.path.isdir(directory) == True):

                for reference, paths, items in os.walk(current_directory):

                    for path in paths:
                        
                        folder = directory + "\\" + path

                        if (os.path.isdir(folder) == True):

                            duplicate = reference + "\\" + path

                            for item in os.listdir(duplicate):

                                if item not in os.listdir(folder): shutil.move(duplicate + "\\" + item, folder)
                                else: os.remove(duplicate + "\\" + item)

                            os.rmdir(duplicate)


    def link_selector(self, link, title, label, channel, anchor):

        position, best = 0, 0

        for index in range(len(link)):
            
            title_score = fw.ratio(title.lower().rstrip().lstrip(), label[index].lower().rstrip().lstrip())
            channel_score = fw.ratio(channel.lower().rstrip().lstrip(), anchor[index].lower().rstrip().lstrip()) if (channel != None) else 0
            score = title_score + channel_score
            if (score > best): position, best = index, score

        url = link[position]
        return url


    def test_query(self, request, indicator):

        if (indicator == 0):

            status = [character for character in self.restrictions if character in request]

            while ((request == "") | (status != [])):

                os.system("cls")
                request = input("\nInvalid folder name, please provide a valid title for the directory (restricted characters include; ?, /, \\, :, *, >, <, |, \', \" and leaving the query blank): ")
                status.clear()
                status = [character for character in self.restrictions if character in request]

        elif (indicator == 1):

            while (request == ""):

                os.system("cls")
                request = input("\nYour search input is empty, please provide a suitable query: ")

        return request


    def extractor(self, field = "volume"):

        if ((self.category == "video") | (self.category == "audio")):

            count, done = 1, False
            channel = None
            links, titles, duration, fields = [], [], [], []
            channels, anchors, labels, tags = [], [], [], []

            while not done:

                field = self.selector()
                os.system("cls")
                if (self.category == "video"): tag = input("\nWhat category of video are you downloading? (tutorial, lecture etc): ")
                if (self.category == "audio"): tag = input("\nWhat category of audio are you downloading? (podcast, audiobook etc): ")
                status = [character for character in self.restrictions if character in tag]
                if (((tag == "") | (status != []))): tag = self.test_query(tag, 0)
                os.system("cls")
                preference = input("\nDo you have a preferred channel to download your file from?: \n\nA: yes \nB: no \n\n")

                while preference.lower().rstrip().lstrip() not in self.options[0:4]:

                    os.system("cls")
                    preference = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if (preference.lower().rstrip().lstrip() == "a"): preference = True
                elif (preference.lower().rstrip().lstrip() == "b"): preference = False
                os.system("cls")
                if (preference == True): channel = input("\nWhich channel will you be downloading your content from?: ")
                if (channel == ""): channel = self.test_query(channel, 1)
                os.system("cls")
                if ((self.category == "video") & (count == 1)): title = input("\nPlease input a search request for a particular video that you are looking for: ")
                elif ((self.category == "audio") & (count == 1)): title = input("\nPlease input a search request for a particular audio file that you are looking for: ")
                elif ((self.category == "video")): title = input(f"\nPlease input a search request for the {self.ordinal(count)} video(s): ")
                elif ((self.category == "audio")): title = input(f"\nPlease input a search request for the {self.ordinal(count)} file(s): ")
                if (title == ""): title = self.test_query(title, 1)

                if (field == "single"):

                    result = YoutubeSearch(title, max_results = 20).to_dict()
                    link = ["https://www.youtube.com" + entry["url_suffix"] for entry in result]
                    label = [entry["title"] for entry in result]
                    anchor = [entry["channel"] for entry in result]
                    length = [entry["duration"] for entry in result]

                elif (field == "playlist"):

                    result = playlist_search(title, limit = 20).result()["result"]
                    link = [entry["link"] for entry in result]
                    label = [entry["title"] for entry in result]
                    anchor = [entry["channel"]["name"] for entry in result]
                    length = []

                if (len(link) > 1): url = self.show_results(label, link, anchor, length)
                if ((len(link) == 1) | (url == None)): url = self.link_selector(link, title, label, channel, anchor)
                header = label[link.index(url)]
                for character in self.restrictions: header = header.replace(character, "-")
                links.append(url), fields.append(field), tags.append(tag), labels.append(header)
                os.system("cls")
                add = input("\nAre you adding more files to the download schedule?: \n\nA: yes \nB: no \n\n")
                count += 1

                while add not in self.options[0:4]:

                    os.system("cls")
                    add = input("\nInvalid entry, please select an available option: \n\nA: continue adding files to download list \nB: done adding files to download list \n\n")

                if (add.lower().rstrip().lstrip() == "a"): add = "yes"
                elif (add.lower().rstrip().lstrip() == "b"): add = "no"
                if (add.lower().rstrip().lstrip() == "no"): done = True

            os.system("cls")
            return tags, links, fields, labels

        elif (self.category == "comic book"):

            url = "https://readcomiconline.to/Search/Comic"
            issues, headers, paths, fields = [], [], [], []
            done, count = False, 1

            while not done:

                field = self.selector()
                os.system("cls")
                comic, issue = "1", "1"
                if (count == 1): title = input(f"\nPlease input a search request for a particular comic book title: ")
                else: title = input(f"\nPlease input a search request for the {self.ordinal(count)} comic book(s): ")
                if (title == ""): title = self.test_query(title, 1)
                self.persist_search(url)
                search = self.driver.find_element_by_tag_name("input")
                search.send_keys(title)
                search.send_keys(Keys.ENTER)

                if (self.driver.current_url[-5:].lower().rstrip().lstrip() != "comic"): 

                    issues = self.driver.find_elements_by_tag_name("td a")

                else:

                    os.system("cls")
                    select = input("\nDo you want to peruse the available results or let the bot automatically find the requested comic?: \n\nA: list all comics \nB: automatic download \n\n")

                    while select not in self.options[0:4]:

                        os.system("cls")
                        select = input("\nInvalid entry, please select an available option: \n\nA: list all comics \nB: automatic download \n\n")

                    if (select.lower().rstrip().lstrip() == "a"): select = "manual"
                    elif (select.lower().rstrip().lstrip() == "b"): select = "automatic"

                    if (select == "manual"):

                        sites = self.driver.find_elements_by_tag_name("td a")
                        comics = [comic.text for comic in sites]
                        os.system("cls")
                        print("\nHere are the comic books available based on your search request: \n")
                        for index in range(len(comics)): print(f"{index + 1}. {comics[index]}")
                        if (len(comics) > 1): comic = input(f"\n\nWhich comic do you want to download? (1 - {len(comics)}): ")
                        else: print(f"\n\n{comics[0]} will now be downloaded: \n\n")

                        while comic.lower().rstrip().lstrip() not in self.numbers(1, len(comics)):

                            os.system("cls"), print()
                            for index in range(len(comics)): print(f"{index + 1}. {comics[index]}")
                            comic = input(f"\n\nInvalid entry, please specify a value within the given range (1 - {len(comics)}): ")
                            print()

                        book = comics[int(comic) - 1]

                    else:

                        sites = self.driver.find_elements_by_tag_name("td a")
                        comics = [comic.text for comic in sites]
                        channel, anchor = None, None
                        url = self.link_selector(sites, title, comics, channel, anchor)
                        book = url.text

                    comic_book = self.driver.find_element_by_link_text(book)
                    link = comic_book.get_attribute("href")
                    self.persist_search(link)
                    numbers = self.driver.find_elements_by_tag_name("td a")
                    for character in self.restrictions: book = book.replace(character, "-")
                    self.directory_manager(book)

                labels = [number.text for number in numbers]
                labels = list(reversed(labels))
                numbers = [number.get_attribute("href") for number in numbers]
                numbers = list(reversed(numbers))

                if (field == "single"):

                    os.system("cls")

                    if (len(labels) > 1):

                        print(f"\nHere are the available issues for the selected comic book series: \n")
                        for counter in range(len(labels)): print(f"{counter + 1}. {labels[counter]}")
                        issue = input(f"\n\nWhich issue are you downloading from this comic book title? (1 - {len(labels)}): ")
                        print()

                    else: 

                        print(f"\nThere is only one issue in this comic book series, {labels[0]} \n")

                    while issue.rstrip().lstrip() not in self.numbers(1, len(labels)):

                        os.system("cls")
                        print(f"\nInvalid entry, please specify a value within the available range: \n")
                        for counter in range(len(labels)): print(f"{counter + 1}. {labels[counter]}")
                        issue = input(f"\n\nSelect an issue (1 - {len(labels)}): ")
                        print()

                    header = labels[int(issue) - 1]
                    anchor = numbers[int(issue) - 1]
                    labels = header
                    numbers = anchor

                issues.append(numbers), headers.append(labels), paths.append(os.getcwd()), fields.append(field)
                count += 1
                os.system("cls")
                add = input("\nAre you adding more comics to the download schedule?: \n\nA: yes \nB: no \n\n")

                while add not in self.options[0:4]:

                    os.system("cls")
                    add = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if (add.lower().rstrip().lstrip() == "a"): add = "yes"
                elif (add.lower().rstrip().lstrip() == "b"): add = "no"
                if (add.lower().rstrip().lstrip() == "no"): done = True

            return issues, paths, headers, fields

        elif (self.category == "torrent"):

            subprocess.Popen(["C:\\Program Files\\qBittorrent\\qbittorrent.exe"], shell = True)
            types, field = [["series", "show", "shows", "tv show", "tv shows", "anime", "animes", "cartoon", "cartoons", "animated series", "toons"], ["movies", "films", "cinema"]], None
            os.system("cls")
            tag = input("\nWhat category of torrent file(s) are you downloading? (movies, series etc): ")
            status = [character for character in self.restrictions if character in tag]
            if ((tag == "") | (status != [])): tag = self.test_query(tag, 0)
            os.system("cls")
            start, stop = "1", "0"
            choose, done = "b", False
            count, add = 1, "no"
            titles, done = [], False
            begining, end, fields = [], [], []

            if tag.lower().rstrip().lstrip() in types[0]:
                
                while not done:

                    field = self.selector()
                    os.system("cls")
                    if ((field == "episode") & (count == 1)): title = input(f"\nPlease input a particular title for the series that you are searching for along with the required season and episode (format; [title] S[x]E[y] / if you're searching for anything lower than the tenth season and/or episode, use the [title] S[0x]E[0y] format instead): ")
                    elif (field == "episode"): title = input(f"\nPlease specify the title of the {self.ordinal(count)} series that you are searching for along with the required season and episode (format; [title] S[x]E[y] / if you're searching for anything lower than the tenth season and/or episode, use the [title] S[0x]E[0y] format instead): ")
                    elif ((field == "season") & (count == 1)): title, choose = input(f"\nPlease input a particular title for the series that you are searching for along with the required season (format; [title] S[x] / if you're searching for anything lower than the tenth season, use the [title] S[0x] format instead): "), input("\nDo you want to download the entire season?: \n\nA: yes \nB: no \n\n")
                    elif (field == "season"): title, choose = input(f"\nPlease specify the title of the {self.ordinal(count)} series that you are searching for along with the required season (format; [title] S[x] / if you're searching for anything lower than the tenth season, use the [title] S[0x] format instead): "), input("\nDo you want to download the entire season?: \n\nA: yes \nB: no \n\n")
                    elif ((field == "series") & (count == 1)): title, choose = input(f"\nPlease input a particular title for the series that you are searching for (format; [title]): "), input("\nDo you want to download the entire series?: \n\nA: yes \nB: no \n\n")
                    elif (field == "series"): title, choose = input(f"\nPlease specify the title of the {self.ordinal(count)} series that you are searching for (format; [title]): "), input("\nDo you want to download the entire series?: \n\nA: yes \nB: no \n\n")
                    check = title.split()[-1]

                    if (field == "episode"):

                        while check.lower().rstrip().lstrip() not in self.episodes:

                            os.system("cls")
                            title = input("\nInvalid format, the specified file must be provided as follows; [title] S[0x]E[0y]: ")
                            check = title.split()[-1]

                    elif (field == "season"):

                        while check.lower().rstrip().lstrip() not in self.seasons:

                            os.system("cls")
                            title = input("\nInvalid format, the specified file must be provided as follows; [title] S[0x]: ")
                            check = title.split()[-1]

                    while choose.lower().rstrip().lstrip() not in self.options[0:4]:

                        os.system("cls")
                        choose = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                    if (choose.lower().rstrip().lstrip() == "a"): choose = False
                    elif (choose.lower().rstrip().lstrip() == "b"): choose = True
                    os.system("cls")
                    if ((field == "series") & (choose == True)): start, stop = input("\nFrom what season are you starting to download your show?: "), input("\nUp until which season are you downloading your show? (use 0 if you want to download all seasons until the end of the series): ")
                    elif ((field == "season") & (choose == True)): start, stop = input("\nFrom what episode are you starting to download your show?: "), input("\nUp until which episode are you downloading your show? (use 0 if you want to download all episodes until the end of the season): ")
                    if (title == ""): title = self.test_query(title, 1)
                    first = int(start) if start.isdigit() else 1
                    last = int(stop) if stop.isdigit() else 0

                    while (((last < first) & (last != 0)) | (start.lower().rstrip().lstrip() not in self.numbers(0, 100)) | (stop.lower().rstrip().lstrip() not in self.numbers(0, 100))):

                        os.system("cls")
                        if (field == "series"): print(f"\nInvalid entry, the last season must be a positive value larger than the first season: \n")
                        elif (field == "season"): print(f"\nInvalid entry, the last episode must be a positive value larger than the first episode: \n")
                        if (field == "series"): start = input(f"\nChoose which season to start downloading this series from: ")
                        elif (field == "season"): start = input(f"\nChoose which episode to start downloading this season from: ")
                        if (field == "series"): stop = input(f"\nChoose the last season to download from this series: ")
                        elif (field == "season"): stop = input(f"\nChoose the last episode to download from this season: ")
                        first = int(start) if start.isdigit() else 1
                        last = int(stop) if stop.isdigit() else 0

                    os.system("cls")
                    add = input("\nAre you adding more shows to the download schedule?: \n\nA: yes \nB: no \n\n")

                    while add.lower().rstrip().lstrip() not in self.options[0:4]:

                        os.system("cls")
                        add = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                    if (add.lower().rstrip().lstrip() == "a"): add = "yes"
                    elif (add.lower().rstrip().lstrip() == "b"): add = "no"
                    if (add.lower().rstrip().lstrip() == "no"): done = True
                    titles.append(title), fields.append(field)
                    begining.append(start), end.append(stop)
                    choose, count = "b", count + 1
                    start, stop = "1", "0"

            elif (tag.lower().rstrip().lstrip() in types[1]):

                while not done:

                    os.system("cls")
                    if (count == 1): title = input(f"\nPlease input a particular title for the movie that your are searching for: ")
                    else: title = input(f"\nPlease input a search request for the {self.ordinal(count)} movie: ")
                    os.system("cls")
                    add = input("\nAre you adding more movies to the download schedule?: \n\nA: yes \nB: no \n\n")

                    while add not in self.options[0:4]:

                        os.system("cls")
                        add = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                    if (add.lower().rstrip().lstrip() == "a"): add = "yes"
                    elif (add.lower().rstrip().lstrip() == "b"): add = "no"
                    if (add.lower().rstrip().lstrip() == "no"): done = True
                    if (title == ""): title = self.test_query(title, 1)
                    begining.append("1"), end.append("0")
                    titles.append(title), fields.append(None)
                    count += 1

            return titles, tag, fields, begining, end

        elif (self.category == "animation"):

            os.system("cls")
            tag = input("\nWhat category of animated show(s) are you downloading? (movies, series etc): ")
            status = [character for character in self.restrictions if character in tag]
            if ((tag == "") | (status != [])): tag = self.test_query(tag, 0)
            os.system("cls")
            start, stop = "1", "0"
            choose, done = "b", False
            count, add, titles = 1, "no", []
            headers, sites = [], []
            
            while not done:

                os.system("cls")
                title, site, header = [], [], []
                if (count == 1): show = input(f"\nPlease input a particular title for the show that you are searching for: ")
                else: show = input(f"\nPlease specify a title for the {self.ordinal(count)} show that you are searching for: ")
                if (show == ""): show = self.test_query(show, 1)
                text = show.lower().rstrip().lstrip()
                labels, anchors = self.anime_search(show)
                proceed = True
                os.system("cls")

                if (len(anchors) > 0):

                    if (len(anchors) > 1):

                        print("\nHere are the available shows based on your search request: \n")
                        for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                        select = input("\n\nDo you want to download episodes from all of the seasons?: \n\nA: yes \nB: no \n\n")

                        while select.lower().rstrip().lstrip() not in self.options[0:4]:

                            os.system("cls"), print()
                            for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                            select = input("\nInvalid entry, please select an available option, are you downloading episodes from all the seasons?: \n\nA: yes \nB: no \n\n")

                        if (select.lower().rstrip().lstrip() == "a"): select = True
                        elif (select.lower().rstrip().lstrip() == "b"): select = False

                        if (select == False):

                            start = input("\nFrom what season are you starting to download your show?: ")

                            while start.lower().rstrip().lstrip() not in self.numbers(1, len(anchors)):

                                os.system("cls"), print()
                                for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                                start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(anchors)}): ")

                            stop = input("\nUp until which season are you downloading your show? (if you only want to download one season, enter the same value as the starting season): ")

                            while stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(anchors)):

                                os.system("cls"), print()
                                for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                                stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(anchors)}): ")

                            first = int(start) if start.isdigit() else 1
                            last = int(stop) if stop.isdigit() else 0

                            while ((last < first) | (start.lower().rstrip().lstrip() not in self.numbers(1, len(anchors))) | (stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(anchors)))):

                                os.system("cls")
                                print(f"\nInvalid entry, the last season must be a value larger than the first season and within the given range (1 - {len(anchors)}): \n")
                                for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                                start = input(f"\nChoose which season to start downloading {text.title()} from (1 - {len(anchors)}): ")

                                while start.lower().rstrip().lstrip() not in self.numbers(1, len(anchors)):

                                    os.system("cls"), print()
                                    for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                                    start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(anchors)}): ")

                                stop = input(f"\nChoose the last season to download from the series ({start} - {len(anchors)}): ")

                                while first.lower().rstrip().lstrip() not in self.numbers(int(start), len(anchors)):

                                    os.system("cls"), print()
                                    for counter in range(len(anchors)): print(f"{counter + 1}. {labels[counter]}")
                                    stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(anchors)}): ")

                                first = int(start) if start.isdigit() else 1
                                last = int(stop) if stop.isdigit() else 0

                        else: start, stop = "1", str(len(anchors))
                        start, stop = int(start), int(stop)
                        if (stop == start): links, names = [anchors[start - 1]], [labels[start - 1]]
                        elif ((start == 1) & (stop == 0)): links, names = anchors.copy(), labels.copy()
                        elif (stop > start): links, names = anchors[start - 1:stop].copy(), labels[start - 1:stop].copy()

                        for index in range(len(links)):

                            os.system("cls")
                            self.persist_search(links[index])
                            sequence = self.driver.find_elements_by_css_selector("#catlist-listview li a")
                            episodes = [episode.text for episode in sequence]
                            episodes = list(reversed(episodes))
                            anchor = [episode.get_attribute("href") for episode in sequence]
                            anchor = list(reversed(anchor))
                            label = names[index]
                            for character in self.restrictions: label = label.replace(character, "-")
                            print(f"\nThese are all the episodes in {names[index]}: \n")
                            for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                            choose = input(f"\n\nDo you want to download all of the episodes?: \n\nA: yes \nB: no \n\n")

                            while choose.lower().rstrip().lstrip() not in self.options[0:4]:

                                os.system("cls"), print()
                                for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                choose = input(f"\nInvalid entry, please select an available option, are you downloading the entire season of {names[index]}: \n\nA: yes \nB: no \n\n")

                            if (choose.lower().rstrip().lstrip() == "a"): choose = True
                            elif (choose.lower().rstrip().lstrip() == "b"): choose = False

                            if (choose == False):

                                os.system("cls"), print()
                                for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                start = input(f"\n\nFrom what episode are you starting to download {names[index]}?: ")

                                while start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes)):

                                    os.system("cls"), print()
                                    for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                    start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(episodes)}): ")

                                stop = input(f"\nUp until which episode are you downloading this season? (if you only want to download one episode, enter the same value as the starting episode): ")

                                while stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)):

                                    os.system("cls"), print()
                                    for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                    stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(episodes)}): ")

                                first = int(start) if start.isdigit() else 1
                                last = int(stop) if stop.isdigit() else 0

                                while ((last < first) | (start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes))) | (stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)))):

                                    os.system("cls")
                                    print(f"\nInvalid entry, the last episode must be a value larger than the first episode and within the given range (1 - {len(episodes)}): \n")
                                    for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")

                                    start = input(f"\nChoose which episode to start downloading {names[index]} from (1 - {len(episodes)}): ")

                                    while start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes)):

                                        os.system("cls"), print()
                                        for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                        start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(episodes)}): ")

                                    stop = input(f"\nChoose the last episode to download from this season ({start} - {len(episodes)}): ")

                                    while stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)):

                                        os.system("cls"), print()
                                        for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                        stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(episodes)}): ")

                                    first = int(start) if start.isdigit() else 1
                                    last = int(stop) if stop.isdigit() else 0

                            else: start, stop = "1", "0"
                            start, stop = int(start), int(stop)
                            if (start == stop): link, episode = [anchor[start - 1]], [episodes[start - 1]]
                            elif (start < stop): link, episode = anchor[start - 1:stop].copy(), episodes[start - 1:stop].copy()
                            elif ((start == 1) & (stop == 0)): link, episode = anchor.copy(), episodes[start - 1:stop].copy()
                            title.append(label), site.append(link), header.append(episode)

                    elif (len(anchors) == 1):

                        os.system("cls")
                        print(f"\nThere is only one title available with the requested search: {labels[0]}")
                        proceed = input("\n\nDo you want to download episodes from this show?: \n\nA: yes \nB: no \n\n")

                        while proceed.lower().rstrip().lstrip() not in self.options[0:4]:

                            os.system("cls")
                            proceed = input(f"\nInvalid entry, please select an available option: \n\nA: download episodes from {labels[0]} \nB: search for another show \n\n")

                        if (proceed.lower().rstrip().lstrip() == "a"): proceed = True
                        elif (proceed.lower().rstrip().lstrip() == "b"): proceed = False

                        if (proceed == True):

                            os.system("cls")
                            link, label = anchors[0], labels[0]
                            for character in self.restrictions: label = label.replace(character, "-")
                            self.persist_search(link)
                            sequence = self.driver.find_elements_by_css_selector("#catlist-listview li a")
                            episodes = [episode.text for episode in sequence]
                            episodes = list(reversed(episodes))
                            anchor = [episode.get_attribute("href") for episode in sequence]
                            anchor = list(reversed(anchor))
                            print(f"\nThese are all the episodes in {label}: \n")
                            for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                            choose = input("\n\nDo you want to download all of the episodes?: \n\nA: yes \nB: no \n\n")

                            while choose.lower().rstrip().lstrip() not in self.options[0:4]:

                                os.system("cls"), print()
                                for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                choose = input("\n\nInvalid entry, please select an available option, are you downloading all the episodes?: \n\nA: yes \nB: no \n\n")

                            if (choose.lower().rstrip().lstrip() == "a"): choose = True
                            elif (choose.lower().rstrip().lstrip() == "b"): choose = False
                            os.system("cls")

                            if (choose == False):

                                print()
                                for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                start = input(f"\nFrom what episode are you starting to download {label}?: ")

                                while start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes)):

                                    os.system("cls")
                                    start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(episodes)}): ")

                                stop = input("\nUp until which episode are you downloading this season? (if you only want to download one episode, enter the same value as the starting episode): ")

                                while stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)):

                                    os.system("cls")
                                    stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(episodes)}): ")

                            else: start, stop = "1", "0"
                            first = int(start) if start.isdigit() else 1
                            last = int(stop) if stop.isdigit() else 0

                            while ((last < first) | (start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes))) | (stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)))):

                                os.system("cls")
                                print(f"\nInvalid entry, the last episode must be a value larger than the first episode and within the given range (1 - {len(episodes)}): \n")
                                for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                start = input(f"\nChoose which episode to start downloading {label} from (1 - {len(episodes)}): ")

                                while start.lower().rstrip().lstrip() not in self.numbers(1, len(episodes)):

                                    os.system("cls"), print()
                                    for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                    start = input(f"\nInvalid entry, please specify a value within the given range (1 - {len(episodes)}): ")

                                stop = input(f"\nChoose the last episode to download from this season ({start} - {len(episodes)}): ")

                                while stop.lower().rstrip().lstrip() not in self.numbers(int(start), len(episodes)):

                                    os.system("cls"), print()
                                    for counter in range(len(episodes)): print(f"{counter + 1}. {episodes[counter]}")
                                    stop = input(f"\nInvalid entry, please specify a value within the given range ({start} - {len(episodes)}): ")

                                first = int(start) if start.isdigit() else 1
                                last = int(stop) if stop.isdigit() else 0

                            start, stop = int(start), int(stop)
                            if (start == stop): link, episode = [anchor[start - 1]], [episodes[start - 1]]
                            elif (start < stop): link, episode = anchor[start - 1:stop].copy(), episodes[start - 1:stop].copy()
                            elif ((start == 1) & (stop == 0)): link, episode = anchor.copy(), episodes[start - 1:stop].copy()
                            title, site, header = [label], [link], [episode]

                    if (proceed == True):

                        for item in header:

                            for counter in range(len(item)):

                                for character in self.restrictions: item[counter] = item[counter].replace(character, "-")

                        start, stop = str(start), str(stop)
                        titles.append(title), sites.append(site), headers.append(header)
                        os.system("cls")
                        add = input("\nAre you adding more shows to the download schedule?: \n\nA: yes \nB: no \n\n")

                        while add.lower().rstrip().lstrip() not in self.options[0:4]:

                            os.system("cls")
                            add = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                        if (add.lower().rstrip().lstrip() == "a"): add = "yes"
                        elif (add.lower().rstrip().lstrip() == "b"): add = "no"
                        if (add.lower().rstrip().lstrip() == "no"): done = True
                        choose, count = "b", count + 1
                        start, stop = "1", "0"

                elif (len(anchors) == 0):

                    exit = input(f"\nThere are no results matching your requested search; '{show}', do you want to try a different title or exit the current download session? (all previously added shows will continue to be downloaded): \n\nA: input another title \nB: proceed to download specified shows \n\n")

                    while exit.lower().rstrip().lstrip() not in self.options[0:4]:

                        os.system("cls")
                        exit = input(f"\nInvalid entry, please select an available option: \n\nA: input another title \nB: proceed to download specified shows \n\n")

                    if (exit.lower().rstrip().lstrip() == "a"): done = False
                    elif (exit.lower().rstrip().lstrip() == "b"): done = True

            os.system("cls")
            return titles, sites, headers, tag


    def torrent_selector(self, title, links, titles, seeders, leechers, sizes, sites, ID = None):

        score, best, magnet, test = 0, 0, None, []
        url = "http://samcloud.tplinkdns.com:50000"
        getData = "/getTorrentData"
        good_quality = ["720", "265"]
        seed, leech, byte, torrent, tag = [], [], [], [], []
        links, titles, seeders, leechers, sizes, sites, check = self.filter_torrents(links, titles, seeders, leechers, sizes, sites)
        target = title.lower().rstrip().lstrip()
        flag = False

        for index in range(len(links)):

            flag = False
            if (links[index][-1] == "/"): append = "&site="
            else: append = "/&site="
            fetch_link = "?link=" + links[index] + append + sites[index]
            response = requests.get(url + getData + fetch_link)
            compare = " ".join(titles[index].split("."))
            score = fw.ratio(compare.lower().rstrip().lstrip(), target)
            if (score < 31): score, flag = self.test_similarity(compare.lower().rstrip().lstrip(), target), True

            if (((score > 50) & (response.json() != "Invalid Request") & (flag == True)) |
                ((score >= 31) & (response.json() != "Invalid Request") & (flag == False))):

                if (check == True):

                    if (((good_quality[0] in titles[index]) & (good_quality[1] in titles[index])) | 
                        (("hd" in titles[index].lower()) & (good_quality[0] not in titles[index]) & (good_quality[1] not in titles[index]))):

                        if ((ID.lower() in titles[index].lower()) | (ID == None)):

                            magnet = response.json()["magnet"]
                            torrent.append(magnet), leech.append(leechers[index])
                            seed.append(seeders[index]), byte.append(sizes[index])
                            tag.append(compare)

                else:

                    if ((ID.lower() in titles[index].lower()) | (ID == None)):

                        magnet = response.json()["magnet"]
                        torrent.append(magnet), leech.append(leechers[index])
                        seed.append(seeders[index]), byte.append(sizes[index])
                        tag.append(compare)

        if (len(torrent) == 0): magnet = "empty"
        else: magnet = self.choose_magnet(torrent, seed, leech, byte, tag)
        return magnet


    def test_similarity(self, compare, target):

        score, percent = 0, 0
        for index in range(len(target)): score += 1 if (compare[index] == target[index]) else 0
        percent = 100*score / len(target)
        return percent


    def choose_magnet(self, torrents, seeds, leeches, sizes, tags):

        fastest = max(seeds)
        occurance = seeds.count(fastest)

        if (occurance == 1):

            address = seeds.index(fastest)
            magnet = torrents[address]

        else:

            slowest = max(leeches)
            occurance = leeches.count(slowest)

            if (occurance == 1):

                address = seeds.index(fastest)
                magnet = torrents[address]

            else:

                smallest = min(sizes)
                occurance = sizes.count(smallest)
                fast = seeds.index(fastest)
                slow = leeches.index(slowest)
                small = sizes.count(smallest)

                if (occurance == 1):

                    address = seeds.index(fastest)
                    magnet = torrents[address]

                else:

                    indices = [position for position, x in enumerate(seeds) if x == fastest]
                    address, previous = indices[0], 100e9

                    for position in indices:

                        slow = leeches[position]
                        if (slow <= previous): address = position
                        previous = slow

                    magnet = torrents[address]

        return magnet


    def filter_torrents(self, links, titles, seeders, leechers, sizes, sites):

        seeders = [int(seed) for seed in seeders]
        leechers = [int(leech) for leech in leechers]
        Links, Titles = links.copy(), titles.copy()
        Seeders, Leechers = seeders.copy(), leechers.copy()
        Sizes, Sites = sizes.copy(), sites.copy()
        test, check, skip = [], False, False
        good_quality = ["720", "265"]
        other_quality = ["2160", "1080", "480", "264"]
        bad_quality = ["hdcam", "cam", "cam-rip", "ts", "hdts", "telesync", "pdvd", "predvdrip", "x264-ion10", "mp4-mobile", "dub", "hindi", "3d"]
        sizes, Sizes = self.convert_size(sizes), self.convert_size(Sizes)

        for index in range(len(titles)):

            text = " ".join(titles[index].split("."))
            header = text.split()
            address = Links.index(links[index])

            for word in header:

                for quality in bad_quality:

                    if quality in word.lower().rstrip().lstrip():

                        Links.pop(address), Titles.pop(address)
                        Seeders.pop(address), Leechers.pop(address)
                        Sizes.pop(address), Sites.pop(address)
                        skip = True
                        break

                if (skip == True): 

                    skip = False
                    break

        for title in Titles:

            if (((good_quality[0] in title) & (good_quality[1] in title)) |
                (("hd" in title.lower()) & (good_quality[0] not in title) & (good_quality[1] not in title))):

                check = True
                break

        if (check == True):
    
            links, titles = Links.copy(), Titles.copy()
            seeders, leechers = Seeders.copy(), Leechers.copy()
            sizes, sites = Sizes.copy(), Sites.copy()

            for index in range(len(Sizes)):

                for quality in other_quality:

                    if quality in Titles[index].lower().rstrip().lstrip():

                        address = titles.index(Titles[index])
                        links.pop(address), titles.pop(address)
                        seeders.pop(address), leechers.pop(address)
                        sizes.pop(address), sites.pop(address)
                        break

            Links, Titles = links.copy(), titles.copy()
            Seeders, Leechers = seeders.copy(), leechers.copy()
            Sizes, Sites = sizes.copy(), sites.copy()

        links, titles = list(reversed(Links)), list(reversed(Titles))
        seeders, leechers = list(reversed(Seeders)), list(reversed(Leechers))
        sizes, sites = list(reversed(Sizes)), list(reversed(Sites))
        return links, titles, seeders, leechers, sizes, sites, check


    def convert_size(self, size):

        for index in range(len(size)):

            if (size[index][-2:] == "YB"): factor = 1e24
            elif (size[index][-2:] == "ZB"): factor = 1e21
            elif (size[index][-2:] == "EB"): factor = 1e18
            elif (size[index][-2:] == "PB"): factor = 1e15
            elif (size[index][-2:] == "TB"): factor = 1e12
            elif (size[index][-2:] == "GB"): factor = 1e9
            elif (size[index][-2:] == "MB"): factor = 1e6
            elif (size[index][-2:] == "KB"): factor = 1e3
            else: factor = 1
            byte = "".join(size[index][0:-3].split(","))
            size[index] = float(byte)*factor

        return size


    def slugify(self, value):

        title = ucd.normalize("NFKD", value).encode("ascii", "ignore")
        title = re.sub("[^\\w\\s-]", "", title.decode())
        title = str(title.strip().lower().rstrip().lstrip())
        title = str(re.sub("[-\\s]+", "-", title))
        return title


    def persist_search(self, site):

        done = False

        while not done:

            try:

                self.driver.get(site)
                done = True
                break

            except Exception as E:

                print(E)
                time.sleep(2)
                done = False
                continue


    def save_images(self):

        options = self.driver.find_elements_by_tag_name("select")
        quality = self.driver.find_element_by_id("selectQuality")
        Quality = Select(quality)
        Quality.select_by_visible_text("High quality")
        page = self.driver.find_element_by_id("selectReadType")
        Page = Select(page)
        Page.select_by_visible_text("All pages")
        website = str(self.driver.page_source)
        images = []

        with open("comicbook_site.txt", "w+") as file:

            file.write(website)
            file.seek(0)

            for line in file:

                start = line.find("lstImages.push(")
                end = line.find(");")

                if (start != -1):

                    anchor = line[start + 16:end - 1]
                    anchor = anchor.replace("1600", "3975")
                    images.append(anchor)

        return images


    def download_images(self, image, counter):

        try:

            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'}
            site = requests.get(image.strip("\""), headers = headers)
            with open(f"{counter}.jpg", "wb") as file: file.write(site.content)

        except:

            urllib.request.urlretrieve(image, f"{counter}.jpg")


    def image_thread(self, images):

        pages = list(range(len(images)))
        bulk, section = 50, 0

        if (len(images) > bulk):

            batch = int(len(images) / bulk)
            remainder = len(images) - batch*bulk

            for index in range(batch):

                pages = list(range(section, section + bulk))
                with concurrent.futures.ThreadPoolExecutor(bulk) as executor: executor.map(self.download_images, images[section: section + bulk], pages)
                section += bulk

            if (remainder != 0):

                pages = list(range(section, section + remainder))
                with concurrent.futures.ThreadPoolExecutor(remainder) as executor: executor.map(self.download_images, images[section: section + remainder], pages)

        else:

            with concurrent.futures.ThreadPoolExecutor(len(images)) as executor: executor.map(self.download_images, images, pages)


    def pdf_converter(self, title):

        files = os.listdir(os.getcwd())
        folder = sorted(files, key = lambda file: int(file.split(".")[0]) if file.endswith(".jpg") else -1)
        images = [file for file in folder if file.endswith(".jpg")]
        with open(f"{title}.pdf", "wb") as PDF: PDF.write(converter.convert(images))


    def process_file(self, title):

        done = False

        while not done:

            try:

                files = os.listdir(os.getcwd())
                if (f"{title}.pdf" in files): os.remove(f"{title}.pdf")
                images = self.save_images()
                self.image_thread(images)
                self.pdf_converter(title)
                done = True
                break

            except:

                done = False
                continue


    def kill_chrome(self):

        folder = os.listdir(os.getcwd())
        parent = psutil.Process(self.driver.service.process.pid)
        children = parent.children(recursive = True)

        if ("chrome_tabs.txt" in folder):
    
            with open("chrome_tabs.txt", "r") as file: ID = file.readlines()

            for pid in ID:

                try: os.kill(int(pid.strip("\n")), signal.SIGTERM)
                except: continue

        with open("chrome_tabs.txt", "w") as file:

            file.write(f"{self.driver.service.process.pid}")
            for child in children: file.write(f"\n{child.pid}")
                
                
                
                
if __name__ == "__main__":
    
    # download qbit-torrent, configure server UI manager and setup a username & password
    user = "" # qbit-torrent server UI manager login name
    password = "" # qbit-torrent server UI manager login password
    path = os.getcwd() + "\\chromedriver" # keep the chromium executable in the same folder as this program
    downloader = Downloader(path, user, password)
    downloader.search()
    downloader.driver.quit()
    os.system("cls")
    print("\nDownload complete\n")
