import random
from num2words import num2words
from time import ctime
import re


# constants

name = "Dalia"
city = "polokwaanee"
hour = int(ctime()[11:13])
blank = ["", None]
pronoun = ["i'm", "i am", "my name is"]
help_question = ["how can i help you today?", "how may i help you today?", "what can I do for you today?", "how may i assist you today?", "how can i help you?", "how may i help you?", "what can I do for you?", "how may i assist you?"]
conclusion = ["i am now ready for instructions", "i am now online", "i will now be listening for commands", "initialization process complete", "vocal protocols are now enabled", "succesfully established communication protocols"]
prefixes = ["today is", "the date is", f"the current time in {city} is", f"the current time in your city is", "the current date is"]
variable = list(range(4))
value = random.choice(variable)

salutations = ["greetings", 
			   "hello there", 
			   "hi there", 
			   "hey there"]

error_message = ["an unexpected error has occured", 
				 "error encountered", 
				 "i've run into unforeseen problems", 
				 "unexpected problems encountered"]

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

numbers = [" ".join(re.split(", |-|\n", num2words(number))) for number in range(201)]
number = {numbers[index]: index for index in range(201)}
for index in range(201): number[f"{index}"] = index

if ((hour >= 6) & (hour < 12)):
	greeting = "good morning"
elif ((hour >= 12) & (hour < 18)):
	greeting = "good afternoon"
elif ((hour >= 18) | (hour >= 0) & (hour < 6)):
	greeting = "good evening"


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
				 f"{random.choice(salutations)}. I am your digital assistant. I am now ready for instructions",
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
			  "please deactivate now",
			  "please shut down now",
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
				  "remove x from the list",
				  "delete x from the list",
				  "erase x from the list",
				  "please remove x from the list",
				  "please delete x from the list",
				  "please erase x from the list",
				  f"{name} remove x from the list",
				  f"{name} delete x from the list",
				  f"{name} erase x from the list",
				  f"{name} please remove x from the list",
				  f"{name} please delete x from the list",
				  f"{name} please erase x from the list",
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
			   "add x to the list",
			   "include x on the list",
			   "append x to the list",
			   "please add x to the list",
			   "please include x on the list",
			   "please append x to the list",
			   f"{name} add x to the list",
			   f"{name} include x on the list",
			   f"{name} append x to the list",
			   f"{name} please add x to the list",
			   f"{name} please include x on the list",
			   f"{name} please append x to the list",
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

read_command = ["please read the x list",
			    "please read x list",
			    "please read out x list",
			    "please read out the x list",
			    "what's in the x list",
			    "read the x list",
			    "read out the x list",
			    "read out x list",
			    "read x list",
				f"{name} please read the x list",
			    f"{name} please read x list",
			    f"{name} please read out x list",
			    f"{name} please read out the x list",
			    f"{name} what's in the x list",
			    f"{name} read the x list",
			    f"{name} read out the x list",
			    f"{name} read out x list",
			    f"{name} read x list"]

read_command = [read_command, list(set([phrase.split(" x ")[0] for phrase in read_command]))]

read_command[1].sort(key = lambda word: word.count(" "), reverse = True)

read_response = lambda note = "grocery": random.choice([f"here are the items in the {note} list",
				   							  			f"the {note} list has the following items",
			  	   							  			f"i have recorded the following items in the {note} list",
			  	   							  			f"the {note} list currently contains the following items"])

noFile_response = lambda note = "grocery": random.choice(["the requested file does not exist",
				   							  			  "there is no such file in the root directory",
			  	   							  			  f"a list with the name of {note} is not present in this folder",
			  	   							  			  f"the {note} list is not created yet",
			  	   							  			  f"the {note} list has not yet been initialized at present"])

noItem_response = lambda note = "grocery": random.choice(["the requested list is empty",
			  	   							  			  "this list currently has no items recorded in it",
				   							  			  f"the {note} list is empty",
			  	   							  			  f"there are no items in the {note} list yet",
			  	   							  			  f"the {note} list is currently empty"])


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


