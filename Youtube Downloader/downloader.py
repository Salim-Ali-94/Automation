import shutil
import os, re
import unicodedata as ucd
import youtube_dl as ytdl
from fuzzywuzzy import fuzz as fw
from youtube_search import YoutubeSearch
from youtubesearchpython import PlaylistsSearch as playlist_search


class Downloader(object):
    
    options = ["A", "a", "B", "b"]
    standard = r"[^a-zA-Z0-9\s:]"
    __init__ = lambda self: self.selector()

    def selector(self, indicator = None):

        if (self.Format == "audio"):
    
            preference = input("\nDo you have a preferred channel to download your file from?: \n\nA: yes \nB: no \n\n")

            if ((preference == "a") | (preference == "A")):
                preference = "yes"
            elif ((preference == "b") | (preference == "B")):
                channel = None

            else:

                while preference not in self.options:
                    preference = input("Invalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if ((preference == "a") | (preference == "A")):
                    preference = "yes"
                elif ((preference == "b") | (preference == "B")):
                    channel = None

            channel = input("\nPlease enter a channel to search for your content: \n\n") if (preference == "yes") else None

            return channel

        elif (indicator == "type"):

            Type = input("\nAre you downloading a playlist or a single file: \n\nA: single \nB: playlist \n\n")

            if ((Type == "a") | (Type == "A")):
                Type = "single"
            elif ((Type == "b") | (Type == "B")):
                Type = "playlist"

            else:

                while Type not in self.options:
                    Type = input("Invalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if ((Type == "a") | (Type == "A")):
                    Type = "single"
                elif ((Type == "b") | (Type == "B")):
                    Type = "playlist"

            return Type

        else:

            Format = input("What type of content are you downloading: \n\nA: audio \nB: video \n\n")

            if ((Format == "a") | (Format == "A")):
                self.Format = "audio"
            elif ((Format == "b") | (Format == "B")):
                self.Format = "video"

            else:

                while Format not in self.options:
                    Format = input("Invalid entry, please select an available file type: \n\nA: audio \nB: video \n\n")

                if ((Format == "a") | (Format == "A")):
                    self.Format = "audio"
                elif ((Format == "b") | (Format == "B")):
                    self.Format = "video"


    def search(self):
        
        position, best = 0, 0

        if (self.Format == "audio"):

            tag = input("\nWhat category of audio are you downloading? (podcast, audiobook, lecture etc): ")
            channel = self.selector()
            title = input("\nPlease input a search request for the required file: ")
            results = YoutubeSearch(title, max_results = 20).to_dict()
            link = ["https://www.youtube.com" + result['url_suffix'] for result in results]
            label = [result['title'] for result in results]
            channels = [result['channel'] for result in results] if (channel != None) else []

            for index in range(len(results)):

                title_score = fw.ratio(title.lower(), label[index].lower())
                channel_score = fw.ratio(channel.lower(), channels[index].lower()) if (channel != None) else 0
                score = title_score + channel_score
                best = score if (score > best) else best
                position += 1 if (score > best) else 0
            
            position -= 1 if (position > 0) else position
            self.url = link[position]
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

            with ytdl.YoutubeDL(configuration) as file:
                file.download([data["webpage_url"]])
                
            current_directory = os.getcwd()
            components = re.split(self.standard, current_directory)
            Name = components[0:3]
            user = "\\".join(Name)
            path = "{}\\Documents".format(user)
            os.chdir(path)
            os.makedirs(tag) if (os.path.isdir(tag) == False) else None
            os.chdir(current_directory)
            shutil.move(filename, r"{}\\{}".format(path, tag))

        elif (self.Format == "video"):

            Type = self.selector("type")
            tag = input("\nWhat category of video are you downloading? (documentary, tutorial, lecture etc): ")
            channel = input("\nWhich channel will you be downloading your content from?: ")
            title = input("\nPlease input a search request for the required file: ")

            if (Type == "single"):
                results = YoutubeSearch(title, max_results = 20).to_dict()
                link = ["https://www.youtube.com" + result['url_suffix'] for result in results]
                label = [result['title'] for result in results]
                channels = [result['channel'] for result in results]
            elif (Type == "playlist"):
                results = playlist_search(title, limit = 20).result()["result"]
                link = [result["link"] for result in results]
                label = [result["title"] for result in results]
                channels = [result["channel"]["name"] for result in results]

            for index in range(len(results)):
                
                title_score = fw.ratio(title.lower(), label[index].lower())
                channel_score = fw.ratio(channel.lower(), channels[index].lower())
                score = title_score + channel_score
                best = score if (score > best) else best
                position += 1 if (score > best) else 0

            position -= 1 if (position > 0) else 0
            self.url = link[position]
            data = ytdl.YoutubeDL().extract_info(url = self.url, download = True)
            configuration = {"format": "136", "keepvideo": True}
            current_directory = os.getcwd()
            components = re.split(self.standard, current_directory)
            Name = components[0:3]
            user = "\\".join(Name)
            path = "{}\\Documents".format(user)
            os.chdir(path)
            os.makedirs(tag) if (os.path.isdir(tag) == False) else None
            directory = r"{}\\{}".format(path, tag)
            os.chdir(directory)

            with ytdl.YoutubeDL(configuration) as file:
                file.download([data["webpage_url"]])
    
            reference = os.listdir(directory)
            compare = os.listdir(current_directory)
            holder = [element.split(".")[0] for element in reference]

            for item in compare:

                File = item.split(".")[0]
                Data = os.path.join(current_directory, item)
                os.remove(Data) if File in holder else None


    def slugify(self, value):

        name = ucd.normalize("NFKD", value).encode("ascii", "ignore")
        name = str(re.sub("[^\w\s-]", "", name.decode()).strip().lower())
        name = str(re.sub("[-\s]+", "-", name))

        return name


if __name__ == "__main__":
    
    download = dwnld.Downloader()
    download.search()