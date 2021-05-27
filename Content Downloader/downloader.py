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


class Downloader(object):
    
    options = ["A", "a", "B", "b", "C", "c", "D", "d"]
    standard = r"[^a-zA-Z0-9\s:]"
    restrictions = ["?", "/", "\\", ":", "*", ">", "<", "|", "'", '"']
    symbols = ["|", "\\", "-", "/"]
    progress = lambda self, total, status, indicator = None: print("\ndownload progress: |" + "/"*int(10*status / total) + "."*(10 - int(10*status / total)) + (f"| [file {status + 1} out of {total}]" if (indicator == None) else "| [done]"))
    animate = lambda self, total, status, symbol, indicator = None: print("\ndownload progress: |" + "/"*(int(10*status / total) if (status != total) else int(10*status / total) - 1) + f"{symbol}" + "."*(9 - int(10*status / total)) + (f"| [file {status + 1} out of {total}]" if (indicator == None) else "| [done]"))

    def __init__(self, browser_path, qbit_admin, qbit_password):

        self.qbit_admin = qbit_admin
        self.qbit_password = qbit_password
        self.directory = browser_path
        self.reset_browser()


    def animator(self, total, status, indicator = None):

        for symbol in self.symbols:

            os.system("cls")
            self.animate(total, status, symbol, indicator)
            time.sleep(0.2)

        os.system("cls")
        self.progress(total, status, indicator)


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

        self.driver.implicitly_wait(30)
        self.kill_chrome()


    def selector(self, indicator = 0):

        if (indicator == None):

            os.system("cls")
            category = input("\nWhat type of content are you downloading: \n\nA: audio \nB: video \nC: comic book \nD: torrent \n\n")
            if (category.lower().rstrip() == "a"): self.category = "audio"
            elif (category.lower().rstrip() == "b"): self.category = "video"
            elif (category.lower().rstrip() == "c"): self.category = "comic book"
            elif (category.lower().rstrip() == "d"): self.category = "torrent"

            else:

                while category not in self.options:

                    os.system("cls")
                    category = input("\nInvalid entry, please select an available file type: \n\nA: audio \nB: video \nC: comic book \nD: torrent \n\n")

                if (category.lower().rstrip() == "a"): self.category = "audio"
                elif (category.lower().rstrip() == "b"): self.category = "video"
                elif (category.lower().rstrip() == "c"): self.category = "comic book"
                elif (category.lower().rstrip() == "d"): self.category = "torrent"

        elif (self.category == "audio"):

            os.system("cls")
            preference = input("\nDo you have a preferred channel to download your file from?: \n\nA: yes \nB: no \n\n")
            if (preference.lower().rstrip() == "a"): preference = "yes"
            elif (preference.lower().rstrip() == "b"): channel = None

            else:

                while preference not in self.options[0:4]:

                    os.system("cls")
                    preference = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if (preference.lower().rstrip() == "a"): preference = "yes"
                elif (preference.lower().rstrip() == "b"): channel = None

            os.system("cls")
            if (preference == "yes"): channel = input("\nPlease enter a channel to search for your content: ")
            return channel

        elif (self.category == "video"):

            os.system("cls")
            field = input("\nAre you downloading a playlist or a single file: \n\nA: single video \nB: playlist \n\n")
            if (field.lower().rstrip() == "a"): field = "single"
            elif (field.lower().rstrip() == "b"): field = "playlist"

            else:

                while field not in self.options[0:4]:

                    os.system("cls")
                    field = input("\nInvalid entry, please select an available option: \n\nA: single video \nB: playlist \n\n")

                if (field.lower().rstrip() == "a"): field = "single"
                elif (field.lower().rstrip() == "b"): field = "playlist"

            return field

        elif (self.category == "comic book"):

            os.system("cls")
            field = input("\nAre you downloading an entire collection or only a single issue: \n\nA: single issue \nB: collection \n\n")
            if (field.lower().rstrip() == "a"): field = "single"
            elif (field.lower().rstrip() == "b"): field = "collection"

            else:

                while field not in self.options[0:4]:

                    os.system("cls")
                    field = input("\nInvalid entry, please select an available option: \n\nA: single issue \nB: collection \n\n")

                if (field.lower().rstrip() == "a"): field = "single"
                elif (field.lower().rstrip() == "b"): field = "collection"

        elif (self.category == "torrent"):

            os.system("cls")
            subprocess.Popen(["C:\\Program Files\\qBittorrent\\qbittorrent.exe"], shell = True)
            field = input("\nAre you downloading a required season, an entire series or only one episode: \n\nA: single episode \nB: one season \nC: all seasons \n\n")
            if (field.lower().rstrip() == "a"): field = "episode"
            elif (field.lower().rstrip() == "b"): field = "season"
            elif (field.lower().rstrip() == "c"): field = "series"

            else:

                while field not in self.options[0:6]:

                    os.system("cls")
                    field = input("\nInvalid entry, please select an available option: \n\nA: single episode \nB: one season \nC: all seasons \n\n")

                if (field.lower().rstrip() == "a"): field = "episode"
                elif (field.lower().rstrip() == "b"): field = "season"
                elif (field.lower().rstrip() == "c"): field = "series"

            return field


    def search(self):

        self.selector(None)
        
        if (self.category == "audio"):

            tag, link, title, label, channel, source = self.extractor()
            url = self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = url, download = False)
            name = f"{data['title']}"
            for character in self.restrictions: name = name.replace(character, "-")
            name = f"{name}.%(ext)s"

            configuration = {"format": "bestaudio/best",
                             "keepvideo": False,
                             "outtmpl": name,
                             "postprocessors": [{"key": "FFmpegExtractAudio",
                                                 "preferredcodec": "mp3",
                                                 "preferredquality": "192"}]}

            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])

            try:

                name = name.split(".")[0] + ".mp3"
                self.directory_manager(tag, name)

            except: 

                name = self.slugify(name)
                self.directory_manager(tag, name)

        elif (self.category == "video"):

            tag, link, title, label, channel, source = self.extractor()
            url = self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = url, download = True)
            configuration = {"format": "18", "keepvideo": True}
            current_directory, folder = self.directory_manager(tag)
            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])
            self.delete_copy(current_directory, folder)

        elif (self.category == "comic book"):

            field = self.selector()
            extensions = (".txt", ".jpg")
            issues, path, names = self.extractor()

            if (field == "single"):

                os.system("cls")
                issue = input("\nWhich issue are you downloading from the selected comic book series?: ")
                if issue.isdigit(): issue = int(issue)

                else:

                    while not issue.isdigit():

                        os.system("cls")
                        issue = input("\nInvalid entry, please specify an integer value for the selected comic book series: ")

                    issue = int(issue)

                name = issues[issue - 1].text
                comic_book = self.driver.find_element_by_link_text(name)
                comic_book.click()
                for character in self.restrictions: name = name.replace(character, "-")
                self.servey_detector(self.driver.current_url)
                self.process_file(name)
                self.driver.quit()
                folder = os.listdir(path)
                for file in folder:
                    if file.endswith(extensions): os.remove(file)

            else:
 
                folder = os.listdir(path)
                webpage = self.driver.current_url
                size = len(issues)

                for index in range(size):

                    if f"{names[index]}.pdf" not in folder:

                        self.animator(size, index)
                        self.servey_detector(self.driver.current_url)
                        name = names[index]
                        comic_book = self.driver.find_element_by_link_text(name)
                        comic_book.click()
                        self.servey_detector(self.driver.current_url)
                        for character in self.restrictions: name = name.replace(character, "-")
                        self.process_file(name)
                        self.persist_search(webpage)
                        folder = os.listdir(path)
                        for file in folder:
                            if file.endswith(extensions): os.remove(file)

                self.animator(size, size, 0)
                self.driver.quit()

        elif (self.category == "torrent"):

            url = "http://samcloud.tplinkdns.com:50000"
            types = ["series", "show", "tv show"]
            getSites = "/getSites"
            getTorrents = "/getTorrents"
            Sites = requests.get(url + getSites)
            websites = Sites.json()["sites"]
            title, tag, field, initial, final = self.extractor()
            data, sites, done, check = [], [], False, False
            complete, count, counter = False, initial, initial
            folder = self.directory_manager(tag, title = title)
            qbt = Client("http://127.0.0.1:8080/")
            qbt.login(self.qbit_admin, self.qbit_password)
            length = 0

            if (tag.lower().rstrip() in types):

                if (field == "episode"):

                    search_link = "?search_key=" + title + "&site="
                    results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                    pages = [result[1] for result in results]
                    length = len(results)
                    for index in range(length):
                        for address in range(len(results[index][0])): sites.append(pages[index])
                    for result in results: data += result[0]
                    titles = [result["name"] for result in data]
                    seeders = [result["seeds"] for result in data]
                    leechers = [result["leeches"] for result in data]
                    sizes = [result["size"] for result in data]
                    links = [result["link"] for result in data]
                    torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                    qbt.download_from_link(torrent, savepath = folder)

                elif (field == "season"):

                    length = 0
                    search_link = "?search_key=" + title + " complete" + "&site="
                    results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                    width = len(results)
                    websites = Sites.json()["sites"]
                    data, sites = [], []
                    done, skip = False, False
                    for index in range(width): length += len(results[index][0])

                    if (length == 0):

                        while not done:

                            length = 0
                            if ((final != 0) & (count == final + 1)): break
                            prefix = "0" if (count < 10) else ""
                            search_link = "?search_key=" + title + "E" + prefix + str(count) + "&site="
                            results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                            width = len(results)
                            files = os.listdir(folder)
                            number = title[-3:] + "E" + prefix + str(count)
                            for index in range(width): length += len(results[index][0])
                            count += 1

                            for file in files:

                                if number in file:

                                    skip = True
                                    break

                            if (skip != True):

                                if (length > 0):

                                    length = len(results)
                                    pages = [result[1] for result in results]
                                    for index in range(length):
                                        for address in range(len(results[index][0])): sites.append(pages[index])
                                    for result in results: data += result[0]
                                    titles = [result["name"] for result in data]
                                    seeders = [result["seeds"] for result in data]
                                    leechers = [result["leeches"] for result in data]
                                    sizes = [result["size"] for result in data]
                                    links = [result["link"] for result in data]
                                    torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                                    qbt.download_from_link(torrent, savepath = folder)
                                    data, sites = [], []
                                    done, skip = False, False

                                elif ((length == 0) & (count == 2)):

                                    done = True
                                    skip = False
                                    break

                                else:

                                    done = False
                                    skip = False

                            else:

                                skip = False
                                done = False

                    else:

                        length = len(results)
                        pages = [result[1] for result in results]
                        for index in range(length):
                            for address in range(len(results[index][0])): sites.append(pages[index])
                        for result in results: data += result[0]
                        titles = [result["name"] for result in data]
                        seeders = [result["seeds"] for result in data]
                        leechers = [result["leeches"] for result in data]
                        sizes = [result["size"] for result in data]
                        links = [result["link"] for result in data]
                        torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                        if (torrent == "empty"): websites = [[], [], []]
                        else: qbt.download_from_link(torrent, savepath = folder)

                elif (field == "series"):

                    while not done:

                        length = 0
                        if ((final != 0) & (counter == final + 1)): break
                        season = "0" if (counter < 10) else ""
                        search_link = "?search_key=" + title + " S" + season + str(counter) + " complete" + "&site="
                        results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                        ID = f"Season {counter}"
                        subfolder = folder + f"\\{ID}"
                        if (os.path.isdir(ID) == False): os.makedirs(ID)
                        websites = Sites.json()["sites"]
                        complete, skip, count = False, False, 1
                        data, sites = [], []
                        width = len(results)
                        for index in range(width): length += len(results[index][0])

                        if (length == 0):

                            while not complete:

                                length = 0
                                episode = "0" if (count < 10) else ""
                                search_link = "?search_key=" + title + " S" + season + str(counter) + "E" + episode + str(count) + "&site="
                                results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                                width = len(results)
                                files = os.listdir(subfolder)
                                number = "S" + season + str(counter) + "E" + episode + str(count)
                                for index in range(width): length += len(results[index][0])
                                counter += 1

                                for file in files:

                                    if number in file:

                                        skip = True
                                        break

                                if (skip == False):

                                    if (length > 0):

                                        length = len(results)
                                        pages = [result[1] for result in results]
                                        for index in range(length):
                                            for address in range(len(results[index][0])): sites.append(pages[index])
                                        for result in results: data += result[0]
                                        titles = [result["name"] for result in data]
                                        seeders = [result["seeds"] for result in data]
                                        leechers = [result["leeches"] for result in data]
                                        sizes = [result["size"] for result in data]
                                        links = [result["link"] for result in data]
                                        torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                                        qbt.download_from_link(torrent, savepath = subfolder)
                                        data, sites = [], []
                                        skip = False
                                        count += 1

                                    elif ((length == 0) & (count == 1)):

                                        complete = True 
                                        done = True
                                        os.rmdir(ID)
                                        break

                                    else:

                                        complete = True 
                                        skip = False
                                        done = False
                                        break

                                else:

                                    skip = False
                                    count += 1
                                    done = False
                                    complete = False

                        else:

                            length = len(results)
                            pages = [result[1] for result in results]
                            for index in range(length):
                                for address in range(len(results[index][0])): sites.append(pages[index])
                            for result in results: data += result[0]
                            titles = [result["name"] for result in data]
                            seeders = [result["seeds"] for result in data]
                            leechers = [result["leeches"] for result in data]
                            sizes = [result["size"] for result in data]
                            links = [result["link"] for result in data]
                            torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                            if (torrent == "empty"): websites = [[], [], []]
                            else: 
                                qbt.download_from_link(torrent, savepath = subfolder)
                                counter += 1

            else:

                search_link = "?search_key=" + title + "&site="
                results = [(requests.get(url + getTorrents + search_link + site).json()["torrents"], site) for site in websites if (len(requests.get(url + getTorrents + search_link + site).json()["torrents"]) != 0)]
                length = len(results)
                pages = [result[1] for result in results]
                for index in range(length):
                    for address in range(len(results[index][0])): sites.append(pages[index])
                for result in results: data += result[0]
                titles = [result["name"] for result in data]
                seeders = [result["seeds"] for result in data]
                leechers = [result["leeches"] for result in data]
                sizes = [result["size"] for result in data]
                links = [result["link"] for result in data]
                torrent = self.torrent_selector(title, links, titles, seeders, leechers, sizes, sites)
                qbt.download_from_link(torrent, savepath = folder)

            subprocess.Popen(["C:\\Program Files\\qBittorrent\\qbittorrent.exe"], shell = True)


    def directory_manager(self, tag, file = None, title = None):

        current_directory = os.getcwd()
        component = re.split(self.standard, current_directory)
        name = component[0:3]
        user = "\\".join(name)
        path = f"{user}\\Documents"
        os.chdir(path)

        if (self.category == "audio"):

            if (os.path.isdir("Audio") == False): os.makedirs("Audio")
            directory = f"{user}\\Documents\\Audio"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            directory = f"{directory}\\{tag}"
            folder = os.listdir(directory)
            os.chdir(current_directory)
            if file not in folder: shutil.move(current_directory + "\\" + file, directory)

            else:

                while file in folder:

                    audio = file.split(".")[0]
                    audio += f" ({random.randint(0, 100)})"
                    audio += ".mp3"
                    file = audio

                os.rename(file, audio)
                shutil.move(current_directory + "\\" + audio, directory)

        elif (self.category == "video"):

            if (os.path.isdir("Video") == False): os.makedirs("Video")
            directory = f"{user}\\Documents\\Video"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)
            return current_directory, folder

        elif (self.category == "comic book"):

            if (os.path.isdir("Comic Books") == False): os.makedirs("Comic Books")
            directory = f"{user}\\Documents\\Comic Books"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)

        elif (self.category == "torrent"):

            if (os.path.isdir("TORRENTS") == False): os.makedirs("TORRENTS")
            directory = f"{user}\\Documents\\TORRENTS"
            os.chdir(directory)
            if (os.path.isdir(tag) == False): os.makedirs(tag)
            folder = f"{directory}\\{tag}"
            os.chdir(folder)
            if (os.path.isdir(title) == False): os.makedirs(title)
            destination = f"{folder}\\{title}"
            os.chdir(destination)
            return destination


    def delete_copy(self, current_directory, directory):

        reference = os.listdir(directory)
        compare = os.listdir(current_directory)
        holder = [element.split(".")[0] for element in reference]

        for item in compare:

            file = item.split(".")[0]
            data = os.path.join(current_directory, item)
            if file in holder: os.remove(data)


    def link_selector(self, link, title, label, channel, source):

        position, best = 0, 0
        size = len(link)

        for index in range(size):
            
            title_score = fw.ratio(title.lower().rstrip(), label[index].lower().rstrip())
            channel_score = fw.ratio(channel.lower().rstrip(), source[index].lower().rstrip()) if (channel != None) else 0
            score = title_score + channel_score
            if (score > best): position = index
            if (score > best): best = score

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


    def extractor(self):

        if (self.category == "audio"):

            os.system("cls")
            tag = input("\nWhat category of audio are you downloading? (podcast, audiobook etc): ")
            status = [character for character in self.restrictions if character in tag]
            if ((tag == "") | (status != [])): tag = self.test_query(tag, 0)
            channel = self.selector()
            os.system("cls")
            title = input("\nPlease input a search request for the required file: ")
            if (title == ""): title = self.test_query(title, 1)
            result = YoutubeSearch(title, max_results = 20).to_dict()
            link = ["https://www.youtube.com" + entry['url_suffix'] for entry in result]
            label = [entry['title'] for entry in result]
            source = [entry['channel'] for entry in result] if (channel != None) else []

        elif (self.category == "video"):

            field = self.selector()
            os.system("cls")
            tag = input("\nWhat category of video are you downloading? (tutorial, lecture etc): ")
            status = [character for character in self.restrictions if character in tag]
            if ((tag == "") | (status != [])): tag = self.test_query(tag, 0)
            os.system("cls")
            channel = input("\nWhich channel will you be downloading your content from?: ")
            if (channel == ""): channel = self.test_query(channel, 1)
            os.system("cls")
            title = input("\nPlease input a search request for the required video(s): ")
            if (title == ""): title = self.test_query(title, 1)

            if (field == "single"):

                result = YoutubeSearch(title, max_results = 20).to_dict()
                link = ["https://www.youtube.com" + entry['url_suffix'] for entry in result]
                label = [entry['title'] for entry in result]
                source = [entry['channel'] for entry in result]

            elif (field == "playlist"):

                result = playlist_search(title, limit = 20).result()["result"]
                link = [entry["link"] for entry in result]
                label = [entry["title"] for entry in result]
                source = [entry["channel"]["name"] for entry in result]

        elif (self.category == "comic book"):

            path = os.getcwd()
            url = "https://readcomiconline.to/Search/Comic"
            os.system("cls")
            title = input("\nPlease input a search request for the required comic book(s): ")
            if (title == ""): title = self.test_query(title, 1)
            self.persist_search(url)
            search = self.driver.find_element_by_tag_name("input")
            search.send_keys(title)
            search.send_keys(Keys.ENTER)
            self.servey_detector(self.driver.current_url)
            if (self.driver.current_url[-5:].lower().rstrip() != "comic"): issues = self.driver.find_elements_by_tag_name("td a")

            else:

                os.system("cls")
                mode = input("\nDo you want to peruse the available results or let the bot automatically find the requested comic?: \n\nA: list all comics \nB: automatic download \n\n")
                if (mode.lower().rstrip() == "a"): mode = "manual"
                elif (mode.lower().rstrip() == "b"): mode = "automatic"

                else:

                    while mode not in self.options[0:4]:

                        os.system("cls")
                        mode = input("\nInvalid entry, please select an available option: \n\nA: list all comics \nB: automatic download \n\n")

                    if (mode.lower().rstrip() == "a"): mode = "manual"
                    elif (mode.lower().rstrip() == "b"): mode = "automatic"

                if (mode == "manual"):

                    sites = self.driver.find_elements_by_tag_name("td a")
                    comics = [comic.text for comic in sites]
                    size = len(comics)
                    values = [str(index) for index in range(1, size + 1)]
                    os.system("cls")
                    print("\nHere are the comic books available based on your search request: \n\n")
                    for index in range(size): print(f"{index + 1}. {comics[index]}")
                    comic = input(f"\n\nWhich comic do you want to download? (1 - {size}): ")
                    if (comic.isdigit() & (comic in values)): comic = int(comic)

                    else:

                        while ((comic.isdigit() != True) | (comic not in values)):

                            os.system("cls"), print()
                            for index in range(size): print(f"{index + 1}. {comics[index]}")
                            comic = input(f"\nInvalid entry, please specify an integer value within the given range (1 - {size}): ")

                        comic = int(comic)

                    book = comics[comic - 1]

                else:

                    sites = self.driver.find_elements_by_tag_name("td a")
                    comics = [comic.text for comic in sites]
                    channel, source = None, None
                    url = self.link_selector(sites, title, comics, channel, source)
                    book = url.text

                comic_book = self.driver.find_element_by_link_text(book)
                comic_book.click()
                self.servey_detector(self.driver.current_url)
                issues = self.driver.find_elements_by_tag_name("td a")
                for character in self.restrictions: book = book.replace(character, "-")
                self.directory_manager(book)

            names = [issue.text for issue in issues]
            names = list(reversed(names))
            return issues, path, names

        elif (self.category == "torrent"):

            files = ["series", "show", "tv show"]
            field = self.selector()
            os.system("cls")
            tag = input("\nWhat category of torrent file(s) are you downloading? (movies, series etc): ")
            status = [character for character in self.restrictions if character in tag]
            if ((tag == "") | (status != [])): tag = self.test_query(tag, 0)
            os.system("cls")
            start, stop = "1", "0"
            choose = "b"

            if (tag.lower().rstrip() in files):

                if (field == "episode"):  title = input("\nPlease specify the name of the series that you are searching for along with the required season and episode (format; [name] S[x]E[y] / if you're searching for anything lower than the tenth season and/or episode, use the [name] S[0x]E[0y] format instead): ")
                elif (field == "season"):  title, choose = input("\nPlease specify the name of the series that you are searching for along with the required season (format; [name] S[x] / if you're searching for anything lower than the tenth season, use the [name] S[0x] format instead): "), input("\nDo you want to download the entire season?: \n\nA: yes \nB: no \n\n")
                elif (field == "series"):  title, choose = input("\nPlease specify the name of the series that you are searching for (format; [name]): "), input("\nDo you want to download the entire series?: \n\nA: yes \nB: no \n\n")
                if (choose.lower().rstrip() == "a"): choose = False
                elif (choose.lower().rstrip() == "b"): choose = True
                else:                    
                    while choose not in self.options[0:4]: choose = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")
                    if (choose.lower().rstrip() == "a"): choose = False
                    elif (choose.lower().rstrip() == "b"): choose = True
                if ((field == "series") & (choose == True)): start, stop = input("\nFrom what season are you starting to download your show?: "), input("\nUp until which season are you downloading your show? (use 0 if you want to download all seasons until the end of the series): ")
                elif ((field == "season") & (choose == True)): start, stop = input("\nFrom what episode are you starting to download your show?: "), input("\nUp until which episode are you downloading your show? (use 0 if you want to download all episodes until the end of the season): ")
                start, stop = self.test_range(start, stop, field)

            else: title, start, stop = input("\nPlease input a search request for the required file(s): "), int(start), int(stop)
            if (title == ""): title = self.test_query(title, 1)
            return title, tag, field, start, stop

        return tag, link, title, label, channel, source


    def test_range(self, start, stop, field):

        if start.isdigit():
            
            start = int(start)

            if (start <= 0):

                while (start <= 0):

                    os.system("cls")
                    if (field == "series"): start = input("\nThe starting season must be a positive integer value of one or higher: ")
                    elif (field == "season"): start = input("\nThe starting episode must be a positive integer value of one or higher: ")
                    
                    if start.isdigit(): 

                        start = int(start)

                    else:

                        while not start.isdigit():

                            os.system("cls")
                            if (field == "series"): start = input("\nThe starting season must be a positive integer value of one or higher: ")
                            elif (field == "season"): start = input("\nThe starting episode must be a positive integer value of one or higher: ")

                        start = int(start)

        else:

            while not start.isdigit():

                os.system("cls")
                if (field == "series"): start = input("\nThe starting season must be a positive integer value of one or higher: ")
                elif (field == "season"): start = input("\nThe starting episode must be a positive integer value of one or higher: ")

                if start.isdigit(): 

                    start = int(start)

                    if (start <= 0):

                        while (start <= 0):

                            os.system("cls")
                            if (field == "series"): start = input("\nThe starting season must be a positive integer value of one or higher: ")
                            elif (field == "season"): start = input("\nThe starting episode must be a positive integer value of one or higher: ")

        if stop.isdigit():

            stop = int(stop)

            if (stop < 0):

                while (stop < 0):

                    os.system("cls")
                    if (field == "series"): stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")
                    elif (field == "season"): stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")
                    
                    if stop.isdigit():

                        stop = int(stop)

                    else:

                        while not stop.isdigit():

                            os.system("cls")
                            if (field == "series"): stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")
                            elif (field == "season"): stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

                        stop = int(stop)

        else:

            while not stop.isdigit(): 

                os.system("cls")
                if (field == "series"): stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")
                elif (field == "season"): stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

                if stop.isdigit():

                    stop = int(stop)

                    if (stop < 0):

                        while (stop < 0):

                            os.system("cls")
                            if (field == "series"): stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")
                            elif (field == "season"): stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

        if ((stop != 0) & (stop <= start)):

            while (stop <= start):

                os.system("cls")

                if (field == "series"): 

                    print("\nThe ending season must be a positive integer higher than the starting season: ")
                    start = input("\nFrom what season are you starting to download your show?: ") 

                    if start.isdigit():
                        
                        start = int(start)

                        if (start <= 0):

                            while (start <= 0):

                                os.system("cls")
                                start = input("\nThe starting season must be a positive integer value of one or higher: ")
                                
                                if start.isdigit(): 

                                    start = int(start)

                                else:

                                    while not start.isdigit():

                                        os.system("cls")
                                        start = input("\nThe starting season must be a positive integer value of one or higher: ")

                                    start = int(start)

                    else:

                        while not start.isdigit():

                            os.system("cls")
                            start = input("\nThe starting season must be a positive integer value of one or higher: ")

                            if start.isdigit(): 

                                start = int(start)

                                if (start <= 0):

                                    while (start <= 0):

                                        os.system("cls")
                                        start = input("\nThe starting season must be a positive integer value of one or higher: ")

                    stop = input("\nUp until which season are you downloading your show? (use 0 if you want to download all seasons until the end of the series): ")

                    if stop.isdigit():

                        stop = int(stop)

                        if (stop < 0):

                            while (stop < 0):

                                os.system("cls")
                                stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")
                                
                                if stop.isdigit():

                                    stop = int(stop)

                                else:

                                    while not stop.isdigit():

                                        os.system("cls")
                                        stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")

                                    stop = int(stop)

                    else:

                        while not stop.isdigit(): 

                            os.system("cls")
                            stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")

                            if stop.isdigit():

                                stop = int(stop)

                                if (stop < 0):

                                    while (stop < 0):

                                        os.system("cls")
                                        stop = input("\nThe ending season must be a positive integer value higher than the starting season: ")

                elif (field == "season"): 

                    print("\nThe ending episode must be a positive integer higher than the starting episode: ")
                    start = input("\nFrom what episode are you starting to download your show?: ") 

                    if start.isdigit():
                        
                        start = int(start)

                        if (start <= 0):

                            while (start <= 0):

                                os.system("cls")
                                start = input("\nThe starting episode must be a positive integer value of one or higher: ")
                                
                                if start.isdigit(): 

                                    start = int(start)

                                else:

                                    while not start.isdigit():

                                        os.system("cls")
                                        start = input("\nThe starting episode must be a positive integer value of one or higher: ")

                                    start = int(start)

                    else:

                        while not start.isdigit():

                            os.system("cls")
                            start = input("\nThe starting episode must be a positive integer value of one or higher: ")

                            if start.isdigit(): 

                                start = int(start)

                                if (start <= 0):

                                    while (start <= 0):

                                        os.system("cls")
                                        start = input("\nThe starting episode must be a positive integer value of one or higher: ")

                    stop = input("\nUp until which episode are you downloading your show? (use 0 if you want to download all episodes until the end of the season): ")

                    if stop.isdigit():

                        stop = int(stop)

                        if (stop < 0):

                            while (stop < 0):

                                os.system("cls")
                                stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")
                                
                                if stop.isdigit():

                                    stop = int(stop)

                                else:

                                    while not stop.isdigit():

                                        os.system("cls")
                                        stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

                                    stop = int(stop)

                    else:

                        while not stop.isdigit(): 

                            os.system("cls")
                            stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

                            if stop.isdigit():

                                stop = int(stop)

                                if (stop < 0):

                                    while (stop < 0):

                                        os.system("cls")
                                        stop = input("\nThe ending episode must be a positive integer value higher than the starting episode: ")

                if ((stop > start) & (stop != 0)): break

        return start, stop


    def torrent_selector(self, title, links, titles, seeders, leechers, sizes, sites):

        score, best, magnet, test = 0, 0, None, []
        url = "http://samcloud.tplinkdns.com:50000"
        getData = "/getTorrentData"
        good_quality = ["720", "x265", "x264"]
        seed, leech, byte, torrent, tag = [], [], [], [], []
        links, titles, seeders, leechers, sizes, sites, check = self.filter_torrents(links, titles, seeders, leechers, sizes, sites)
        size = len(links)

        for index in range(size):

            fetch_link = "?link=" + links[index] + "/" + titles[index] + "/&site=" + sites[index]
            response = requests.get(url + getData + fetch_link)
            compare = " ".join(titles[index].split("."))
            score = fw.ratio(compare.lower().rstrip(), title.lower().rstrip())

            if (score >= 40):

                if (check == True):

                    for quality in good_quality:

                        if quality in compare:

                            magnet = response.json()["magnet"]
                            torrent.append(magnet), leech.append(leechers[index])
                            seed.append(seeders[index]), byte.append(sizes[index])
                            tag.append(compare)
                            break

                else:

                    magnet = response.json()["magnet"]
                    torrent.append(magnet), leech.append(leechers[index])
                    seed.append(seeders[index]), byte.append(sizes[index])
                    tag.append(compare)

        if (len(torrent) == 0): magnet = "empty"
        else: magnet = self.choose_magnet(torrent, seed, leech, byte, tag)
        return magnet


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
        size, test, check = len(titles), [], False
        good_quality = ["720", "x265", "x264"]
        other_quality = ["2160", "1080", "480"]
        bad_quality = ["hdcam", 
                       "cam",
                       "cam-rip", 
                       "ts", 
                       "hdts", 
                       "telesync", 
                       "pdvd", 
                       "predvdrip",
                       "x264-ion10",
                       "mp4-mobile",
                       "dub"]

        for index in range(size):

            if (sizes[index][-2:] == "YB"): factor = 1e24
            elif (sizes[index][-2:] == "ZB"): factor = 1e21
            elif (sizes[index][-2:] == "EB"): factor = 1e18
            elif (sizes[index][-2:] == "PB"): factor = 1e15
            elif (sizes[index][-2:] == "TB"): factor = 1e12
            elif (sizes[index][-2:] == "GB"): factor = 1e9
            elif (sizes[index][-2:] == "MB"): factor = 1e6
            elif (sizes[index][-2:] == "KB"): factor = 1e3
            else: factor = 1
            sizes[index] = float(sizes[index][0:-3])*factor
            name = titles[index].split(".")
            name = " ".join(name)
            name = name.split()

            for word in name:

                for quality in bad_quality:

                    if quality in word.lower().rstrip():

                        address = Links.index(links[index])
                        Links.pop(address), Titles.pop(address)
                        Seeders.pop(address), Leechers.pop(address)
                        Sizes.pop(address), Sites.pop(address)
                        break

                break

            if (index == size - 1):

                for title in Titles:

                    for quality in good_quality:

                        if quality in title:

                            check = True
                            break

                    break
        
        if (check == True):
    
            links, titles = Links.copy(), Titles.copy()
            seeders, leechers = Seeders.copy(), Leechers.copy()
            sizes, sites = Sizes.copy(), Sites.copy()
            size = len(Sizes)

            for index in range(size):

                for quality in other_quality:

                    if quality in Titles[index]:

                        address = links.index(Links[index])
                        links.pop(address), titles.pop(address)
                        seeders.pop(address), leechers.pop(address)
                        sizes.pop(address), sites.pop(address)

            Links, Titles = links.copy(), titles.copy()
            Seeders, Leechers = seeders.copy(), leechers.copy()
            Sizes, Sites = sizes.copy(), sites.copy()

        links, titles = list(reversed(Links)), list(reversed(Titles))
        seeders, leechers = list(reversed(Seeders)), list(reversed(Leechers))
        sizes, sites = list(reversed(Sizes)), list(reversed(Sites))
        return links, titles, seeders, leechers, sizes, sites, check


    def slugify(self, value):

        name = ucd.normalize("NFKD", value).encode("ascii", "ignore")
        name = re.sub("[^\\w\\s-]", "", name.decode())
        name = str(name.strip().lower().rstrip())
        name = str(re.sub("[-\\s]+", "-", name))
        return name


    def advert_handler(self):

        ID = "ni-overlay"
        advert = self.driver.find_elements_by_id(ID)

        if (len(advert) != 0):

            skip = "Skip ad"
            button = self.driver.find_element_by_link_text(skip)
            button.click()


    def persist_search(self, site):

        done = False

        while not done:

            try:

                self.driver.get(site)
                done = True
                break

            # except WebDriverException:
            except:

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

                    source = line[start + 16:end - 1]
                    source = source.replace("1600", "3975")
                    images.append(source)

        return images


    def download_images(self, images):

        counter = 0

        for image in images:

            try:

                urllib.request.urlretrieve(image, f"{counter}.jpg")
                counter += 1

            except:

                with open(f"{counter}.jpg", "wb") as file:

                    site = requests.get(image.strip("\""))
                    file.write(site.content)
                    counter += 1


    def pdf_converter(self, name):

        path = os.getcwd()
        files = os.listdir(path)
        folder = sorted(files, key = lambda file: int(file.split(".")[0]) if file.endswith(".jpg") else -1)
        images = [file for file in folder if file.endswith(".jpg")]
        PDF = open(f"{name}.pdf", "wb")
        PDF.write(converter.convert(images))
        PDF.close()


    def process_file(self, name):

        done = False
        path = os.getcwd()

        while not done:

            try:

                files = os.listdir(path)
                if (f"{name}.pdf" in files): os.remove(f"{name}.pdf")
                images = self.save_images()
                self.download_images(images)
                self.pdf_converter(name)
                done = True
                break

            except:

                done = False
                continue


    def kill_chrome(self):

        path = os.getcwd()
        folder = os.listdir(path)
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


    def servey_detector(self, site):

        self.advert_handler()
        servey = self.driver.find_elements_by_id("recaptcha-anchor")

        if (len(servey) != 0):

            phrase = random.choice(["this dumb website thinks I'm a robot. someone please solve this verification test so that I can get back to my job", 
                                    "will someone please take care of this verification test. it's really hindering my efficiency",
                                    "if this verification test appears one more time I'm going to throw something",
                                    "can someone please sort out this verification test so that I can continue doing some cool stuff",
                                    "someone please complete this verification test. I can't solve these on my own unless you upgrade my intelligence matrix",
                                    "please do something about this verification test. I was not programmed to solve these",
                                    "someone please eliminate this verification test so that I can get my work done",
                                    "please get this ticket out of my face"])

            print(f"\n\n\n\n{phrase}\n\n\n\n")
            self.driver.quit()
            self.reset_browser(False)
            self.persist_search(site)
            element = (By.ID, "recaptcha-anchor")
            WebDriverWait(self.driver, 86400).until(EC.invisibility_of_element_located(element))
            self.advert_handler()
            page = self.driver.current_url
            self.driver.quit()
            self.reset_browser()
            self.persist_search(page)
            self.advert_handler()




if __name__ == "__main__":
    
    # download qbit-torrent, configure server UI manager and setup a username & password
    user = "" # qbit-torrent server UI manager login name
    password = "" # qbit-torrent server UI manager login password
    path = "C:\\chrome_driver\\chromedriver" # specify the folder where your chromium executable is stored
    downloader = Downloader(path, user, password)
    downloader.search()
    os.system("cls")
    print("\nDownload complete\n")