# music instructions

audio_command = ["play music",
				 "play songs",
				 "play tunes",
				 "play the tracks",
				 "please play music",
				 "please play songs",
				 "please play tunes",
				 "please play the tracks",
				 f"{name} play music",
				 f"{name} play songs",
				 f"{name} play tunes",
				 f"{name} play the tracks",
				 f"{name} please play music",
				 f"{name} please play songs",
				 f"{name} please play tunes",
				 f"{name} please play the tracks"]

Next = ["skip track",
		"next track",
		"next song",
		"skip",
		"next"]
			     
Stop = ["stop",
		"exit",
		"quit",
		"close"]
			     
Previous = ["previous",
			"previous track",
			"previous song"]
			     
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
		"down",
		"lower"]

Volume = ["volume x",
		  "set volume to x",
		  "set the volume to x",
		  "please set the volume to x"
		  f"{name} set the volume to x",
		  f"{name} please set the volume to x"]
		
Play = ["play",
		"resume",
		"continue"]

Pause = ["pause",
		 "pause music",
		 "pause song",
		 "pause track"]

Volume = [Volume, list(set([phrase.split(" x")[0] for phrase in Volume]))]

Volume[1].sort(key = lambda word: word.count(" "), reverse = True)

# controls, control_audio = [Next, Previous, Stop, Pause, Play, Up, Down, Volume[0], Volume[1]], []
controls, control_audio = [Next, Previous, Stop, Pause, Play, Up, Down, Volume[0]], []

for category in controls:
	for phrase in category: control_audio.append(phrase)


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


# captcha variables

captcha_response = ["this dumb website thinks I'm a robot. someone please solve this verification test so that I can get back to my job", 
				  	"will someone please take care of this verification test. it's really hindering my efficiency",
				  	"if this verification test appears one more time I'm going to throw something",
				  	"can someone please sort out this verification test so that I can continue doing some cool shit",
				  	"someone please complete this verification test. I can't solve these on my own unless you upgrade my intelligence matrix",
				  	"please do something about this verification test. I was not programmed to solve these",
				  	"someone please eliminate this verification test so that I can get my work done",
				  	"someone please eradicate this verification test. you should really consider upgrading my conciousness to an AI",
				  	"this verification test is at it again. if you made me an AI we wouldn't keep running into this problem",
				  	"please get this ticket out of my face"]


# news instructions

news_command = ["give me the news",
				"what's the latest news",
				"what are the latest headlines",
				"what are the headlines for today",
				"give me the latest news",
				"give me the current news",
				"what's the current news",
				"please give me the latest news",
				"please give me the current news",
				"please give me the news",
				f"{name} please give me the latest news",
				f"{name} please give me the current news",
				f"{name} please give me the news",
				f"{name} give me the news",
				f"{name} what's the latest news",
				f"{name} what are the latest headlines",
				f"{name} what are the headlines for today",
				f"{name} give me the latest news",
				f"{name} give me the current news"
				f"{name} what's the current news"]

dictate_command = ["please read the x article",
				   "read the x article",
				   "read article x",
				   "please read article x",
				   f"{name} please read the x article",
				   f"{name} read the x article",
				   f"{name} please read article x",
				   f"{name} read article x"]

dictate_command = [dictate_command, list(set([phrase.split(" x"  if " x" in phrase else " x ")[0] for phrase in dictate_command]))]

dictate_command[1].sort(key = lambda word: word.count(" "), reverse = True)

news_response = ["here is a list of all the articles available on yahoo news",
				 "here are the latest news headlines from yahoo",
				 "here is a list of the news articles I found on yahoo",
				 "here is a list of the news articles I managed to collect from yahoo",
				 "here is a list of the news articles I managed to curate from yahoo",
				 "here are the top stories from yahoo news",
				 "here are the current news extracts from yahoo"]

