import speech_recognition as gSTT
import pyttsx3 as pTTS
import datetime
from time import ctime
import random
from constants import *
import os, re, sys
import webbrowser
import urllib.request
import subprocess
import smtplib
from email.message import EmailMessage
import requests
import vlc
import time
from pynput.keyboard import Key, Controller
import json
sys.stderr = open(os.devnull, "w")
from fuzzywuzzy import fuzz as fw
sys.stderr = sys.__stderr__
from youtube_search import YoutubeSearch


class Olivia(object):

	def __init__(self, city, key, sender, receiver, password):

		self.engine = pTTS.init()
		voice = self.engine.getProperty("voices")[9].id
		self.engine.setProperty("voice", voice)
		rate = self.engine.getProperty("rate")
		self.engine.setProperty("rate", rate - 50)
		self.reset_status()
		self.email("grocery")
		self.key = key
		self.city = city[0].upper() + city[1:].lower()
		self.sender = sender
		self.password = password
		self.receiver = receiver
		self.ticket = False
		self.flag = False


	def respond(self, text):

		self.engine.say(text)
		self.engine.runAndWait()


	def record(self):

		capture = gSTT.Recognizer()

		with gSTT.Microphone() as source:

			""" capture.adjust_for_ambient_noise(source) """
			audio = capture.listen(source)
			request = ""

			try:

				request = capture.recognize_google(audio)
				print(f"\n{name} heard you say:", request, "\n")
				self.interaction(request)

			except gSTT.UnknownValueError as error:

				reply = "Sorry, I didn't get that"
				error = str(error)
				reply = reply + ". Exception: " + error
				self.interaction(reply = reply)

				with open("unknown_value_error.txt", "w") as file:
					file.write(f"Exception: {error}\n")

			except gSTT.RequestError:

				reply = "Sorry, my speech service is down"
				self.respond(reply)
				self.interaction(request, reply)

			except Exception as error:

				reply = "an unexpected error has occured"
				error = str(error)
				reply = reply + ". Exception: " + error
				self.interaction(reply = reply)

				with open("unexpected_error.txt", "w") as file:
					file.write(f"Exception: {error}\n")

		return request.lower()


	def task(self, command):

		condition = None

		if "what's your name" in command:

			reply = random.choice(["My name is ", "I am ", "I'm "]) + name
			self.respond(reply)
			self.interaction(command, reply)
			condition = 1

		if "what's the time" in command:

			date_time = self.time_formatter()
			reply = "the current time is " + date_time
			self.respond(reply)
			self.interaction(command, reply)
			condition = 1

		if [phrase.lower() for phrase in weather_command if phrase.lower() in command]:

			forecast = self.get_weather()
			reply = f"the temperature is {forecast[0]} degrees celcius {weather_map[forecast[1]]}"
			self.respond(reply)
			self.interaction(command, reply)
			condition = 1

		if [phrase.lower() for phrase in note_command if phrase.lower() in command]:

			reply = random.choice(note_ask)
			self.respond(reply)
			self.interaction(command, reply)
			self.listen(0)
			condition = 1

		if [phrase.lower() for phrase in remove_command[1] if phrase.lower() in command]:

			item = self.parse(command, remove_command[0], 0)

			with open("grocery.txt", "r") as file: 
				groceries = file.readlines()

			if (item in [entry.strip("\n") for entry in groceries]):

				self.erase(item, "grocery")
				reply = remove_response(item)
				self.respond(reply)
				self.interaction(command, reply)
				condition = 1

			else:
				self.interaction(command)

		if [phrase.lower() for phrase in add_command[1] if phrase.lower() in command]:

			item = self.parse(command, add_command[0], 0)
			self.save("grocery", item)
			reply = add_response(item)
			self.respond(reply)
			self.interaction(command, reply)
			condition = 1

		if [phrase.lower() for phrase in search_command[1] if phrase.lower() in command]:

			request = self.parse(command, search_command[0], 1)
			self.search(request)
			reply = search_response(request)
			self.respond(reply)
			self.interaction(command, reply)
			condition = 1

		if [phrase.lower() for phrase in play_command[1] if phrase.lower() in command]:

			position = self.parse(command, play_command[0], 1)
			self.play_YouTube(LUT[position]) if ((position in LUT) & (self.ticket == True)) else None
			condition = 1

		if [phrase.lower() for phrase in email_command[1] if phrase.lower() in command]:

			reply = random.choice(email_response)
			self.respond(reply)
			self.send_email("grocery")
			self.interaction(command, reply)
			with open("email_status.txt", "w") as file: file.write("still busy....")
			condition = 1

		if [phrase.lower() for phrase in audio_command if phrase.lower() in command]:

			self.create_playlist()
			self.play_media()
			self.interaction(command)
			condition = 1

		if [phrase.lower() for phrase in control_audio if phrase.lower() in command]:

			if (self.flag == True):

				self.media_control(command)
				self.interaction(command)
				condition = 1

		if [phrase.lower() for phrase in video_command[1] if phrase.lower() in command]:

			title = self.parse(command, video_command[0], 2)
			directory = os.getcwd()

			if (title != None):

				video, folder = self.find_video(title)
				condition = 1

				if ((video != None) | (folder != None)):

					self.play_video(video, folder)
					self.interaction(command)
					os.chdir(directory)

				elif ((self.ticket == False) & (self.flag == False)):

					reply = random.choice(empty_response)
					self.respond(reply)
					self.interaction(command, reply)

		if [phrase.lower() for phrase in close_command if phrase.lower() in command]:

			if (self.ticket == True):

				reply = random.choice(close_response)
				self.respond(reply)

			self.close()
			self.interaction(command, reply if (self.ticket == True) else None)
			condition = 1

		if [phrase.lower() for phrase in deactivate if phrase.lower() in command]:

			reply = random.choice(sleep_response)
			self.respond(reply)
			self.interaction(command, reply)
			condition = 0

			return False, condition

		return True, condition


	def listen(self, indicator):

		done, audio = False, ""
		count, previous = 0, ""
		status = False

		while not done:

			audio = self.record()
			self.interaction(audio)
			print("Recording items....", "\n")

			if ((audio in blank) & (previous in blank)):
				count += 1

			else:

				item = audio
				self.save("grocery", item)
				count = 0
				status = True

			if (count >= 1):

				done = True
				break

			previous = audio

		if (status == True):

			self.remove_duplicate("grocery")
			path = os.getcwd()
			folder = os.listdir(path)

			if "grocery.txt" in folder:
	
				reply = random.choice(note_response)
				self.respond(reply)
				self.interaction(reply = reply)
				self.read("grocery")


	def parse(self, command, category, indicator):

		for sentence in category:

			first = sentence.split(" x " if " x " in sentence else " x")

			if first[0] in command:

				common = sentence.split()
				total = command.split()
				reduced = command.split()

				for word in total:

					if word in common:
						reduced.remove(word)

				if (indicator == 0):

					document = reduced[-1]
					reduced.pop()
					item = " ".join(reduced)
					return item

				elif (indicator == 1):

					request = " ".join(reduced)
					return request

				elif (indicator == 2):

					if (len(reduced) >= 3):

						episode = reduced[-1]
						season = reduced[-2]
						reduced.pop()
						reduced.pop()
						title = " ".join(reduced)
						return [title, season, episode]

					elif (len(reduced) != 0):

						title = " ".join(reduced)
						return [title, "x", "x"]

					else:
						return None


	def save(self, note, item):

		with open(f"{note}.txt", "a") as file:
			file.write(f"\n{item}\n")

		self.refactor(note)


	def erase(self, item, note):

		with open(f"{note}.txt", "r") as file:
			lines = file.readlines()

		with open(f"{note}.txt", "w") as file:

			for line in lines:

				if (line.strip("\n") != item):
					file.write(line)

		self.refactor(note)


	def interaction(self, command = None, reply = None):

		title = "transcript.txt"

		with open(title, "a") as file:

			date = datetime.datetime.now()
			instant = str(date)[0:16]
			file.write("You: {} ({})\n".format(command if (command not in blank) else "N/A", instant))
			file.write("{}: {} ({})\n".format(name, reply if (reply not in blank) else "N/A", instant))


	def read(self, note):

		with open(f"{note}.txt", "r") as file:

			items = [line for line in file]

		for item in items:

			self.respond(item)


	def refactor(self, note):

		with open(f"{note}.txt") as input_file, open(f"{note}_edit.txt", "w") as output_file:

			for line in input_file:

				if not line.strip(): continue
				output_file.write(line)

		os.remove(f"{note}.txt")
		os.rename(f"{note}_edit.txt", f"{note}.txt")


	def remove_duplicate(self, note):

		collection = []

		with open(f"{note}.txt", "r") as file:
			lines = file.readlines()

		with open(f"{note}.txt", "w") as file:

			for line in lines:

				if (line.strip("\n") not in collection):

					file.write(line)
					collection.append(line.strip("\n"))

		self.refactor(note)


	def search(self, request):

		proxy = "&sp=EgIQAQ%253D%253D"
		results = YoutubeSearch(request, max_results = 20).to_dict()
		url = "https://www.youtube.com/results?search_query=" + "+".join(request.split()) + proxy

		if (len(results) <= 2):

			html = urllib.request.urlopen(url)
			result = set()
			check = result.add
			videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
			results = [index for index in videos if not (index in result or check(index))]
			self.links = ["https://www.youtube.com" + entry for entry in results]

		else:
			self.links = ["https://www.youtube.com" + entry['url_suffix'] for entry in results]

		webbrowser.get().open_new(url)
		self.ticket = True


	def close(self):

		subprocess.run("taskkill /f /im chrome.exe", shell = True)		
		self.ticket = False


	def time_formatter(self):
		
		hour = int(ctime()[11:13])
		check = ctime()[8:9]

		if (hour > 11):
			append = "PM"
			if (hour > 12):
				hour -= 12
		else:
			append = "AM"
			if (hour == 0):
				hour = 12
		if (check == " "):
			date_time = ctime()[0:8] + ctime()[9:11]
		else:
			date_time = ctime()[0:11]
		if (hour < 10):
			date_time += "0" + str(hour) + ctime()[13:16]
		else:
			date_time += str(hour) + ctime()[13:16]

		date_time += append + ctime()[19:24]

		return date_time


	def email(self, note):

		check = ctime()[8:9]
		date_time = self.time_formatter()
		day = int(date_time[8:10]) if (check != " ") else int(date_time[8:9])
		path = os.getcwd()
		folder = os.listdir(path)
		with open("email_status.txt", "r") as file: status = file.readlines()
		status = status[0].strip("\n")

		if ((day >= 25) & (status != "sent")):

			self.send_email(note)

			if f"{note}.txt" in folder:
				os.remove(f"{note}.txt")

			if "transcript.txt" in folder:
				os.remove("transcript.txt")


	def send_email(self, note):

		subject = "Automated message"
		body = f"Here is your latest {note} list." + f"\n-{name}"
		message = EmailMessage()
		message["Subject"] = subject
		message["From"] = self.sender
		message["To"] = self.receiver
		message.set_content(body)

		with open(f"{note}.txt", "rb") as file:

			data = file.read()
			title = file.name

		message.add_attachment(data, maintype = "text", subtype = "txt", filename = title)

		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

			smtp.login(self.sender, self.password)
			smtp.send_message(message)

		with open("email_status.txt", "w") as file:
			file.write("sent")


	def reset_status(self):

		date_time = self.time_formatter()
		check = ctime()[8:9]
		day = int(date_time[8:10]) if (check != " ") else int(date_time[8:9])

		if ((day >= 1) & (day < 25)):

			with open("email_status.txt", "w") as file:
				file.write("still busy....")


	def get_weather(self):

		url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.key}&units=metric"
		data = requests.get(url).json()
		temperature = data["main"]["temp"]
		weather = data["weather"][0]["description"]
		forecast = [temperature, weather]

		return forecast


	def create_playlist(self):

		Name = self.root()
		user = "\\".join(Name)
		path = f"{user}\\Music"
		folder = os.listdir(path)
		random.shuffle(folder)

		with open("playlist.m3u", "w") as file:

			for item in folder:

				if item.endswith(".mp3"):
					file.write(f"file:///{path}\\{item}\n")


	def play_media(self):

		instance = vlc.Instance()
		player = instance.media_player_new()
		media = instance.media_new("playlist.m3u")
		media_list = instance.media_list_new(["playlist.m3u"])
		media.get_mrl()
		player.set_media(media)
		self.VLC = instance.media_list_player_new()
		self.VLC.set_media_list(media_list)
		self.VLC.play()
		self.flag = True


	def media_control(self, command):

		if [phrase.lower() for phrase in Next if phrase.lower() in command]:
			self.VLC.next()
		elif [phrase.lower() for phrase in Previous if phrase.lower() in command]:
			self.VLC.previous()
		elif [phrase.lower() for phrase in Pause if phrase.lower() in command]:
			self.VLC.pause()
		elif [phrase.lower() for phrase in Play if phrase.lower() in command]:
			self.VLC.play()
		elif [phrase.lower() for phrase in Up if phrase.lower() in command]:
			volume = self.VLC.get_media_player().audio_get_volume()
			self.VLC.get_media_player().audio_set_volume(volume + 10)
		elif [phrase.lower() for phrase in Down if phrase.lower() in command]:
			volume = self.VLC.get_media_player().audio_get_volume()
			self.VLC.get_media_player().audio_set_volume(volume - 10)
		elif [phrase.lower() for phrase in Stop if phrase.lower() in command]:
			self.VLC.stop()
			self.flag = False


	def play_video(self, video, directory):

		space = Key.space
		keyboard = Controller()
		os.chdir(directory)
		subprocess.Popen(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", "--fullscreen", video, '--key-pause="space"', "--qt-continue=2"], shell = True)
		time.sleep(20)
		keyboard.press(space)
		keyboard.release(space)


	def find_video(self, video):

		best, media, folder = 0, None, None
		pattern = r"[-_\;\,\.\+\% ]"
		Name = self.root()
		user = "\\".join(Name)
		path = f"{user}\\Videos"
		extensions = (".mp4", ".mkv", ".wav", ".avi", ".flv", ".mov", ".wmv", ".webm")
		item = video[0].lower()
		status = False
		size = len(video[0].split())

		if ((video[1] in LUT) | (video[2] in LUT)):

			if video[1] in LUT:

				video[1] = LUT[video[1]] + 1
				video[1] = str(video[1])

			if video[2] in LUT:

				video[2] = LUT[video[2]] + 1
				video[2] = str(video[2])

		if (video[1].isdigit() | video[2].isdigit()):

			if video[1].isdigit():
				S = int(video[1])

			if video[2].isdigit():
				E = int(video[2])

		if (video[1].isdigit() & video[2].isdigit()):
			status = True

		if status:

			if ((S < 10) & (E < 10)):
				item += " S0" + video[1] + "E0" + video[2]

			elif ((S < 10) & (E >= 10)):
				item += " S0" + video[1] + "E" + video[2]

			elif ((S >= 10) & (E < 10)):
				item += " S" + video[1] + "E0" + video[2]

			elif ((S >= 10) & (E >= 10)):
				item += " S" + video[1] + "E" + video[2]

			item = item.lower()

		for root, directory, files in os.walk(path):

			for file in files:

				if file.endswith(extensions):

					sections = re.split(pattern, file)
					File = [section for section in sections if section != ""]
					compare = " ".join(File)
					compare = compare.lower()
					check = compare.split()
					test = " ".join([phrase for phrase in check if phrase in item.split()])
					score = fw.ratio(item.lower(), test.lower())

					if (len(check) >= size):

						confirm = " ".join(check[0:size])

						if ((score > best) & (video[0].lower() == confirm)):

							media = file
							folder = root
							best = score

		if (best < 85):

			media = None
			folder = None

		return media, folder


	def play_YouTube(self, position):

		video = self.links[position]
		webbrowser.get().open(video)
		reply = random.choice(play_response)
		self.respond(reply)


	def root(self):

		standard = r"[^a-zA-Z0-9\s:]"
		current_directory = os.getcwd()
		component = re.split(standard, current_directory)
		Name = component[0:3]

		return Name




if __name__ == "__main__":

	city = "" # residing city of the user
	key = "" # get a free api key from the Open Weather Map website (subscribe)
	sender = "" # one email address to send the list from
	password = "" # password of the email used for the "sender" (above) 
	receiver = "" # another email address to receive the list
	enable, counter, condition = True, 0, 0
	agent = Olivia(city, key, sender, receiver, password)

	while enable:

		print("Offline....")
		speech = agent.record()

		if [phrase.lower() for phrase in activate if phrase.lower() in speech]:

			if (counter == 0):

				date_time = agent.time_formatter()
				forecast = agent.get_weather()
				initialize = greet(date_time, forecast)
				agent.respond(initialize)

			else:

				greeting = random.choice(wake_response)
				agent.respond(greeting)
 
			while enable:

				print("Listening....")
				instruction = agent.record()
				enable, condition = agent.task(instruction)

				if (condition == None):
					counter += 1

				else:
					counter = 1

				if (counter >= 20):

					enable = False
					counter = 1
					break

			enable = True
