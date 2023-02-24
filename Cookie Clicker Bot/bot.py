import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import keyboard
from utility import *
from constants import *


def botManager():

	rate = 0
	replace = "no"
	golden_cookie = []
	minimum, delay = None, None

	if (os.path.isdir("Save Files") == True):

		root = os.getcwd()
		os.chdir("Save Files")
		os.system("cls"), print()
		backup = input("Do you want to load a previous save file? (y / n): ")

		while backup.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

			os.system("cls"), print()
			backup = input("Do you want to load a previous save file? (y / n): ")

		if backup.lower().rstrip().lstrip() in ["y", "yes"]:

			os.system("cls"), print()
			save_files = os.listdir(os.getcwd())
			files = [save_files[index][3:-4].replace("_save_file", "").replace("_", " ") for index in range(len(save_files))]
			print("Here are the available save files:\n")
			for index in range(len(files)): print(f"{index + 1}. {files[index]}")
			select = input(f"\nPlease select a checkpoint to load (1 - {len(files)}) / Or hit 0 to cancel loading a game session: ") if (len(files) > 1) else input(f"\nLoad the given save file? (y / n): ")

			if (len(files) > 1):

				while select.lower().lstrip().rstrip() not in [str(index + 1) for index in range(len(files))] + ["0"]:

					os.system("cls"), print()
					print("Here are the available save files:\n")
					for index in range(len(files)): print(f"{index + 1}. {files[index]}")
					select = input(f"\nPlease select a checkpoint to load (1 - {len(files)}) / Or hit 0 to cancel loading a game session: ") if (len(files) > 1) else input(f"\nLoad the given save file? (y / n): ")

			else:

				while select.lower().lstrip().rstrip() not in ["y", "yes", "n", "no"]:

					os.system("cls"), print()
					print("Here are the available save files:\n")
					for index in range(len(files)): print(f"{index + 1}. {files[index]}")
					select = input(f"\nPlease select a checkpoint to load (1 - {len(files)}) / Or hit 0 to cancel game load: ") if (len(files) > 1) else input(f"\nLoad the given save file? (y / n): ")

			if ((len(files) > 1) and select.lower().lstrip().rstrip() not in ["no", "n", "0"]): bakery = files[int(select.lower().lstrip().rstrip()) - 1]
			elif ((len(files) == 1) and select.lower().lstrip().rstrip() in ["yes", "y"]): bakery = files[0]
			else: backup = "no"

		os.chdir(root)

	else:

		backup = "no"

	if backup.lower().rstrip().lstrip() in ["n", "no"]:

		if (os.path.isdir("Save Files") == True):

			root = os.getcwd()
			os.chdir("Save Files")

			while True:

				os.system("cls"), print()
				bakery = input("Name your bakery (leave blank to randomize): ")

				if f"CC_{'_'.join(bakery.split())}_save_file.txt" in os.listdir(os.getcwd()):

					os.system("cls"), print()
					replace = input(f"A save file for bakery '{bakery}' already exists, do you want to replace your progress? (y / n): ")

					while replace.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

						os.system("cls"), print()
						replace = input("Do you want to replace your progress? (y / n): ")

					if replace.lower().lstrip().rstrip() in ["y", "yes"]:

						break

					else:

						os.system("cls"), print()
						again = input("Try another bakery name? (y / n): ")

						while again.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

							os.system("cls"), print()
							again = input("Try another bakery name? (y / n): ")

						if again.lower().lstrip().rstrip() in ["n", "no"]:

							bakery = ""
							break

				else:

					break

			os.chdir(root)
	
		else:

			os.system("cls"), print()
			bakery = input("Name your bakery (leave blank to randomize): ")

	os.system("cls"), print()
	save_frequency = input("How often (minutes) do you want to save your progress?: ")

	while not isNumber(save_frequency.lower().rstrip().lstrip()):

		os.system("cls"), print()
		save_frequency = input("How often (minutes) do you want to save your progress?: ")

	os.system("cls"), print()
	strategy = input("Select a strategy for buying upgrades:\n\na. Rich dad\nb. Poor dad\nc. Random\n\n")

	while strategy.lower().rstrip().lstrip() not in ["a", "b", "c"]:

		os.system("cls"), print()
		strategy = input("Select a strategy for buying upgrades:\n\na. Rich dad\nb. Poor dad\nc. Random\n\n")

	if (strategy.lower().rstrip().lstrip() == "c"):

		os.system("cls"), print()
		method = input("Should items and upgrades be selected after a given interval (delay) or everytime a certain number of cookies is collected (threshold)?:\n\na. Delay\nb. Threshold\n\n")

		while method.lower().rstrip().lstrip() not in ["a", "b"]:

			os.system("cls"), print()
			method = input("Should items and upgrades be selected after a given interval (delay) or everytime a certain number of cookies is collected (threshold)?:\n\na. Delay\nb. Threshold\n\n")

		if (method.lower().rstrip().lstrip() == "a"): 

			os.system("cls"), print()
			delay = input("How often (minutes) do you want to buy items and upgrades?: ")

			while not isNumber(delay.lower().rstrip().lstrip()):

				os.system("cls"), print()
				delay = input("How often (minutes) do you want to buy items and upgrades?: ")

		else: 

			os.system("cls"), print()
			minimum = input("Set a minimum price point (number of cookies) for purchasing upgrades and items: ")

			while not minimum.lower().rstrip().lstrip().isdigit():

				os.system("cls"), print()
				minimum = input("Set a minimum price point (number of cookies) for purchasing upgrades and items: ")

	os.system("cls"), print()
	speed = input(f"Please specify a processing capacity for the bot:\n\na. shaytaan ({random.choice(['channel', 'invoke', 'manifest', 'unleash'])} the spirit of the devil himself, meneer iblees, {random.choice(['ripping', 'burning', 'shredding'])} through your cpu cycles)\nb. lightning (produce blazing speeds, at the {random.choice(['cost', 'expense'])} of moderate cpu operation)\nc. salim (slowest motherfucker in town, cpu is hardly {random.choice(['bothered', 'concerned', 'perplexed'])})\n\n")

	while speed.lower().rstrip().lstrip() not in ["a", "b", "c"]:

		os.system("cls"), print()
		speed = input("Please specify a processing capacity for the bot:\n\na. shaytaan (faster click rate, heavy cpu operation)\nb. lightning (standard click rate, moderate cpu operation)\nc. salim (slower click rate, light cpu operation)\n\n")

	os.system("cls"), print()
	view = input("Should game updates be displayed? (y / n): ")

	while view.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

		os.system("cls"), print()
		view = input("Should game updates be displayed? (y / n): ")

	os.system("cls"), print()
	window = input(f"Do you want the game to start in {random.choice(['shadow', 'stealth'])} mode? (y / n): ")

	while window.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

		os.system("cls"), print()
		window = input(f"Do you want to the game to start in {random.choice(['shadow', 'stealth'])} mode? (y / n): ")

	os.system("cls"), print()
	listener = input("Do you want to activate the keyboard listener? (y / n): ")

	while listener.lower().rstrip().lstrip() not in ["y", "yes", "n", "no"]:

		os.system("cls"), print()
		listener = input("Do you want to activate the keyboard listener? (y / n): ")

	if (speed.lower().lstrip().rstrip() == "b"): rate = 0.05
	elif (speed.lower().lstrip().rstrip() == "c"): rate = 0.1
	opened = True if window.lower().lstrip().rstrip() in ["n", "no"] else False
	save_interval = abs(float(save_frequency))*60
	os.system("cls"), print()
	driver = initializeDriver(not(opened))
	driver.maximize_window()
	driver.get(URL)
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "langSelect-EN")))
	language = driver.find_element_by_id("langSelect-EN")
	driver.execute_script("arguments[0].click();", language)
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "prefsButton")))
	if (backup.lower().lstrip().rstrip() in ["n", "no"]): driver, bakery = nameBakery(driver, bakery, True if replace.lower().lstrip().rstrip() in ["y", "yes"] else False)
	else: driver = loadCheckpoint(driver, bakery, opened, False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cc_btn.cc_btn_accept_all")))
	got_it = driver.find_elements_by_css_selector(".cc_btn.cc_btn_accept_all")
	if (len(got_it) > 0): got_it[0].click()
	if backup.lower().lstrip().rstrip() in ["n", "no"]: driver = saveProgress(driver, bakery, False)
	WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "bigCookie")))	
	cookie = driver.find_element_by_id("bigCookie")
	start = float(time.time())
	begin = float(time.time())

	while True:

		cookie.click()
		if (speed.lower().lstrip().rstrip() != "a"): time.sleep(rate)
		amount = driver.find_element_by_id("cookies").text.split()[0]
		unlocked = driver.find_elements_by_css_selector(".product.unlocked.enabled")
		upgrades = driver.find_elements_by_css_selector(".crate.upgrade.enabled")
		golden_cookie = driver.find_elements_by_css_selector(".shimmer")

		if (len(golden_cookie) > 0): 

			golden_cookie = []
			WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".shimmer"))).click()
			if view in ["y", "yes"]: print("You found a golden cookie!")

		if (strategy.lower().lstrip().rstrip() == "a"):

			if (len(unlocked) > 0): driver, upgrades = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
			if (len(upgrades) > 0): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

		elif (strategy.lower().lstrip().rstrip() == "b"):

			if (len(unlocked) > 0): driver, upgrades = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
			if (len(upgrades) > 0): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

		elif (strategy.lower().lstrip().rstrip() == "c"):

			if (delay != None):

				stop = float(time.time())
				t = stop - begin

				if (t >= abs(float(delay))*60):

					if ((len(unlocked) > 0) & (len(upgrades) == 0)): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
					elif ((len(upgrades) > 0) & (len(unlocked) == 0)): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

					elif ((len(unlocked) > 0) & (len(upgrades) > 0)):

						parity = random.randint(0, 1)
						if (parity%2 == 0): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
						else: driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

					begin = float(time.time())

			elif (minimum != None):

				if (int(amount.replace(",", "")) >= int(minimum.replace(",", ""))):

					if ((len(unlocked) > 0) & (len(upgrades) == 0)): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
					elif ((len(upgrades) > 0) & (len(unlocked) == 0)): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

					elif ((len(unlocked) > 0) & (len(upgrades) > 0)):

						parity = random.randint(0, 1)

						if (parity%2 == 0): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
						else: driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade", False if view.lower().lstrip().rstrip() in ["n", "no"] else True)

		end = float(time.time())
		delta = end - start

		if (delta >= save_interval):

			driver = saveProgress(driver, bakery, False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
			WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "bigCookie")))
			start = float(time.time())
			cookie = driver.find_element_by_id("bigCookie")

		if listener in ["y", "yes"]:

			if keyboard.is_pressed("esc"):

				if view in ["y", "yes"]: print("\nShutting down...\n")
				driver.quit()
				break

			elif (((opened == True) and keyboard.is_pressed("end")) or ((opened == False) and keyboard.is_pressed("home"))):

				if (view in ["y", "yes"] and (opened == True)): print(f"\n{random.choice(['Activating', 'Initiating', 'Entering'])} ninja mode...\n")
				elif (view in ["y", "yes"] and (opened == False)): print("\nOpening the game window...\n")
				driver.quit()
				opened = False if (opened == True) else True
				driver = initializeDriver(not(opened))
				driver.maximize_window()
				driver.get(URL)
				WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "langSelect-EN")))
				language = driver.find_element_by_id("langSelect-EN")
				driver.execute_script("arguments[0].click();", language)
				WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "bakeryName")))
				driver = loadCheckpoint(driver, bakery, opened, False if view.lower().lstrip().rstrip() in ["n", "no"] else True)
				WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cc_btn.cc_btn_accept_all")))
				got_it = driver.find_elements_by_css_selector(".cc_btn.cc_btn_accept_all")
				if (len(got_it) > 0): got_it[0].click()
				WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "bigCookie")))
				cookie = driver.find_element_by_id("bigCookie")

			elif (((view.lower().lstrip().rstrip() in ["y", "yes"]) and keyboard.is_pressed("page_down")) or ((view.lower().lstrip().rstrip() in ["n", "no"]) and keyboard.is_pressed("page_up"))):

				if (view.lower().lstrip().rstrip() in ["y", "yes"]): 

					view = "no"

				elif (view.lower().lstrip().rstrip() in ["n", "no"]): 

					view = "yes"
					print(f"\nGame alerts {random.choice(['are now visible', 'will now be visible'])}...")

			elif (((speed.lower().lstrip().rstrip() in ["b", "c"]) and keyboard.is_pressed("+")) or ((speed.lower().lstrip().rstrip() in ["a", "b"]) and keyboard.is_pressed("-"))):

				if ((speed.lower().lstrip().rstrip() == "b") and keyboard.is_pressed("+")):

					speed = "a"
					rate = 0
					if view in ["y", "yes"]: print(f"\n{random.choice(['Switching it up to', 'Shifting to', 'Switching to', 'Shifting it up to'])} {random.choice(['balistic', 'hyper'])} {random.choice(['speeds', 'mode'])}...\n")

				elif ((speed.lower().lstrip().rstrip() == "c") and keyboard.is_pressed("+")):

					speed = "b"
					rate = 0.05
					if view in ["y", "yes"]: print(f"\n{random.choice(['Switching it up to', 'Shifting to', 'Switching to', 'Shifting it up to'])} lightning {random.choice(['speeds', 'mode'])}...\n")

				elif ((speed.lower().lstrip().rstrip() == "b") and keyboard.is_pressed("-")):

					speed = "c"
					rate = 0.1
					if view in ["y", "yes"]: print(f"\n{random.choice(['Switching to', 'Shifting to', 'Dialing it down to', 'Dialing it back to', 'Switching down to', 'Shifting down to', 'Turning it down to'])} salim {random.choice(['speeds', 'mode'])}...\n")
		
				elif ((speed.lower().lstrip().rstrip() == "a") and keyboard.is_pressed("-")):

					speed = "b"
					rate = 0.05
					if view in ["y", "yes"]: print(f"\n{random.choice(['Switching to', 'Shifting to', 'Dialing it down to', 'Switching down to', 'Shifting down to', 'Turning it down to'])} lightning {random.choice(['speeds', 'mode'])}...\n")

			if keyboard.is_pressed("/"):

				listener = "no"
				if view in ["y", "yes"]: print(f"\nDeactivating the keyboard listener, you will no longer be able to change game settings now...\n")




if __name__ == "__main__":

	botManager()