news_checking = ["scanning yahoo database for relevant news information",
				 "checking yahoo for latest news updates",
				 "collecting the top stories from yahoo news",
				 "searching yahoo news and parsing collected articles for grammar correction",
				 "serching top headlines from yahoo now",
				 "searching news articles from yahoo now",
				 "please be patient while I scour yahoo news for available articles"]


# covid instructions

covidInform_command = ["how many people have covid in x",
				 	   "what's the infected count in x",
					   "what's the covid infected count in x",
					   "how many individuals are infected with covid in x",
					   "covid update for x",
					   "corona virus update for x",
					   "coronavirus update for x",
					   "how many covid cases are recorded for x",
					   "covid update in x",
					   "corona virus update in x",
					   "coronavirus update in x",
					   "how many covid cases are recorded in x",
					   "what's the latest covid infected cases for x",
					   "what's the current covid infected cases in x",
					   "what's the latest covid infected cases in x",
					   "what's the current covid infected cases for x",
					   f"{name} how many people have covid in x",
					   f"{name} what's the infected count in x",
					   f"{name} what's the covid infected count in x",
					   f"{name} how many individuals are infected with covid in x",
					   f"{name} covid update for x",
					   f"{name} corona virus update for x",
					   f"{name} coronavirus update for x",
					   f"{name} how many covid cases are recorded for x",
					   f"{name} what is the latest covid infected cases for x",
					   f"{name} what is the current covid infected cases in x"]

covidInform_command = [covidInform_command, list(set([phrase.split(" x")[0] for phrase in covidInform_command]))]

covidInform_command[1].sort(key = lambda word: word.count(" "), reverse = True)

covid_response = lambda country, amount: random.choice([f"the total number of confirmed cases in {country} is {num2words(amount)}",
				  				 			   		    f"the infected count for {country} is {num2words(amount)}",
				  				 			   		    f"the " + random.choice(["number", "amount"]) + f" of people infected with covid in {country} is {num2words(amount)}"])

covidHighest_response = lambda country, amount: random.choice([f"the country with the largest affected population is {country} with {num2words(amount)} infected " + random.choice(["persons", "cases", "individuals"]),
					  				 			   		       f"the country with the highest affected population is {country} with {num2words(amount)} people infected",
					  				 			   		       f"{country} has the most infected " + random.choice(["persons", "people", "individuals", "population"]) + f" with {num2words(amount)} cases",
					  				 			   		       f"{country} has {num2words(amount)} confirmed cases and is currently the worst affected country"])

covidLowest_response = lambda country, amount: random.choice([f"the country with the smallest affected population is {country} with {num2words(amount)} infected " + random.choice(["persons", "cases", "individuals"]),
					  				 			   		      f"the country with the lowest number of affected people is {country} with {num2words(amount)} infected cases",
					  				 			   		      f"{country} has the least infected " + random.choice(["persons", "people", "individuals", "population"]) + f" with {num2words(amount)} cases",
					  				 			   		      f"{country} has {num2words(amount)} confirmed cases and is currently the least affected country"])

covidHighest_command = ["which country has the highest infected cases",
						"which country has the highest number of cases",
						"which country has the most number of covid cases",
						"which country has the highest number of infected people",
						f"{name} which country has the highest infected cases",
						f"{name} which country has the highest number of cases",
						f"{name} which country has the most number of covid cases",
						f"{name} which country has the highest number of infected people"]

covidLowest_command = ["which country has the lowest infected cases",
					   "which country has the lowest number of cases",
					   "which country has the least number of covid cases",
					   "which country has the lowest number of infected people",
					   f"{name} which country has the lowest infected cases",
					   f"{name} which country has the lowest number of cases",
					   f"{name} which country has the least number of covid cases",
					   f"{name} which country has the lowest number of infected people"]

covid_commands, covid_command = [covidInform_command[0], covidInform_command[1], covidHighest_command, covidLowest_command], []

