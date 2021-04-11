import random
from time import ctime


# constants

name = "Olivia"
hour = int(ctime()[11:13])
blank = ["", None]
salutations = ["hello", "hey", "hi", "greetings", "hello there", "hi there", "hey there"]
error_message = ["an unexpected error has occured", "error encountered", "I've run into unforeseen problems", "unexpected problems encountered"]

LUT = {"first": 0,
	   "one": 0,
	   "1": 0,
	   "1st": 0,
	   "second": 1,
	   "two": 1,
	   "2": 1,
	   "2nd": 1,
	   "third": 2,
	   "three": 2,
	   "3": 2,
	   "3rd": 2,
	   "fourth": 3,
	   "four": 3,
	   "4": 3,
	   "4th": 3,
	   "fifth": 4,
	   "five": 4,
	   "5": 4,
	   "5th": 4,
	   "sixth": 5,
	   "six":5,
	   "6": 5,
	   "6th": 5,
	   "seventh": 6,
	   "seven": 6,
	   "7": 6,
	   "7th": 6,
	   "eighth": 7,
	   "eight": 7,
	   "8": 7,
	   "8th": 7,
	   "ninth": 8,
	   "nine": 8,
	   "9": 8,
	   "9th": 8,
	   "tenth": 9,
	   "ten": 9,
	   "10": 9,
	   "10th": 9,
	   "eleventh": 10,
	   "eleven": 10,
	   "11": 10,
	   "11th": 10,
	   "twelvth": 11,
	   "twelve": 11,
	   "12": 11,
	   "12th": 11,
	   "thirteenth": 12,
	   "thirteen": 12,
	   "13": 12,
	   "13th": 12,
	   "fourteenth": 13,
	   "fourteen": 13,
	   "14": 13,
	   "14th": 13,
	   "fifteenth": 14,
	   "fifteen": 14,
	   "15": 14,
	   "15th": 14,
	   "sixteenth": 15,
	   "sixteen": 15,
	   "16": 15,
	   "16th": 15,
	   "seventeenth": 16,
	   "seventeen": 16,
	   "17": 16,
	   "17th": 16,
	   "eighteenth": 17,
	   "eighteen": 17,
	   "18": 17,
	   "18th": 17,
	   "nineteenth": 18,
	   "nineteen": 18,
	   "19": 18,
	   "19th": 18,
	   "twentieth": 19,
	   "twenty": 19,
	   "20": 19,
	   "20th": 19}

# greetings

if ((hour >= 6) & (hour < 12)):
	greeting = "good morning"
elif ((hour >= 12) & (hour < 18)):
	greeting = "good afternoon"
elif ((hour >= 18) | (hour >= 0) & (hour < 6)):
	greeting = "good evening"

greet = lambda date_time, forecast: f"{greeting}. I'm {name}. your virtual assistant. today is {date_time}. the weather in your city is {forecast[0]} degrees celcius {weather_map[forecast[1]]}. I am now online. what can I do for you?"

# activation instructions

activate = ["hello",
	    "switch on",
	    "wake up",
	    "bring yourself back online",
	    f"wake up {name}",
	    f"{name} wake up",
	    f"hey {name}",
	    f"hello {name}"]

wake_response = [f"{random.choice(salutations)}. how can I help you?",
		 f"{random.choice(salutations)}. what can I do for you today?",
		 f"{random.choice(salutations)}. what can I do for you?",
		 f"{random.choice(salutations)}. how can I help you today?",
		 f"{random.choice(salutations)}. I am your digital assistant. {name}. I am now ready for instructions",
		 "what can I do for you today?",
		 "what can I do for you?",
		 "ready for instructions"]

# deactivation instructions

deactivate = [f"bye {name}",
	      f"leave now {name}"
	      "you can go now",
	      "shut down",
	      "turn off",
	      "switch off",
	      "deactivate",
	      "deactivate now",
	      "please deactivate now",
	      "please shut down now",
	      "please shutdown now",
	      "shutdown",
	      "go offline",
	      "you can shut down now"]

sleep_response = ["bye now",
		  "goodbye",
		  "okay. until next time",
		  "okay. until next time then",
		  "okay. shutting down now",
		  "okay. leaving now",
		  "okay. bye now",
		  "going offline",
		  "going offline now"]

# note instructions

note_ask = ["what should I record?", 
	    "what should I take down?", 
	    "what would you like me to note?", 
	    "what would you like me to take down?", 
	    "what would you like me to record?"]

note_command = ["take note",
		"take this down",
		"make a note",
		"write this down",
		"remember this",
		"take note please"
		"take this down please",
		"make a note please",
		"write this down please",
		"remember this please",
		"please make a note",
		"please write this down",
		"please take this down",
		"please remember this"]

note_response = ["this is what I have so far",
		 "here is what I have so far",
		 "here's what I have so far"]

