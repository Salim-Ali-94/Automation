import shutil
import os, re, sys
import requests
import random
import warnings
import urllib.request
import unicodedata as ucd
import youtube_dl as ytdl
import img2pdf as converter
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as browser
sys.stderr = open(os.devnull, "w")
from fuzzywuzzy import fuzz as fw
sys.stderr = sys.__stderr__
from youtube_search import YoutubeSearch
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from youtubesearchpython import PlaylistsSearch as playlist_search


class Downloader(object):
    
    options = ["A", "a", "B", "b", "C", "c"]
    standard = r"[^a-zA-Z0-9\s:]"

    def __init__(self, driver_path):

        self.selector(None)
        settings = browser.ChromeOptions()
        settings.headless = True
        self.driver = browser.Chrome(executable_path = driver_path, options = settings)
        self.driver.implicitly_wait(30)


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
            os.system("cls")
            title = input("\nPlease input a search request for the required comic book(s): ")
            self.directory_manager(tag)
            path = os.getcwd()
            folder = os.listdir(path)
            self.driver.get(URL)
            search = self.driver.find_element_by_tag_name("input")
            search.send_keys(title)
            search.send_keys(Keys.ENTER)
            self.advert_handler()

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
                self.advert_handler()
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
                images = self.save_images()
                self.download_images(images)
                self.driver.quit()
                self.pdf_converter(title, number)
                folder = os.listdir(path)

                for file in folder:

                    if file.endswith(extensions):
                        os.remove(file)

            else:
 
                webpage = self.driver.current_url
                size = len(issues)

                for index in range(size):

                    if (f"{title} {index + 1}.pdf" not in folder):

                        self.advert_handler()
                        issues = self.driver.find_elements_by_tag_name("td a")
                        issue = list(reversed(issues))[index]
                        click = self.driver.find_element_by_link_text(issue.text)
                        click.click()
                        images = self.save_images()
                        self.download_images(images)
                        self.driver.get(webpage)
                        self.pdf_converter(title, index + 1)
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
        os.makedirs(tag) if (os.path.isdir(tag) == False) else None
        folder = f"{path}\\{tag}"

        if (self.Format == "audio"):

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
            os.chdir(folder)
            return current_directory, folder

        elif (self.Format == "comic book"):
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
            position += 1 if (score > best) else 0
            best = score if (score > best) else best

        position -= 1 if (position > 0) else 0
        self.url = link[position]


    def extractor(self):

        if (self.Format == "audio"):

            os.system("cls")
            tag = input("\nWhat category of audio are you downloading? (podcast, audiobook etc): ")
            channel = self.selector()
            os.system("cls")
            title = input("\nPlease input a search request for the required file: ")
            result = YoutubeSearch(title, max_results = 20).to_dict()
            link = ["https://www.youtube.com" + entry['url_suffix'] for entry in result]
            label = [entry['title'] for entry in result]
            source = [entry['channel'] for entry in result] if (channel != None) else []

        elif (self.Format == "video"):

            Type = self.selector()
            os.system("cls")
            tag = input("\nWhat category of video are you downloading? (tutorial, lecture etc): ")
            os.system("cls")
            channel = input("\nWhich channel will you be downloading your content from?: ")
            os.system("cls")
            title = input("\nPlease input a search request for the required file(s): ")

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

        advert = BeautifulSoup(self.driver.page_source, "html.parser")
        configuration = {"id": "ni-overlay"}
        Advert = advert.find_all("div", attrs = configuration)

        if (len(Advert) != 0):

            skip = "Skip ad"
            button = self.driver.find_element_by_link_text(skip)
            button.click()


    def save_images(self):

        options = self.driver.find_elements_by_tag_name("select")
        quality = self.driver.find_element_by_id("selectQuality")
        Quality = Select(quality)
        Quality.select_by_visible_text("High quality")
        page = self.driver.find_element_by_id("selectReadType")
        Page = Select(page)
        Page.select_by_visible_text("All pages")
        url = self.driver.current_url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        website = str(soup.prettify())
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

            urllib.request.urlretrieve(image, f"{counter}.jpg")
            counter += 1


    def pdf_converter(self, name, number):

        path = os.getcwd()
        files = os.listdir(path)
        folder = sorted(files, key = lambda file: int(file.split(".")[0]) if file.endswith(".jpg") else -1)
        images = [file for file in folder if file.endswith(".jpg")]
        PDF = open("{} {}.pdf".format(name, number), "wb")
        PDF.write(converter.convert(images))
        PDF.close()




if __name__ == "__main__":
    
    path = "C:\\chrome_driver\\chromedriver.exe"
    download = Downloader(path)
    download.search()
    os.system("cls")
    print("Download complete\n")