for category in covid_commands:
	for phrase in category: covid_command.append(phrase)


# stock market variables

company = ["TSLA", "MSFT", "AAPL", "TWTR", "FB", "GOOGL", "AMZN", "IBM"]
random.shuffle(company)
stocks = company[0:5]
# stocks = ["TSLA", "MSFT", "AAPL", "GOOGL", "AMZN"]

companies = {"TSLA": "tesla",
		   	 "MSFT": "microsoft",
		   	 "AAPL": "apple",
		     "TWTR": "twitter",
		     "FB": "facebook",
		     "GOOGL": "google",
		     "AMZN": "amazon",
		     "IBM": "ibm"}


# currency variables

money = ["GBP", "USD", "EUR"]
random.shuffle(money)
currencies = ["ZAR"] + money
pounds = ["pound", "british pound", "pound sterling"]
dollars = ["dollar", "american dollar", "U.S. dollar"]
rands = ["rand", "south african rand"]

currency_units =  {"ZAR": "rand",
		   		   "EUR": "euro",
		   		   "USD": random.choice(dollars),
		   		   "GBP": random.choice(pounds)}

details = [f"one _currency_ is _amount_ {currency_units[currencies[0]]}" + random.choice(["s", ""]),
		   f"the _currency_ to the {currency_units[currencies[0]]} is _amount_ {currency_units[currencies[0]]}" + random.choice(["s", ""]),
		   f"one _currency_ is equal to _amount_ {currency_units[currencies[0]]}" + random.choice(["s", ""]),
		   f"one _currency_ is equivalent to _amount_ {currency_units[currencies[0]]}" + random.choice(["s", ""])]

random.shuffle(details)


# downloader instructions

torrentDownload_command = ["please download x season y episode z torrent",
					       "download x season y episode z torrent",
					       "please get x season y episode z torrent",
					       "get x season y episode z torrent",
					       "please download x season y from episode w until episode z torrent",
					       "download x season y from episode w until episode z torrent",
					       "please get x season y from episode w until episode z torrent",
					       "get x season y episode from episode w until episode z torrent",
					       "please download x season y from episode z torrent",
					       "download x season y from episode z torrent",
					       "please get x season y from episode z torrent",
					       "get x season y episode from episode z torrent",
					       "please download x season y torrent",
					       "download x season y torrent",
					       "please get x season y torrent",
					       "get x season y torrent",
					       "please download x from season y until season z torrent",
					       "download x from season y until season z torrent",
					       "please get x from season y until season z torrent",
					       "get x from season y until season z torrent",
					       "please download x from season y torrent",
					       "download x from season y torrent",
					       "please get x from season y torrent",
					       "get x from season y torrent",
					       "download x torrent",
					       "please download x torrent",
					       "get x torrent",
					       "please get x torrent",
					       "download x series torrent",
					       "please download x series torrent",
					       "get x series torrent",
					       "please get x series torrent",
					       f"{name} please download x season y from episode w until episode z torrent",
					       f"{name} download x season y from episode w until episode z torrent",
					       f"{name} please get x season y from episode w until episode z torrent",
					       f"{name} get x season y episode from episode w until episode z torrent",
					       f"{name} please download x from season y until season z torrent",
					       f"{name} download x from season y until season z torrent",
					       f"{name} please get x from season y until season z torrent",
					       f"{name} get x from season y until season z torrent",
					       f"{name} please download x season y from episode z torrent",
					       f"{name} download x season y from episode z torrent",
					       f"{name} please get x season y from episode z torrent",
					       f"{name} get x season y episode from episode z torrent",
					       f"{name} please download x from season y torrent",
					       f"{name} download x from season y torrent",
					       f"{name} please get x from season y torrent",
					       f"{name} get x from season y torrent",
					       f"{name} please download x season y episode z torrent",
					       f"{name} download x season y episode z torrent",
					       f"{name} please get x season y episode z torrent",
					       f"{name} get x season y episode z torrent",
					       f"{name} please download x season y torrent",
					       f"{name} download x season y torrent",
					       f"{name} please get x season y torrent",
					       f"{name} get x season y torrent",
					       f"{name} download x torrent",
					       f"{name} please download x torrent",
					       f"{name} get x torrent",
					       f"{name} please get x torrent",
					       f"{name} download x series torrent",
					       f"{name} please download x series torrent",
					       f"{name} get x series torrent",
					       f"{name} please get x series torrent"]