remove_command = ["please remove x from the y list",
		  "please delete x from the y list",
		  "please erase x from the y list",
		  "please remove x from y list",
		  "please delete x from y list",
		  "please erase x from y list",
		  "remove x from the y list",
		  "delete x from the y list",
		  "erase x from the y list",
		  "remove x from y list",
		  "delete x from y list",
		  "erase x from y list",
		  f"{name} remove x from the y list",
		  f"{name} delete x from the y list",
		  f"{name} erase x from the y list",
		  f"{name} remove x from y list",
		  f"{name} delete x from y list",
		  f"{name} erase x from y list",
		  f"{name} please remove x from the y list",
		  f"{name} please delete x from the y list",
		  f"{name} please erase x from the y list",
		  f"{name} please remove x from y list",
		  f"{name} please delete x from y list",
		  f"{name} please erase x from y list"]

remove_command = [remove_command, list(set([phrase.split(" x ")[0] for phrase in remove_command]))]

remove_command[1].sort(key = lambda word: word.count(" "), reverse = True)

remove_response = lambda item, note = "grocery": random.choice([f"removed {item} from the {note} list",
								f"removed {item} from record",
								f"deleted {item} from the {note} list",
								f"deleted {item} from record",
								f"erased {item} from the {note} list",
								f"erased {item} from record"])

add_command = ["please add x to the y list",
	       "please add x to y list",
	       "please include x to the y list",
	       "please include x on the y list",
	       "please include x to y list",
	       "please include x on y list",
	       "add x to the y list",
	       "add x to y list",
	       "include x on y list",
	       "include x to y list"
	       "include x on the y list",
	       "include x to the y list"
	       "append x to y list",
	       "append x to the y list"
	       "please append x to y list",
	       "please append x to the y list",
	       f"{name} add x to the y list",
	       f"{name} add x to y list",
	       f"{name} please add x to the y list",
	       f"{name} please add x to y list",
	       f"{name} include x on y list",
	       f"{name} include x to y list",
	       f"{name} include x on the y list",
	       f"{name} include x to the y list",
	       f"{name} please include x on y list",
	       f"{name} please include x to y list",
	       f"{name} please include x on the y list",
	       f"{name} please include x to the y list",
	       f"{name} append x to y list",
	       f"{name} append x to the y list",
	       f"{name} please append x to y list",
	       f"{name} please append x to the y list"]

add_command = [add_command, list(set([phrase.split(" x ")[0] for phrase in add_command]))]

add_command[1].sort(key = lambda word: word.count(" "), reverse = True)

add_response = lambda item, note = "grocery": random.choice([f"added {item} to the {note} list",
							     f"added {item} to record",
							     f"saved {item} to the {note} list",
							     f"saved {item} to record",
							     f"included {item} on the {note} list",
							     f"included {item} on record"])

# YouTube search instructions

search_command = ["please search for x",
		  "please search x",
		  "search for x",
		  "search x",
		  f"{name} please search for x",
		  f"{name} please search x",
		  f"{name} search for x",
		  f"{name} search x"]

search_command = [search_command, list(set([phrase.split(" x")[0] for phrase in search_command]))]

search_command[1].sort(key = lambda word: word.count(" "), reverse = True)

search_response = lambda request: random.choice([f"here is what I found for {request}",
						 f"here are the results for {request}",
						 f"these are the videos I found for {request}",
						 f"searching YouTube for {request}"])

play_command = ["please play the x video",
		"play the x video",
		"play video x",
		"please play video x",
		f"{name} please play the x video",
		f"{name} play the x video",
		f"{name} please play video x",
		f"{name} play video x"]

play_command = [play_command, list(set([phrase.split(" x "  if " x " in phrase else " x")[0] for phrase in play_command]))]

play_command[1].sort(key = lambda word: word.count(" "), reverse = True)

play_response = ["here is the video you requested",
		 "opening your requested video",
		 "playing your video now",
		 "opening your video now"]

close_command = ["please close the browser",
		 "close the browser",
		 "close browser",
		 "please close browser",
		 "please close youtube",
		 "close youtube",
		 "exit from the browser",
		 "exit from browser",
		 "exit the browser",
		 "exit browser",
		 "please exit from the browser",
		 "please exit from browser",
		 "please exit the browser",
		 "please exit browser",
		 "exit youtube",
		 "exit from youtube",
		 "exit chrome",
		 "exit from chrome",
		 "please exit youtube",
		 "please exit from youtube",
		 "please exit from chrome",
		 "please exit chrome",
		 f"{name} please close the browser",
		 f"{name} close the browser",
		 f"{name} close browser",
		 f"{name} please close browser",
		 f"{name} please close youtube",
		 f"{name} close youtube",
		 f"{name} exit from the browser",
		 f"{name} exit from browser",
		 f"{name} exit the browser",
		 f"{name} exit browser",
		 f"{name} please exit from the browser",
		 f"{name} please exit from browser",
		 f"{name} please exit the browser",
		 f"{name} please exit browser",
		 f"{name} exit youtube",
		 f"{name} exit from youtube",
		 f"{name} exit from chrome",
		 f"{name} exit chrome",
		 f"{name} please exit youtube",
		 f"{name} please exit from youtube",
		 f"{name} please exit from chrome",
		 f"{name} please exit chrome"]

