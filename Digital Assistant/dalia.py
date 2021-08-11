import speech_recognition as gSTT
import pyttsx3 as pTTS
from num2words import num2words
from alpha_vantage.timeseries import TimeSeries
import datetime
from time import ctime
import random
import signal
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
sys.stderr = open(os.devnull, "w")
from fuzzywuzzy import fuzz as fw
sys.stderr = sys.__stderr__
from youtube_search import YoutubeSearch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard as kb
from covid import Covid
import shlex
from subprocess import DEVNULL, STDOUT
import psutil
from food_delivery import OrderFood
from word2number import w2n


class Dalia(OrderFood):

	def __init__(self, country, city, owm_key, sender, receiver, gmail_password, browser_path, qbit_admin, qbit_password, mrDFood_admin, mrDFood_password, stockMarket_key, currencyExchange_key):

		self.engine = pTTS.init()
		self.reference = os.getcwd()
		voices = [voice.name for voice in self.engine.getProperty("voices")]
		index = voices.index("Cortana")
		voice = self.engine.getProperty("voices")[index].id
		self.engine.setProperty("voice", voice)
		rate = self.engine.getProperty("rate")
		self.engine.setProperty("rate", rate - 50)
		self.stockMarket_key = stockMarket_key
		self.currencyExchange_key = currencyExchange_key
		self.owm_key = owm_key
		self.country = country.title()
		self.city = city.title()
		self.sender = sender
		self.gmail_password = gmail_password
		self.receiver = receiver
		self.ticket = False
		self.flag = False
		self.reset_status()
		self.email("grocery")
		super().__init__(browser_path, mrDFood_admin, mrDFood_password, qbit_admin, qbit_password, 1)


	def respond(self, text):

		self.engine.say(text)
		self.engine.runAndWait()


	def record(self):

		capture = gSTT.Recognizer()

		with gSTT.Microphone() as source:

			# capture.adjust_for_ambient_noise(source)
			audio = capture.listen(source)
			request = ""

			try:

				request = capture.recognize_google(audio)
				print(f"{name} heard you say:", request)
				correct = self.correction(request)

				if (correct.lower() != request.lower()):

					print(f"Corrected input speech to:", correct)
					request = correct
					
			except Exception as error:

				pass

		return request.lower()


	def task(self, command):

		condition = None

		if "what's your name" in command:

			reply = random.choice(pronoun) + name
			self.respond(reply)
			condition = 1

		if "what's the time" in command:

			date_time = self.time_formatter()
			reply = "the current time is " + date_time
			self.respond(reply)
			condition = 1

		if "what's the weather in" in command:

			city = command.split()[-1]
			forecast = self.weather(city)

			if (len(forecast) != 0):

				reply = f"the temperature in {city} is {forecast[0]} degrees celcius.... the pressure is {forecast[2]} and the humidity is {forecast[3]} {weather_map[forecast[1]]}"
				self.respond(reply)
				condition = 1

		if [phrase.lower() for phrase in download_command[1] if phrase.lower() in command]:

			if (command.lower().rstrip().lstrip().split()[-1] == "torrent"):

				try:

					self.category = "torrent"
					title, tag, field, initial, final = self.parse(command, torrentDownload_command[0])
					subprocess.Popen(["C:\\Program Files\\qBittorrent\\qbittorrent.exe"], shell = True)
					reply = random.choice(torrent_checking)
					self.respond(reply)
					super().search(title, tag, field, initial, final)
					reply = random.choice(torrent_response)
					self.respond(reply)
					condition = 1

				except Exception as E:

					print(E)

			elif ((command.lower().rstrip().lstrip().split()[-1] == "video") | (command.lower().rstrip().lstrip().split()[-1] == "audio")): 

				try:

					if (command.lower().rstrip().lstrip().split()[-1] == "video"): self.category = "video"
					elif (command.lower().rstrip().lstrip().split()[-1] == "audio"): self.category = "audio"
					reply = random.choice(youtube_checking)
					self.respond(reply)
					field, tag, title = self.parse(command, youtubeDownload_command[0])
					super().search(title, tag, field)
					reply = random.choice(youtube_checking)
					self.respond(reply)
					condition = 1

				except Exception as E:

					print(E)

			elif (command.lower().rstrip().lstrip().split()[-1] == "anime"):

				try:

					self.category = "animation"
					title, tag, field, initial, final = self.parse(command, animeDownload_command[0])
					reply = random.choice(anime_checking)
					self.respond(reply)
					super().search(title = title, tag = tag, field = field, initial = initial, final = final)
					reply = random.choice(anime_checking)
					self.respond(reply)
					condition = 1

				except Exception as E:

					print(E)

		if [phrase.lower() for phrase in weather_command if phrase.lower() in command]:

			forecast = self.weather()
			reply = f"the temperature is {forecast[0]} degrees celcius {weather_map[forecast[1]]}"
			self.respond(reply)
			condition = 1

		if [phrase.lower() for phrase in note_command if phrase.lower() in command]:

			reply = random.choice(note_ask)
			self.respond(reply)
			self.listen(0)
			condition = 1

		if [phrase.lower() for phrase in remove_command[1] if phrase.lower() in command]:

			item = self.parse(command, remove_command[0], 0)
			with open("grocery.txt", "r") as file: groceries = file.readlines()
			grocery_list = [entry.strip("\n") for entry in groceries]

			if item in grocery_list:

				self.erase(item, "grocery")
				reply = remove_response(item)
				self.respond(reply)
				condition = 1

		if [phrase.lower() for phrase in add_command[1] if phrase.lower() in command]:

			item = self.parse(command, add_command[0], 0)
			self.save("grocery", item)
			reply = add_response(item)
			self.respond(reply)
			condition = 1

		if [phrase.lower() for phrase in search_command[1] if phrase.lower() in command]:

			request = self.parse(command, search_command[0], 1)
			self.search(request)
			reply = search_response(request)
			self.respond(reply)
			condition = 1

		if [phrase.lower() for phrase in play_command[1] if phrase.lower() in command]:

			position = self.parse(command, play_command[0], 1)
			if ((position in LUT) & (self.ticket == True)): self.play_YouTube(LUT[position])
			condition = 1

		if [phrase.lower() for phrase in email_command[1] if phrase.lower() in command]:

			reply = random.choice(email_response)
			self.respond(reply)
			self.send_email("grocery")
			with open("email_status.txt", "w") as file: file.write("still busy....")
			condition = 1

		if [phrase.lower() for phrase in audio_command if phrase.lower() in command]:

			self.create_playlist()
			self.play_media()
			condition = 1

		if [phrase.lower() for phrase in control_audio if phrase.lower() in command]:

			if (self.flag == True):

				self.media_control(command)
				condition = 1

		if [phrase.lower() for phrase in video_command[1] if phrase.lower() in command]:

			title = self.parse(command, video_command[0], 2)
			directory = os.getcwd()

			if (title != None):

				video, folder = self.find_video(title)
				condition = 1

				if ((video != None) | (folder != None)):

					self.play_video(video, folder)
					os.chdir(directory)

				elif ((self.ticket == False) & (self.flag == False)):

					reply = random.choice(empty_response)
					self.respond(reply)

		if [phrase.lower() for phrase in close_command if phrase.lower() in command]:

			if (self.ticket == True):

				reply = random.choice(close_response)
				self.respond(reply)

			self.close()
			condition = 1

		if [phrase.lower() for phrase in read_command[1] if phrase.lower() in command]:

			path = os.getcwd()
			folder = os.listdir(path)
			groceries = []
			empty = ["", " ", "\n"]

			if "grocery.txt" in folder:

				with open("grocery.txt", "r") as file:

					groceries = [line for line in file]
					groceries = [grocery.strip() for grocery in groceries if grocery.strip() not in empty]
					size = len(groceries)

				if (size == 0):

					reply = noItem_response()
					self.respond(reply)

				else:

					reply = read_response()
					self.respond(reply)
					self.read("grocery")

			else: 

				reply = noFile_response()
				self.respond(reply)

			condition = 1

		if [phrase.lower() for phrase in news_command if phrase.lower() in command]:

			reply = random.choice(news_checking)
			self.respond(reply)
			headlines, articles = self.news()
			reply = random.choice(news_response)
			self.respond(reply)
			self.read(headlines)
			self.dictate(articles)
			condition = 1

		if [phrase.lower() for phrase in covid_command if phrase.lower() in command]:

			(amount, reply) = self.covid_information(command)
			if (amount != None): self.respond(reply)
			condition = 1

		if [phrase.lower() for phrase in deactivate if phrase.lower() in command]:

			reply = random.choice(sleep_response)
			self.respond(reply)
			condition = 0

			return False, condition

		return True, condition


	def correction(self, audio):

		if (audio.split()[0].lower() == "and"):
			audio = audio.split()
			audio[0] = "add"
			audio = " ".join(audio)
		elif ("i love you" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("i love you", name)
		elif ("love you" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("love you", name)
		elif ("onivia" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("onivia", name)
		elif ("all of you" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("all of you", name)
		elif ("golfland" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("golfland", "go offline")
		elif ("glock 9" in audio.lower()):
			audio = audio.lower()
			audio = audio.replace("glock 9", "go offline")
		return audio


	def listen(self, indicator):

		done, audio = False, ""
		count, previous = 0, ""
		status = False
		print("Recording items....", "\n")

		while not done:

			audio = self.record()
			if ((audio in blank) & (previous in blank)): count += 1

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
				self.read("grocery")


	def parse(self, command, category, indicator = None):

		best, phrase = 0, ""

		for sentence in category:

			score = fw.ratio(sentence.lower(), command.lower())
			if (score > best): phrase, best = sentence, score

		common, total, reduced = phrase.split(), command.split(), command.split()
		for word in total: reduced.remove(word) if word in common else None

		if (indicator == 0):

			if (" y " in phrase):

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
				reduced.pop(), reduced.pop()
				title = " ".join(reduced)
				return [title, season, episode]

			elif (len(reduced) > 0):

				title = " ".join(reduced)
				return [title, "x", "x"]

			else:

				return None

		elif (command.split()[-1] == "torrent"):

			if (("from episode" in command.lower()) & ("until episode" in command.lower())):

				S = ""
				tag = "series"
				field = "season"
				final = reduced[-1]
				initial = reduced[-2]
				season = reduced[-3]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				if (final.isdigit() == False): final = str(w2n.word_to_num(final))
				if (int(season) < 10): S = "0"
				title = " ".join(reduced[0:-3])
				search = title.rstrip().lstrip() + " S" + S + season
				initial, final = self.test_order(initial, final)

			elif (("from season" in command.lower()) & ("until season" in command.lower())):

				tag = "series"
				field = "series"
				final = reduced[-1]
				initial = reduced[-2]
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				if (final.isdigit() == False): final = str(w2n.word_to_num(final))
				title = " ".join(reduced[0:-2])
				search = title.rstrip().lstrip()
				initial, final = self.test_order(initial, final)

			elif (("from episode" in command.lower()) & ("until episode" not in command.lower())):

				S = ""
				tag = "series"
				field = "season"
				final = "0"
				initial = reduced[-1]
				season = reduced[-2]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				if (int(season) < 10): S = "0"
				title = " ".join(reduced[0:-2])
				search = title.rstrip().lstrip() + " S" + S + season
				initial = str(abs(int(initial)))

			elif (("from season" in command.lower()) & ("until season" not in command.lower())):

				tag = "series"
				field = "series"
				final = "0"
				initial = reduced[-1]
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				title = " ".join(reduced[0:-1])
				search = title.rstrip().lstrip()
				initial = str(abs(int(initial)))

			elif (("episode" in command.lower()) & ("season" in command.lower())):

				tag = "series"
				initial, final = "1", "0"
				field = "episode"
				S, E = "", ""
				episode = reduced[-1]
				season = reduced[-2]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (episode.isdigit() == False): episode = str(w2n.word_to_num(episode))
				if (int(season) < 10): S = "0"
				if (int(episode) < 10): E = "0"
				title = " ".join(reduced[0:-2])
				search = title.rstrip().lstrip() + " S" + S + season + "E" + E + episode

			elif (("episode" not in command.lower()) & ("season" in command.lower())):

				S = ""
				tag = "series"
				initial, final = "1", "0"
				field = "season"
				season = reduced[-1]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (int(season) < 10): S = "0"
				title = " ".join(reduced[0:-1])
				search = title.rstrip().lstrip() + " S" + S + season

			elif (("episode" not in command.lower()) & ("season" not in command.lower()) & ("series" in command.lower())):

				S = ""
				tag = "series"
				initial, final = "1", "0"
				field = "series"
				title = " ".join(reduced)
				search = title.lower().rstrip().lstrip()

			elif (("episode" not in command.lower()) & ("season" not in command.lower())):

				if ("movie" in command.lower()): tag = "movie"
				else: tag = "other"
				field = tag
				initial, final = "1", "0"
				title = " ".join(reduced)
				search = title.lower().rstrip().lstrip()

			return [search], tag, [field], [initial], [final]

		elif (command.split()[-1] == "anime"):

			if (("from episode" in command.lower()) & ("until episode" in command.lower())):

				tag = "series"
				field = "season"
				final = reduced[-1]
				initial = reduced[-2]
				season = reduced[-3]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				if (final.isdigit() == False): final = str(w2n.word_to_num(final))
				title = " ".join(reduced[0:-3])
				search = title.lower().rstrip().lstrip() + " season " + season
				initial, final = self.test_order(initial, final)

			elif (("from season" in command.lower()) & ("until season" in command.lower())):

				tag = "series"
				field = "series"
				final = reduced[-1]
				initial = reduced[-2]
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				if (final.isdigit() == False): final = str(w2n.word_to_num(final))
				title = " ".join(reduced[0:-2])
				search = title.lower().rstrip().lstrip()
				initial, final = self.test_order(initial, final)

			elif (("from episode" in command.lower()) & ("until episode" not in command.lower())):

				tag = "series"
				field = "season"
				final = "0"
				initial = reduced[-1]
				season = reduced[-2]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				title = " ".join(reduced[0:-2])
				search = title.lower().rstrip().lstrip() + " season " + season
				initial = str(abs(int(initial)))

			elif (("from season" in command.lower()) & ("until season" not in command.lower())):

				tag = "series"
				field = "series"
				final = "0"
				initial = reduced[-1]
				if (initial.isdigit() == False): initial = str(w2n.word_to_num(initial))
				title = " ".join(reduced[0:-1])
				search = title.lower().rstrip().lstrip()
				initial = str(abs(int(initial)))

			elif (("episode" in command.lower()) & ("season" in command.lower())):

				tag = "series"
				initial, final = None, None
				field = "episode"
				episode = reduced[-1]
				season = reduced[-2]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				if (episode.isdigit() == False): episode = str(w2n.word_to_num(episode))
				title = " ".join(reduced[0:-2])
				search = title.lower().rstrip().lstrip() + " season " + season + " episode " + episode

			elif (("episode" not in command.lower()) & ("season" in command.lower())):

				tag = "series"
				initial, final = "1", "0"
				field = "season"
				season = reduced[-1]
				if (season.isdigit() == False): season = str(w2n.word_to_num(season))
				title = " ".join(reduced[0:-1])
				search = title.lower().rstrip().lstrip() + " season " + season

			elif (("episode" not in command.lower()) & ("season" not in command.lower()) & ("series" in command.lower())):

				tag = "series"
				initial, final = "1", "0"
				field = "series"
				title = " ".join(reduced)
				search = title.lower().rstrip().lstrip()

			elif (("episode" not in command.lower()) & ("season" not in command.lower()) & ("everything" in command.lower())):

				tag = "series"
				initial, final = None, None
				field = "series"
				title = " ".join(reduced)
				search = title.lower().rstrip().lstrip()

			elif (("episode" not in command.lower()) & ("season" not in command.lower())):

				if ("movie" in command.lower()): tag = "movie"
				else: tag = "other"
				field = tag
				initial, final = "1", "0"
				title = " ".join(reduced)
				search = title.lower().rstrip().lstrip()

			return search, tag, field, initial, final

		elif ((command.split()[-1] == "video") | (command.split()[-1] == "audio") | (command.split()[-2:] == "video playlist") | (command.split()[-2:] == "audio playlist")):

			if (command.split()[-1] == "video"): tag = f"{name}-downloaded videos"
			elif (command.split()[-1] == "audio"): tag = f"{name}-downloaded mp3s"
			elif (command.split()[-2:] == "video playlist"): tag = f"{name}-downloaded video playlists"
			elif (command.split()[-2:] == "audio playlist"): tag = f"{name}-downloaded audio playlists"
			if (command.split()[-1] == "playlist"): field = "playlist"
			else: field = "single"
			title = " ".join(reduced)
			return field, tag, title


	def test_order(self, initial, final):

		if ((int(initial) < 0) | (int(final) < 0)):

			final = abs(int(final))
			initial = abs(int(initial))

		if ((final != "0") & (int(final) < int(initial))):

			placeholder = initial
			final = initial
			initial = placeholder

		elif (int(final) == int(initial)):

			final = int(initial) + 1
			initial = initial

		return str(initial), str(final)


	def save(self, note, item):

		with open(f"{note}.txt", "a") as file: file.write(f"\n{item}\n")
		self.refactor(note)


	def erase(self, item, note):

		with open(f"{note}.txt", "r") as file: lines = file.readlines()

		with open(f"{note}.txt", "w") as file:

			for line in lines:

				if (line.strip("\n") != item): file.write(line)

		self.refactor(note)


	def read(self, text, indicator = None):

		if (type(text) == str):
			with open(f"{text}.txt", "r") as file: items = [line for line in file]
		elif (type(text) == list):
			items = [f"{index + 1}.... " + text[index] if indicator == None else text[index] for index in range(len(text))]
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
		with open(f"{note}.txt", "r") as file: lines = file.readlines()

		with open(f"{note}.txt", "w") as file:

			for line in lines:

				if (line.strip("\n") not in collection):

					file.write(line)
					collection.append(line.strip("\n"))

		self.refactor(note)


	def search(self, request):

		portal = "&sp=EgIQAQ%253D%253D"
		results = YoutubeSearch(request, max_results = 20).to_dict()
		url = "https://www.youtube.com/results?search_query=" + "+".join(request.split()) + portal

		if (len(results) <= 2):

			html = urllib.request.urlopen(url)
			result = set()
			check = result.add
			videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
			results = [index for index in videos if not (index in result or check(index))]
			self.links = ["https://www.youtube.com" + entry for entry in results]

		else: self.links = ["https://www.youtube.com" + entry['url_suffix'] for entry in results]
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
			if f"{note}.txt" in folder: os.remove(f"{note}.txt")


	def send_email(self, note):

		subject = "Automated message"
		body = f"Here is your latest {note} list." + f"\n-{name}"
		message = EmailMessage()
		message["Subject"] = subject
		message["From"] = self.sender
		message["To"] = self.receiver
		message.set_content(body)
		with open(f"{note}.txt", "rb") as file: data, title = file.read(), file.name
		message.add_attachment(data, maintype = "text", subtype = "txt", filename = title)
		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: smtp.login(self.sender, self.gmail_password), smtp.send_message(message)
		with open("email_status.txt", "w") as file: file.write("sent")


	def reset_status(self):

		date_time = self.time_formatter()
		check = ctime()[8:9]
		day = int(date_time[8:10]) if (check != " ") else int(date_time[8:9])

		if (((day >= 1) & (day < 25)) | ("email_status.txt" not in os.listdir(os.getcwd()))):

			with open("email_status.txt", "w") as file: file.write("still busy....")

		if "grocery.txt" not in os.listdir(os.getcwd()):

			with open("grocery.txt", "w") as file: file.write("")


	def weather(self, city = None):

		if (city == None): url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.owm_key}&units=metric"
		else: url = f"http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&appid={self.owm_key}&units=metric"

		try:
			
			data = requests.get(url).json()
			if (city == None): temperature = data["main"]["temp"]
			else: temperature, pressure, humidity = data["main"]["temp"], data["main"]["pressure"], data["main"]["humidity"]
			weather = data["weather"][0]["description"]
			if (city == None): forecast = [temperature, weather]
			else: forecast = [temperature, weather, pressure, humidity]

		except:

			forecast = []

		return forecast


	def create_playlist(self):

		Name = self.root()
		user = "\\".join(Name)
		path = f"{user}\\Media"
		folder = os.listdir(path)
		random.shuffle(folder)

		with open("playlist.m3u", "w") as file:

			for item in folder:

				if item.endswith(".mp3"): file.write(f"file:///{path}\\{item}\n")


	def play_media(self):

		instance = vlc.Instance()
		player = instance.media_player_new()
		media = instance.media_new("playlist.m3u")
		media_list = instance.media_list_new(["playlist.m3u"])
		media.get_mrl()
		player.set_media(media)
		self.VLC = instance.media_list_player_new()
		self.VLC.set_media_list(media_list)
		self.VLC.get_media_player().audio_set_volume(40)
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
		elif [phrase.lower() for phrase in Volume[1] if phrase.lower() in command]:
			volume = command.split()[-1]
			volume = " ".join(re.split(", |-|\n", volume))
			volume = int(w2n.word_to_num(volume)) if volume in number else None
			if (volume != None): self.VLC.get_media_player().audio_set_volume(volume)
		elif [phrase.lower() for phrase in Stop if phrase.lower() in command]:
			self.VLC.stop()
			self.flag = False


	def play_video(self, video, directory):

		os.chdir(directory)
		subprocess.Popen(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", "--fullscreen", video, "--qt-continue=2"], shell = True)
		self.press_key(30, Key.space)
		for index in range(2): self.press_key(0.25, Key.left)
		for index in range(40): self.press_key(0.25, Key.down)
		for index in range(8): self.press_key(0.25, Key.up)


	def press_key(self, delay, key):

		time.sleep(delay)
		Controller().press(key)
		Controller().release(key)


	def find_video(self, video):

		best, media, folder = 0, None, None
		pattern = r"[-_\;\,\.\+\% ]"
		Name = self.root()
		user = "\\".join(Name)
		paths = [f"{user}\\Videos", f"{user}\\Documents\\TORRENTS", f"{user}\\Documents\\animation"]
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

		for path in paths:
			
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


	def covid_information(self, command = None):

		cvd = Covid()
		countries = cvd.list_countries()
		countries = [country["name"].lower() for country in countries]
		if (command != None): return self.test_covid(command, countries)
		local_cases = cvd.get_status_by_country_name(self.country)
		local_active = local_cases["active"]
		local_confirmed = local_cases["confirmed"]
		local_recovered = local_cases["recovered"]
		local_deaths = local_cases["deaths"]
		global_active = cvd.get_total_active_cases()
		global_confirmed = cvd.get_total_confirmed_cases()
		global_recovered = cvd.get_total_recovered()
		global_deaths = cvd.get_total_deaths()
		data = [local_active, local_confirmed, local_recovered, local_deaths, global_active, global_confirmed, global_recovered, global_deaths]
		return data


	def test_covid(self, command, countries):

		country, amount = None, None
		reply = None
		cvd = Covid()

		if [phrase.lower() for phrase in covidInform_command[1] if phrase.lower() in command]:

			country = command.split()[-1]
			if country in countries: amount = cvd.get_status_by_country_name(country)["confirmed"]
			if country in countries: reply = covid_response(country, amount)

		if [phrase.lower() for phrase in covidHighest_command if phrase.lower() in command]:

			confirmed = [cvd.get_status_by_country_name(area)["confirmed"] for area in countries]
			amount = max(confirmed)
			index = confirmed.index(amount)
			country = countries[index]
			reply = covidHighest_response(country, amount)

		if [phrase.lower() for phrase in covidLowest_command if phrase.lower() in command]:

			confirmed = [cvd.get_status_by_country_name(area)["confirmed"] for area in countries]
			amount = min(confirmed)
			index = confirmed.index(amount)
			country = countries[index]
			reply = covidLowest_response(country, amount)

		return amount, reply


	def news(self):

		url = "https://news.yahoo.com"
		super().persist_search(self, url)
		webpage = self.driver.current_url
		headlines = "h3 a.js-content-viewer"
		articles = self.driver.find_elements_by_css_selector(headlines)
		links = [article.get_attribute("href") for article in articles]
		titles = [item.text for item in articles]
		content = "div.caas-body p"
		counter, collection, reports = 0, [], []
		trash = ["More stories from",
			 "[MUSIC",
			 "Like this article",
			 "Get more from",
			 "Cover photo thumbnail",
			 "Editor's note",
			 "Photo:",
			 "Featured Image via GoFundMe",
			 "[NO AUDIO]",
			 "More from Axios",
			 "Subscribe for free",
			 "Read the original article",
			 "This article is republished",
			 "It was written by",
			 "receives funding from",
			 "Originally Appeared on",
			 "https://",
			 "http://",
			 "Sign up to get"]

		first_check = trash.copy()
		for item in ["https://", "http://", "Featured Image via GoFundMe"]: first_check.remove(item)
		for item in ["(Reporting by", "reported from", "This story originally appeared", "More from"]: first_check.append(item) 
		second_check = first_check.copy()
		for item in ["https://", "http://", "Featured Image via GoFundMe", "Photo by", "Read the full", "Associated Press writers", "This story has been updated to correct", "Here's what he had to say", "Here's what she had to say"]: second_check.append(item)

		for link in links:

			super().persist_search(self, link)
			self.driver.execute_script("var heading = document.getElementsByTagName('strong'); for (var index = heading.length - 1; index >= 0; index--) {heading[index].parentNode.removeChild(heading[index]);}")
			self.driver.execute_script("var element = document.getElementsByTagName('li'); for (var index = element.length - 1; index >= 0; index--) {element[index].parentNode.removeChild(element[index]);}")
			self.driver.execute_script("var extra = document.getElementsByTagName('button'); for (var index = extra.length - 1; index >= 0; index--) {extra[index].parentNode.removeChild(extra[index]);}")
			paragraphs = self.driver.find_elements_by_css_selector(content)
			text = [paragraph.get_attribute("textContent") for paragraph in paragraphs]
			text = self.filter_article(text, first_check)
			text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', " ".join(text))
			sentences = text.copy()
			text = self.filter_article(text, second_check)
			text = shlex.split(" ".join(text), posix = False)
			collect = self.quote_seperator(text)
			for character in collect: collection.append(character.rstrip())
			collection = self.filter_article(collection, trash)
			passage = collection.copy()
			collection = []

			if (len(sentences) > 1):

				report = " ".join(passage)
				report.replace("_", " ")
				reports.append(report)
				if (len(reports) >= 5): break

		return titles[0:5], reports


	def filter_article(self, parent, dilute):

		child = parent.copy()

		for item in parent:

			for element in dilute:

				if element.lower() in item.lower():

					if item in child: 

						child.remove(item)

		return child


	def quote_seperator(self, paragraphs):

		collect, connect, counter = [], "", 0

		for sentence in paragraphs:

			if (((sentence[0] == '"') & (sentence[-1] == '"')) | ((sentence[0] == "'") & (sentence[-1] == "'")) | ((sentence[0] == "“") & (sentence[-1] == "”"))):

				collect.append(connect)
				collect.append(sentence)
				counter += 1

			else:

				if (sentence == "."): connect += sentence
				else: connect += sentence + " "

			if (counter%2 != 0):

				connect = ""
				counter = 0

			if (sentence == paragraphs[-1]): 

				collect.append(connect)

		return collect


	def dictate(self, articles):

		done, audio = False, ""
		status, count = False, 0

		while not done:

			audio = self.record()
			if (audio in blank): count += 1
			elif [phrase.lower() for phrase in dictate_command[1] if phrase.lower() in audio]: status, done = True, True
			if (count >= 4): done = True

		if (status == True):

			position = self.parse(audio, dictate_command[0], 1)

			if position in LUT:

				address = LUT[position]
				article = articles[address]
				self.respond(article)


	def check_keyboard(self):

		if kb.is_pressed("home"):

			self.VLC.pause()
			instruction = self.record()
			enable, condition = self.task(instruction)
			if (self.flag == True): self.VLC.play()

		return enable, condition


	def stock_prices(self):

		interval = TimeSeries(key = self.stockMarket_key, output_format = "json")
		prices, stock_price = [], []

		for stock in stocks:

			data = interval.get_intraday(symbol = stock, interval = "1min", outputsize = "compact")
			latest = next(iter(data[0]))
			price = data[0][latest]["1. open"]
			prices.append(price)

		open_amount = [round(float(price), 2) for price in prices]
		duplicate = open_amount.copy()

		for index in range(5):

			amount = max(open_amount)
			address = duplicate.index(amount)
			company = stocks[address]
			address = open_amount.index(amount)
			pair = (company, amount)
			stock_price.append(pair)
			open_amount.pop(address)

		return stock_price


	def convert_currency(self):

		rates, factor, amount = [], {}, 1
		url = f"http://data.fixer.io/api/latest?access_key={self.currencyExchange_key}"
		response = requests.get(url)
		data = response.json()
		factor = data["rates"]

		for currency in currencies[1:]:

			if (currency != "EUR"): amount = amount / factor[currency]
			if (currencies[0] == "EUR"): rate = str(round(amount, 2))
			else: rate = str(round(amount*factor[currencies[0]], 2))
			cash = rate.split(".")
			if (cash[-1] == "0"): rate = cash[0]
			else: rate = ".".join(cash) 
			pair = (currency, rate)
			rates.append(pair)

		return rates




if __name__ == "__main__":

	# download qbit-torrent, configure server UI manager and setup a username & password
	qbit_admin = "" # qbit-torrent server UI manager login name
	qbit_password = "" # qbit-torrent server UI manager login password
	city = "" # current residing city of the user
	country = "" # current residing country of the user
	owm_key = "" # sign up and get a free api key from the Open Weather Map website (user account required)
	fixer_key = "" # sign up and get a free api key from the Fixer.IO (user account required)
	alphaVantage_key = "" # sign up and get a free api key from the Alpha Vantage website (user account required)
	mrDFood_admin = "" # Mr D Food account email
	mrDFood_password = "" # Mr D Food account password
	sender = "" # one email address to send the list from
	gmail_password = "" # password of the email used for the "sender" (above)
	receiver = "" # another email address to receive the list
	path = os.getcwd() + "\\chromedriver" # keep the chromium executable in the same folder as this program
	enable, counter, condition = True, -1, 0
	agent = Dalia(country, city, owm_key, sender, receiver, gmail_password, path, qbit_admin, qbit_password, mrDFood_admin, mrDFood_password, alphaVantage_key, fixer_key)
	kb.add_hotkey("end", lambda: kb.press_and_release("ctrl+c"))
	os.system("cls"), print()

	try:

		while enable:

			print("Offline (press the home button to activate or the end button to quit)....")
			kb.wait("home")

			if (counter == -1):

				date_time = agent.time_formatter()
				forecast, covid_update = [str(0), "rain"], [str(0)]*8
				exchange_rates, market_prices = [("EUR", str(0))]*3, [("TSLA", str(0))]*5
				if (value == 0): forecast = agent.weather()
				elif (value == 1): covid_update = agent.covid_information()
				elif (value == 2): exchange_rates = agent.convert_currency()
				elif (value == 3): market_prices = agent.stock_prices()
				initialize = greet(country, date_time, forecast, covid_update, exchange_rates, market_prices)
				agent.respond(initialize)

			else:

				greeting = random.choice(wake_response)
				agent.respond(greeting)

			try:

				print("Listening (press the end button to deactivate)....")
		
				while enable:

					if (agent.flag != True): instruction = agent.record()
					if (agent.flag != True): enable, condition = agent.task(instruction)
					else: enable, condition = agent.check_keyboard()
					if (condition == None): counter += 1
					else: counter = 0
					if (counter >= 20): enable, counter = False, 0

			except KeyboardInterrupt:
				
				bye = random.choice(sleep_response)
				agent.respond(bye)
				counter = 0

			enable = True

	except KeyboardInterrupt:

		try: agent.driver.quit()
		except: pass