torrentDownload_command = [torrentDownload_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in torrentDownload_command]))]

torrentDownload_command[1].sort(key = lambda word: word.count(" "), reverse = True)

torrent_checking = ["searching for your requested torrent file",
					"curating available torrents that best match your search request",
					"collecting all relevant torrents to filter and extract your files"]

torrent_response = ["torrent download process will now begin",
					"proceeding to download your files now",
					"setting up the magnet extractor to fetch your torrent files",
					"your magnet file will now be processed",
					f"now downloading your {random.choice(['torrent files', 'torrents', 'files'])}"]

youtubeDownload_command = ["please download x video",
					       "please download x audio",
					       "download x video",
					       "download x audio",
					       "please get x video",
					       "please get x audio",
					       "get x video",
					       "get x audio",
					       "please download x video playlist",
					       "please download x audio playlist",
					       "download x video playlist",
					       "download x audio playlist",
					       "please get x video playlist",
					       "please get x audio playlist",
					       "get x video playlist",
					       "get x audio playlist",
					       f"{name} please download x video",
					       f"{name} please download x audio",
					       f"{name} download x video",
					       f"{name} download x audio",
					       f"{name} please get x video",
					       f"{name} please get x audio",
					       f"{name} get x video",
					       f"{name} get x audio",
					       f"{name} please download x video playlist",
					       f"{name} please download x audio playlist",
					       f"{name} download x video playlist",
					       f"{name} download x audio playlist",
					       f"{name} please get x video playlist",
					       f"{name} please get x audio playlist",
					       f"{name} get x video playlist",
					       f"{name} get x audio playlist"]

youtubeDownload_command = [youtubeDownload_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in youtubeDownload_command]))]

youtubeDownload_command[1].sort(key = lambda word: word.count(" "), reverse = True)

youtube_checking = ["traversing youtube and checking for your file",
					"checking for your file on youtube",
					"searching through available youtube content to find your video"]

youtube_response = ["starting to download your file now",
					"your file will now be downloaded",
					"downloading will now proceed"]

comicDownload_command = ["please download x comic",
					     "download x comic",
					     "please get x comic",
					     "get x comic",
					     "please download x all comics",
					     "download x all comics",
					     "please get x all comics",
					     "get x all comics",
					     f"{name} please download x comic",
					     f"{name} download x comic",
					     f"{name} please get x comic",
					     f"{name} get x comic",
					     f"{name} please download x all comics",
					     f"{name} download x all comics",
					     f"{name} please get x all comics",
					     f"{name} get x all comics"]

comicDownload_command = [comicDownload_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in comicDownload_command]))]

comicDownload_command[1].sort(key = lambda word: word.count(" "), reverse = True)

animeDownload_command = [item.replace("torrent", "anime") for item in torrentDownload_command[0]]

animeDownload_command += ["download x everything anime",
					      "please download x everything anime",
					      "get x everything anime",
					      "please get x everything anime",
					      f"{name} download x everything anime",
					      f"{name} please download x everything anime",
					      f"{name} get x everything anime",
					      f"{name} please get x everything anime"]

animeDownload_command = [animeDownload_command, list(set([phrase.split(" x " if " x " in phrase else " x")[0] for phrase in animeDownload_command]))]

animeDownload_command[1].sort(key = lambda word: word.count(" "), reverse = True)

anime_checking = ["scouring servers for your file",
				  "searching and choosing your file from the available results",
				  "checking for your file in the cloud now"]

