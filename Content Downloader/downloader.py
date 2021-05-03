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

                        
class Downloader(object):
    
    options = ["A", "a", "B", "b", "C", "c"]
    standard = r"[^a-zA-Z0-9\s:]"
    restrictions = ["?", "/", "\\", ":", "*", ">", "<", "|", "'", '"']
    
    def __init__(self, driver_path):

        self.selector(None)
        self.directory = driver_path
        self.reset_driver()


    def reset_driver(self, status = True):

        subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
        settings = webdriver.ChromeOptions()
        settings.headless = status
        path = os.getcwd()
        folder = os.listdir(path)

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
            Format = input("\nWhat type of content are you downloading: \n\nA: audio \nB: video \nC: comic book \n\n")

            if (Format.lower() == "a"):
                self.Format = "audio"

            elif (Format.lower() == "b"):
                self.Format = "video"

            elif (Format.lower() == "c"):
                self.Format = "comic book"

            else:

                while Format not in self.options:
                  
                    os.system("cls")
                    Format = input("\nInvalid entry, please select an available file type: \n\nA: audio \nB: video \nC: comic book \n\n")

                if (Format.lower() == "a"):
                    self.Format = "audio"

                elif (Format.lower() == "b"):
                    self.Format = "video"

                elif (Format.lower() == "c"):
                    self.Format = "comic book"

        elif (self.Format == "audio"):

            os.system("cls")
            preference = input("\nDo you have a preferred channel to download your file from?: \n\nA: yes \nB: no \n\n")

            if (preference.lower() == "a"):
                preference = "yes"

            elif (preference.lower() == "b"):
                channel = None

            else:

                while preference not in self.options[0:4]:
                    os.system("cls")
                    preference = input("\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if (preference.lower() == "a"):
                    preference = "yes"

                elif (preference.lower() == "b"):
                    channel = None

            os.system("cls")
            channel = input("\nPlease enter a channel to search for your content: ") if (preference == "yes") else None

            return channel

        elif (self.Format == "video"):

            os.system("cls")
            Type = input("\nAre you downloading a playlist or a single file: \n\nA: single video \nB: playlist \n\n")

            if (Type.lower() == "a"):
                Type = "single"

            elif (Type.lower() == "b"):
                Type = "playlist"

            else:

                while Type not in self.options[0:4]:
                  
                    os.system("cls")
                    Type = input("\nInvalid entry, please select an available option: \n\nA: single video \nB: playlist \n\n")

                if (Type.lower() == "a"):
                    Type = "single"

                elif (Type.lower() == "b"):
                    Type = "playlist"

            return Type

        elif (self.Format == "comic book"):

            os.system("cls")
            Type = input("\nAre you downloading an entire collection or only a single issue: \n\nA: single issue \nB: collection \n\n")

            if (Type.lower() == "a"):
                Type = "single"

            elif (Type.lower() == "b"):
                Type = "collection"

            else:

                while Type not in self.options[0:4]:
                  
                    os.system("cls")
                    Type = input("\nInvalid entry, please select an available option: \n\nA: single issue \nB: collection \n\n")

                if (Type.lower() == "a"):
                    Type = "single"

                elif (Type.lower() == "b"):
                    Type = "collection"

            return Type


    def search(self):
        
        if (self.Format == "audio"):

            tag, link, title, label, channel, source = self.extractor()
            self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = self.url, download = False)
            name = f"{data['title']}"
            name = self.slugify(name)
            File = f"{name}.%(ext)s"

            configuration = {"format": "bestaudio/best",
                             "keepvideo": False,
                             "outtmpl": File,
                             "postprocessors": [{"key": "FFmpegExtractAudio",
                                                 "preferredcodec": "mp3",
                                                 "preferredquality": "192"}]}

            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])
            File = File.split(".")[0] + ".mp3"
            self.directory_manager(tag, File)

        elif (self.Format == "video"):

            tag, link, title, label, channel, source = self.extractor()
            self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = self.url, download = True)
            configuration = {"format": "18", "keepvideo": True}
            current_directory, folder = self.directory_manager(tag)
            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])
            self.delete_copy(current_directory, folder)

        elif (self.Format == "comic book"):

            Type = self.selector()
            extensions = (".txt", ".jpg")
            URL = "https://readcomiconline.to/Search/Comic"
            os.system("cls")
            tag = input("\nWhich comic book series are you downloading? (Strange Tales, Secret Wars etc): ")
            status = [character for character in self.restrictions if character in tag]
            tag = self.test_query(tag, 0) if ((tag == "") | (status != [])) else tag
            os.system("cls")
            title = input("\nPlease input a search request for the required comic book(s): ")
            title = self.test_query(title, 1) if (title == "") else title
            self.directory_manager(tag)
            path = os.getcwd()
            folder = os.listdir(path)
            self.persist_search(URL)
            search = self.driver.find_element_by_tag_name("input")
            search.send_keys(title)
            search.send_keys(Keys.ENTER)
            self.servey_detector(self.driver.current_url)

            if (self.driver.current_url[-5:].lower() != "comic"):
                issues = self.driver.find_elements_by_tag_name("td a")

            else:

                site = self.driver.find_elements_by_tag_name("td a")
                comics = [comic.text for comic in site]
                channel, source = None, None
                self.link_selector(site, title, comics, channel, source)
                book = self.url.text
                click = self.driver.find_element_by_link_text(book)
                click.click()
                self.servey_detector(self.driver.current_url)
                issues = self.driver.find_elements_by_tag_name("td a")

            if (Type == "single"):

                os.system("cls")
                issues = list(reversed(issues))
                issue = input("\nWhich issue are you downloading from the selected comic book series?: ")

                if issue.isdigit():
                    issue = int(issue)

                else:

                    while not issue.isdigit():
                      
                        os.system("cls")
                        issue = input("\nInvalid entry, please specify an integer value for the selected comic book series: ")

                    issue = int(issue)

                click = self.driver.find_element_by_link_text(issues[issue - 1].text)
                click.click()
                self.servey_detector(self.driver.current_url)
                self.process_file(title, number)
                self.driver.quit()
                folder = os.listdir(path)

                for file in folder:

                    if file.endswith(extensions):
                        os.remove(file)

            else:
 
                webpage = self.driver.current_url
                size = len(issues)

                for index in range(size):

                    if f"{title} {index + 1}.pdf" not in folder:

                        self.servey_detector(self.driver.current_url)
                        issues = self.driver.find_elements_by_tag_name("td a")
                        issue = list(reversed(issues))[index]
                        click = self.driver.find_element_by_link_text(issue.text)
                        click.click()
                        self.servey_detector(self.driver.current_url)
                        self.process_file(title, index + 1)
                        self.persist_search(webpage)
                        folder = os.listdir(path)

                        for file in folder:

                            if file.endswith(extensions):
                                os.remove(file)

                self.driver.quit()


    def directory_manager(self, tag, file = None):

        current_directory = os.getcwd()
        component = re.split(self.standard, current_directory)
        name = component[0:3]
        user = "\\".join(name)
        path = f"{user}\\Documents"
        os.chdir(path)

        if (self.Format == "audio"):

            os.makedirs("Audio") if (os.path.isdir("Audio") == False) else None
            directory = f"{user}\\Documents\\Audio"
            os.chdir(directory)
            os.makedirs(tag) if (os.path.isdir(tag) == False) else None
            folder = f"{directory}\\{tag}"
            os.chdir(current_directory)

            if file not in os.listdir(folder):
                shutil.move(file, folder)

            else:

                while file in os.listdir(folder):

                    audio = file.split(".")[0]
                    audio += f" ({random.randint(0, 100)})"
                    audio += ".mp3"
                    file = audio

                os.rename(file, audio)
                shutil.move(audio, folder)

        elif (self.Format == "video"):

            os.makedirs("Video") if (os.path.isdir("Video") == False) else None
            directory = f"{user}\\Documents\\Video"
            os.chdir(directory)
            os.makedirs(tag) if (os.path.isdir(tag) == False) else None
            folder = f"{directory}\\{tag}"
            os.chdir(folder)

            return current_directory, folder

        elif (self.Format == "comic book"):

            os.makedirs("Comic Books") if (os.path.isdir("Comic Books") == False) else None
            directory = f"{user}\\Documents\\Comic Books"
            os.chdir(directory)
            os.makedirs(tag) if (os.path.isdir(tag) == False) else None
            folder = f"{directory}\\{tag}"
            os.chdir(folder)


    def delete_copy(self, current_directory, directory):

        reference = os.listdir(directory)
        compare = os.listdir(current_directory)
        holder = [element.split(".")[0] for element in reference]

        for item in compare:

            File = item.split(".")[0]
            Data = os.path.join(current_directory, item)
            os.remove(Data) if File in holder else None


    def link_selector(self, link, title, label, channel, source):

        position, best = 0, 0
        size = len(link)

        for index in range(size):
            
            title_score = fw.ratio(title.lower(), label[index].lower())
            channel_score = fw.ratio(channel.lower(), source[index].lower()) if (channel != None) else 0
            score = title_score + channel_score
            position = index if (score > best) else position
            best = score if (score > best) else best

        self.url = link[position]


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

        if (self.Format == "audio"):

            os.system("cls")
            tag = input("\nWhat category of audio are you downloading? (podcast, audiobook etc): ")
            status = [character for character in self.restrictions if character in tag]
            tag = self.test_query(tag, 0) if ((tag == "") | (status != [])) else tag
            channel = self.selector()
            os.system("cls")
            title = input("\nPlease input a search request for the required file: ")
            title = self.test_query(title, 1) if (title == "") else title
            result = YoutubeSearch(title, max_results = 20).to_dict()
            link = ["https://www.youtube.com" + entry['url_suffix'] for entry in result]
            label = [entry['title'] for entry in result]
            source = [entry['channel'] for entry in result] if (channel != None) else []

        elif (self.Format == "video"):

            Type = self.selector()
            os.system("cls")
            tag = input("\nWhat category of video are you downloading? (tutorial, lecture etc): ")
            status = [character for character in self.restrictions if character in tag]
            tag = self.test_query(tag, 0) if ((tag == "") | (status != [])) else tag
            os.system("cls")
            channel = input("\nWhich channel will you be downloading your content from?: ")
            channel = self.test_query(channel, 1) if (channel == "") else channel
            os.system("cls")
            title = input("\nPlease input a search request for the required file(s): ")
            title = self.test_query(title, 1) if (title == "") else title

            if (Type == "single"):

                result = YoutubeSearch(title, max_results = 20).to_dict()
                link = ["https://www.youtube.com" + entry['url_suffix'] for entry in result]
                label = [entry['title'] for entry in result]
                source = [entry['channel'] for entry in result]

            elif (Type == "playlist"):

                result = playlist_search(title, limit = 20).result()["result"]
                link = [entry["link"] for entry in result]
                label = [entry["title"] for entry in result]
                source = [entry["channel"]["name"] for entry in result]

        return tag, link, title, label, channel, source


    def slugify(self, value):

        name = ucd.normalize("NFKD", value).encode("ascii", "ignore")
        name = re.sub("[^\\w\\s-]", "", name.decode())
        name = str(name.strip().lower())
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

        status = False

        while not status:

            try:

                self.driver.get(site)
                status = True
                break

            except WebDriverException:

                time.sleep(2)
                status = False
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

                with open("{}.jpg".format(counter), "wb") as file:

                    site = requests.get(image.strip("\""))
                    file.write(site.content)
                    counter += 1


    def pdf_converter(self, name, number):

        path = os.getcwd()
        files = os.listdir(path)
        folder = sorted(files, key = lambda file: int(file.split(".")[0]) if file.endswith(".jpg") else -1)
        images = [file for file in folder if file.endswith(".jpg")]
        PDF = open("{} {}.pdf".format(name, number), "wb")
        PDF.write(converter.convert(images))
        PDF.close()


    def process_file(self, name, number):

        status = False
        path = os.getcwd()

        while not status:

            try:

                files = os.listdir(path)
                os.remove(f"{name} {number}.pdf") if (f"{name} {number}.pdf" in files) else None
                images = self.save_images()
                self.download_images(images)
                self.pdf_converter(name, number)
                status = True
                break

            except:

                status = False
                continue


    def kill_chrome(self):

        path = os.getcwd()
        folder = os.listdir(path)
        parent = psutil.Process(self.driver.service.process.pid)
        children = parent.children(recursive = True)

        if ("chrome_tabs.txt" in folder):
    
            with open("chrome_tabs.txt", "r") as file:
                ID = file.readlines()

            for pid in ID:

                try:
                    os.kill(int(pid.strip("\n")), signal.SIGTERM)
                except:
                    continue

        with open("chrome_tabs.txt", "w") as file:

            file.write(f"{self.driver.service.process.pid}")

            for child in children:

                file.write(f"\n{child.pid}")


    def servey_detector(self, site):

        self.advert_handler()
        servey = self.driver.find_elements_by_id("recaptcha-anchor")

        if (len(servey) != 0):

            phrase = random.choice(["this dumb website thinks I'm a robot. Someone please solve this verification test so that I can get back to my job", 
                                    "will someone please take care of this verification test. it's really hindering my efficiency",
                                    "if this verification test appears one more time I'm going to throw something",
                                    "please do something about this verification test. I was not programmed to solve these",
                                    "someone please eliminate this verification test so that I can get my work done",
                                    "please get this ticket out of my face"])

            print(f"\n\n\n\n{phrase}\n\n\n\n")
            self.driver.quit()
            self.reset_driver(False)
            self.persist_search(site)
            element = (By.ID, "recaptcha-anchor")
            WebDriverWait(self.driver, 86400).until(EC.invisibility_of_element_located(element))
            self.advert_handler()
            page = self.driver.current_url
            self.driver.quit()
            self.reset_driver()
            self.persist_search(page)
            self.advert_handler()




if __name__ == "__main__":
    
    path = "C:\\chrome_driver\\chromedriver"
    download = Downloader(path)
    download.search()
    os.system("cls")
    print("\nDownload complete\n")
