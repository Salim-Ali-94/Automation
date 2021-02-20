import shutil
import os, re
import requests
import unicodedata as ucd
import youtube_dl as ytdl
import img2pdf as converter
from bs4 import BeautifulSoup
from selenium import webdriver
from fuzzywuzzy import fuzz as fw
from youtube_search import YoutubeSearch
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from youtubesearchpython import PlaylistsSearch as playlist_search


class Downloader(object):
    
    options = ["A", "a", "B", "b", "C", "c"]
    standard = r"[^a-zA-Z0-9\s:]"

    def __init__(self, driver_folder):

        self.selector(None)
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path = driver_folder, options = options)
        self.driver.implicitly_wait(30)


    def selector(self, indicator = 0):

        if (indicator == None):

            Format = input("What type of content are you downloading: \n\nA: audio \nB: video \nC: comic book \n\n")

            if Format in self.options[0:2]:
                self.Format = "audio"
            elif Format in self.options[2:4]:
                self.Format = "video"
            elif Format in self.options[4:6]:
                self.Format = "comic book"

            else:

                while Format not in self.options:
                    Format = input("Invalid entry, please select an available file type: \n\nA: audio \nB: video \nC: comic book \n\n")

                if Format in self.options[0:2]:
                    self.Format = "audio"
                elif Format in self.options[2:4]:
                    self.Format = "video"
                elif Format in self.options[4:6]:
                    self.Format = "comic book"

        elif (self.Format == "audio"):
    
            preference = input("\nDo you have a preferred channel to download your file from?: \n\nA: yes \nB: no \n\n")

            if preference in self.options[0:2]:
                preference = "yes"
            elif preference in self.options[2:4]:
                channel = None

            else:

                while preference not in self.options[0:4]:
                    preference = input("Invalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if preference in self.options[0:2]:
                    preference = "yes"
                elif preference in self.options[2:4]:
                    channel = None

            channel = input("\nPlease enter a channel to search for your content: \n\n") if (preference == "yes") else None

            return channel

        elif (self.Format == "video"):

            Type = input("\nAre you downloading a playlist or a single file: \n\nA: single video \nB: playlist \n\n")

            if Type in self.options[0:2]:
                Type = "single"
            elif Type in self.options[2:4]:
                Type = "playlist"

            else:

                while Type not in self.options[0:4]:
                    Type = input("Invalid entry, please select an available option: \n\nA: single video \nB: playlist \n\n")

                if Type in self.options[0:2]:
                    Type = "single"
                elif Type in self.options[2:4]:
                    Type = "playlist"

            return Type

        elif (self.Format == "comic book"):

            Type = input("\nAre you downloading an entire collection or only a single issue: \n\nA: single issue \nB: collection \n\n")

            if Type in self.options[0:2]:
                Type = "single"
            elif Type in self.options[2:4]:
                Type = "collection"

            else:

                while Type not in self.options[0:4]:
                    Type = input("Invalid entry, please select an available option: \n\nA: single issue \nB: collection \n\n")

                if Type in self.options[0:2]:
                    Type = "single"
                elif Type in self.options[2:4]:
                    Type = "collection"

            return Type


    def search(self):
        
        if (self.Format == "audio"):

            tag, link, title, label, channel, source = self.extractor()
            self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = self.url, download = False)
            name = f"{data['title']}"
            name = self.slugify(name)
            filename = f"{name}.mp3"
            configuration = {"format": "bestaudio/best",
                             "keepvideo": False,
                             "outtmpl": filename,
                             "postprocessors": [{"key": "FFmpegExtractAudio",
                                                 "preferredcodec": "mp3",
                                                 "preferredquality": "192"}]}
            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])
            self.directory_manager(tag, filename)

        elif (self.Format == "video"):

            tag, link, title, label, channel, source = self.extractor()
            self.link_selector(link, title, label, channel, source)
            data = ytdl.YoutubeDL().extract_info(url = self.url, download = True)
            configuration = {"format": "18", "keepvideo": True}
            current_directory, directory = self.directory_manager(tag)
            with ytdl.YoutubeDL(configuration) as file: file.download([data["webpage_url"]])
            self.delete_copy(current_directory, directory)

        elif (self.Format == "comic book"):

            Type = self.selector()
            URL = "https://readcomiconline.to/Search/Comic"
            tag = input("\nWhich comic book series are you downloading? (Civil War, Suprior Iron-Man, Avengers etc): ")
            title = input("\nPlease input a search request for the required comic book(s): ")
            self.driver.get(URL)
            search = self.driver.find_element_by_tag_name("input")
            search.send_keys(title)
            search.send_keys(Keys.ENTER)
            self.advert_handler()
            comics = self.driver.find_elements_by_tag_name("td")
            site = [comic.text for comic in comics]
            channel, source = None, None
            self.link_selector(comics, title, site, channel, source)
            book = self.url.text
            click = self.driver.find_element_by_link_text(book)
            click.click()
            self.advert_handler()
            issues = self.driver.find_elements_by_tag_name("td a")
            issues = list(reversed(issues))
            self.directory_manager(tag)

            if (Type == "single"):

                number = int(input("\nWhich issue are you downloading from the selected comic book series?: "))

                if (type(number) != int):
                    while (type(number) != int):
                        number = int(input("\nInvalid entry, please specify/input an integer value for the selected comic book series?: "))

                click = self.driver.find_element_by_link_text(issues[number - 1].text)
                click.click()
                images = self.save_images()
                self.download_images(images)
                self.driver.quit()
                self.pdf_converter(title, number)
                path = os.getcwd()

                for file in os.listdir(path):
                    if (file.endswith(".jpg") | file.endswith(".txt")):
                        os.remove(file)

            elif (Type == "collection"):
 
                webpage = self.driver.current_url
                size, count = len(issues), 1

                for index in range(size):

                    issues = self.driver.find_elements_by_tag_name("td a")
                    issue = list(reversed(issues))[index]
                    click = self.driver.find_element_by_link_text(issue.text)
                    click.click()
                    images = self.save_images()
                    self.download_images(images)
                    self.driver.get(webpage)
                    self.advert_handler()
                    self.pdf_converter(title, count)
                    path = os.getcwd()
                    count += 1

                    for file in os.listdir(path):
                        if (file.endswith(".jpg") | file.endswith(".txt")):
                            os.remove(file)

                self.driver.quit()
                    

    def directory_manager(self, tag, filename = None):

        current_directory = os.getcwd()
        component = re.split(self.standard, current_directory)
        Name = component[0:3]
        user = "\\".join(Name)
        path = "{}\\Documents".format(user)
        os.chdir(path)
        os.makedirs(tag) if (os.path.isdir(tag) == False) else None
        directory = "{}\\{}".format(path, tag)

        if (self.Format == "audio"):
            os.chdir(current_directory)
            shutil.move(filename, directory)
        elif (self.Format == "video"):
            os.chdir(directory)
            return current_directory, directory
        elif (self.Format == "comic book"):
            os.chdir(directory)


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

            tag = input("\nWhat category of audio are you downloading? (podcast, audiobook etc): ")
            channel = self.selector()
            title = input("\nPlease input a search request for the required file: ")
            result = YoutubeSearch(title, max_results = 20).to_dict()
            link = ["https://www.youtube.com" + result['url_suffix'] for result in result]
            label = [entry['title'] for entry in result]
            source = [entry['channel'] for entry in result] if (channel != None) else []

        elif (self.Format == "video"):

            Type = self.selector()
            tag = input("\nWhat category of video are you downloading? (documentary, tutorial, lecture etc): ")
            channel = input("\nWhich channel will you be downloading your content from?: ")
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
        name = str(re.sub("[^\\w\\s-]", "", name.decode()).strip().lower())
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

        with open("comicbooks_site.txt", "w+") as file:

            file.write(website)
            file.seek(0)

            for line in file:

                start = line.find("lstImages.push(")
                end = line.find(");")

                if (start != -1):

                    src = line[start + 15:end]
                    images.append(src)

        return images


    def download_images(self, images):

        counter = 0

        for image in images:

            with open("{}.jpg".format(counter), "wb") as file:

                site = requests.get(image.strip("\""))
                file.write(site.content)
                counter += 1


    def pdf_converter(self, name, number):

        path = os.getcwd()
        files = os.listdir(path)
        folder = sorted(files, key = lambda file: int(file.split(".")[0]) if file.endswith(".jpg") else -1)
        pictures = [file for file in folder if file.endswith(".jpg")]
        PDF = open("{} {}.pdf".format(name, number), "wb")
        PDF.write(converter.convert(pictures))
        PDF.close()




if __name__ == "__main__":
    
    path = "C:\\chrome_driver\\chromedriver"
    download = Downloader(path)
    download.search()