close_response = ["closing the browser",
		  "closing the browser now",
		  "shutting down chrome",
		  "shutting down the browser now",
		  "exiting from the browser now",
		  "exiting chrome now",
		  "exiting chrome",
		  "exiting from chrome now",
		  "exiting the browser now"
		  "leaving the internet now",
		  "exiting the browser now",
		  "exiting the browser",
		  "shutting down YouTube",
		  "exiting YouTube",
		  "closing YouTube",
		  "exiting YouTube now",
		  "closing YouTube now"]

# email instructions

email_command = ["please email x to me",
		 "email x to me",
		 "send me x",
		 "email x",
		 "please send me x",
		 "send x to me",
		 "please send x to me",
		 f"{name} please email x to me",
		 f"{name} email x to me",
		 f"{name} send me x",
		 f"{name} please send x to me",
		 f"{name} please send me x",
		 f"{name} send x to me",
		 f"{name} please send x to me"]

email_command = [email_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in email_command]))]

email_command[1].sort(key = lambda word: word.count(" "), reverse = True)

email_response = ["sending you your list now",
		  "sending email",
		  "sending email now",
		  "emailing the list to you",
		  "emailing the list to you now",
		  "sending the list to your email",
		  "sending the list to your email now",
		  "emailing your latest list to you now"]

# weather instructions

report = ["with clear skies",
	  "with partly cloudy skies",
	  "with scattered cover",
	  "with broken cover",
	  "with light rain",
	  "and rainy weather",
	  "with thunderstorms",
	  "with snowy weather",
	  "with mist cover",
	  "and the clouds are overcast",
	  "with light rain",
	  "with moderate rain",
	  "with intense rain",
	  "with heavy rain",
	  "with extreme rain",
	  "with freezing rain",
	  "with slight showers",
	  "with	showers",
	  "with intense showers",
	  "with ragged showers"]

weather_map = {"clear sky": report[0],
	       "few clouds": report[1],
	       "scattered clouds": report[2],
	       "broken clouds": report[3],
	       "shower rain": report[4],
	       "rain": report[5],
	       "thunderstorm": report[6],
	       "snow": report[7],
	       "mist": report[8],
	       "overcast clouds": report[9],
	       "light rain": report[10],
	       "moderate rain": report[11],
	       "heavy intensity rain": report[12],
	       "very heavy rain": report[13],
	       "extreme rain": report[14],
	       "freezing rain": report[15],
	       "light intensity shower rain": report[16],
	       "shower rain": report[17],
	       "heavy intensity shower rain": report[18],
	       "ragged shower rain": report[19]}

weather_command = ["what's the weather for today",
		   "how's the weather for today",
		   "what's the weather like",
		   "what's the weather like for today",
		   "what's today's forecast",
		   "how's the weather looking for today",
		   "how's the weather looking",
		   "what's the forecast for today"]

# audio instructions

audio_command = ["play audio",
		 "play media",
		 "play tracks",
		 "play the tracks",
		 "please play audio",
		 "please play media",
		 "please play tracks",
		 "please play the tracks",
		 f"{name} play audio",
		 f"{name} play media",
		 f"{name} play tracks",
		 f"{name} play the tracks",
		 f"{name} please play audio",
		 f"{name} please play media",
		 f"{name} please play tracks",
		 f"{name} please play the tracks"]

Next = ["skip track",
	"next track",
	"next audio",
	"skip",
	"next"]
			     
Stop = ["stop",
	"exit",
	"quit",
	"close"]
			     
Previous = ["previous",
	    "previous track",
	    "previous audio"]
			     
Up = ["volume up",
      "increase volume",
      "increase the volume",
      "louder",
      "louder please",
      "up"]

Down = ["volume down",
	"decrease volume",
	"decrease the volume",
	"reduce volume",
	"reduce the volume",
	"softer",
	"softer please",
	"down"]
		
Play = ["play",
	"resume",
	"continue"]

Pause = ["pause",
	 "pause media",
	 "pause audio",
	 "pause track"]

controls, control_audio = [Next, Previous, Stop, Pause, Play, Up, Down], []

for category in controls:
	for phrase in category:
		control_audio.append(phrase)

# videos instructions

video_command = ["please play x season y episode z",
		 "play x season y episode z",
		 "please open x season y episode z",
		 "open x season y episode z",
		 "start x season y episode z",
		 "please start x season y episode z",
		 "play x",
		 "please play x",
		 "open x",
		 "please open x",
		 "start x",
		 "please start x",
		 f"{name} please play x season y episode z",
		 f"{name} play x season y episode z",
		 f"{name} please open x season y episode z",
		 f"{name} open x season y episode z",
		 f"{name} start x season y episode z",
		 f"{name} please start x season y episode z",
		 f"{name} play x",
		 f"{name} please play x",
		 f"{name} open x",
		 f"{name} please open x",
		 f"{name} start x",
		 f"{name} please start x"]

video_command = [video_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in video_command]))]

video_command[1].sort(key = lambda word: word.count(" "), reverse = True)

empty_response = ["I don't recognize the file you are requesting", 
		  "it seems your requested file was incorrectly identified",
		  "I can't identify the file that you are requesting",
		  "I did not find any files matching your request",
		  "the file that you are requesting does not exist"]