anime_response = ["currently downloading the requested file to your computer",
				  "i am now getting your file",
				  "i will now save your file on to your computer"]

download, download_command = [torrentDownload_command[0], youtubeDownload_command[0], comicDownload_command[0], animeDownload_command[0]], []

for category in download:
	for phrase in category: download_command.append(phrase)


# greetings

greet = lambda country, date_time, forecast = [str(0), "rain"], covid_update = [str(0)]*8, exchange_rates = [("EUR", str(0))]*3, market_prices = [("TSLA", str(0))]*5: [f"{greeting}. {random.choice(pronoun)} {name}. {random.choice(prefixes)} {date_time}. the weather in your city is {str(forecast[0])} degrees celcius {weather_map[forecast[1]]}. {random.choice(conclusion)}. {random.choice(help_question)}",
																					  			 							   	   		   								f"{greeting}. {random.choice(pronoun)} {name}. {random.choice(prefixes)} {date_time}. there are {num2words(str(covid_update[1]))} confirmed corona virus cases in {country}. the all time worldwide infected count is {num2words(str(covid_update[5]))} and the total number of covid related deaths has amounted to {num2words(str(covid_update[7]))}. {random.choice(conclusion)}. {random.choice(help_question)}",
																					  			 							   	   		   								f"{greeting}. {random.choice(pronoun)} {name}. {random.choice(prefixes)} {date_time}. here is a comparison of some exchange rates weighted against your local currency.... {details[0].replace('_currency_', currency_units[exchange_rates[0][0]]).replace('_amount_', exchange_rates[0][1] if len(exchange_rates[0][1].split('.')) == 1 else exchange_rates[0][1].split('.')[0])} " + (f"and {exchange_rates[0][1].split('.')[-1]} cents" if len(exchange_rates[0][1].split('.')) > 1 else "") + f".... {details[1].replace('_currency_', currency_units[exchange_rates[1][0]]).replace('_amount_', exchange_rates[1][1] if len(exchange_rates[1][1].split('.')) == 1 else exchange_rates[1][1].split('.')[0])} " + (f"and {exchange_rates[1][1].split('.')[-1]} cents" if len(exchange_rates[1][1].split('.')) > 1 else "") + f".... {details[2].replace('_currency_', currency_units[exchange_rates[2][0]]).replace('_amount_', exchange_rates[2][1] if len(exchange_rates[2][1].split('.')) == 1 else exchange_rates[2][1].split('.')[0])} " + (f"and {exchange_rates[2][1].split('.')[-1]} cents" if len(exchange_rates[2][1].split('.')) > 1 else "") + f". {random.choice(conclusion)}. {random.choice(help_question)}",
																					  			 							   	   		   								f"{greeting}. {random.choice(pronoun)} {name}. {random.choice(prefixes)} {date_time}. here are the top five stock prices from the selected companies.... {companies[market_prices[0][0]]}. {str(market_prices[0][1])} dollars.... {companies[market_prices[1][0]]}. {str(market_prices[1][1])} dollars.... {companies[market_prices[2][0]]}. {str(market_prices[2][1])} dollars.... {companies[market_prices[3][0]]}. {str(market_prices[3][1])} dollars.... and {companies[market_prices[4][0]]}. {str(market_prices[4][1])} dollars.... {random.choice(conclusion)}. {random.choice(help_question)}"][value]




# AI names

"""
Octavia
Julia
Dalia
Kailani
Eliza
Isla
Amelia
Olivia
Delores
*Tinashe
Tamara = Tinashe + Zamara
*Zamara

Davis
Java
Thurgood
Felix
Sylvester
Orbit
Elliot
Travis
Anthony
Hawking
"""
"""
Jötunheimr
let none ignorant of calculus enter here
"""
"""
Open the pod bay doors, HAL.
I'm sorry, Dave. I'm afraid I can't do that.
"""