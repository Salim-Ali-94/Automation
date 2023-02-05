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

	opened = True
	golden_cookie = []
	minimum, delay = None, None
	os.system("cls"), print()
	backup = input("Do you want to load a previous save file? (y / n): ")

	while backup.lower().rstrip().lstrip() not in ["y", "n"]:

		os.system("cls"), print()
		backup = input("Do you want to load a previous save file? (y / n): ")


	if (backup.lower().rstrip().lstrip() == "y"): 

		os.system("cls"), print()
		bakery = input("Please specify the profile name for the specific save file (case sensitive): ")

	else: 

		os.system("cls"), print()
		bakery = input("Name your bakery (leave blank to randomize): ")

	os.system("cls"), print()
	save_frequency = input("How often (minutes) do you want to save your progress?: ")

	while not save_frequency.lower().rstrip().lstrip().isdigit():

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

			while not delay.lower().rstrip().lstrip().isdigit():

				os.system("cls"), print()
				delay = input("How often (minutes) do you want to buy items and upgrades?: ")

		else: 

			os.system("cls"), print()
			minimum = input("Set a minimum price point (number of cookies) for purchasing upgrades and items: ")

			while not minimum.lower().rstrip().lstrip().isdigit():

				os.system("cls"), print()
				minimum = input("Set a minimum price point (number of cookies) for purchasing upgrades and items: ")

	os.system("cls"), print()
	speed = input("Please specify a click rate for the bot (clicks per second): ")

	while not speed.lower().rstrip().lstrip().isdigit():

		os.system("cls"), print()
		speed = input("Please specify a click rate for the bot (clicks per second): ")

	period = 1 / int(speed)
	save_interval = float(save_frequency)*60
	os.system("cls"), print()
	driver = initializeDriver()
	driver.maximize_window()
	driver.get(URL)
	WebDriverWait(driver, timeout = 30).until(EC.visibility_of_element_located((By.ID, "langSelect-EN")))
	language = driver.find_element_by_id("langSelect-EN")
	driver.execute_script("arguments[0].click();", language)
	if (backup.lower().lstrip().rstrip() == "n"): driver, bakery = nameBakery(driver, bakery)
	elif ((backup.lower().lstrip().rstrip() == "y") & f"CC_{bakery}_save_file.txt" in os.listdir(os.getcwd())): driver = loadCheckpoint(driver, bakery)
	elif ((backup.lower().lstrip().rstrip() == "y") & f"CC_{bakery}_save_file.txt" not in os.listdir(os.getcwd())): print(f"NO SAVE FILE FOUND FOR BAKERY '{bakery}'")
	got_it = driver.find_elements_by_css_selector(".cc_btn.cc_btn_accept_all")
	if (len(got_it) > 0): got_it[0].click()
	driver = saveProgress(driver, bakery)
	cookie = driver.find_element_by_id("bigCookie")
	start = float(time.time())
	begin = float(time.time())

	while True:

		cookie.click()
		time.sleep(period)
		amount = driver.find_element_by_id("cookies").text.split()[0]
		unlocked = driver.find_elements_by_css_selector(".product.unlocked.enabled")
		upgrades = driver.find_elements_by_css_selector(".crate.upgrade.enabled")
		golden_cookie = driver.find_elements_by_css_selector(".shimmer")

		if (len(golden_cookie) > 0): 

			golden_cookie = []
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".shimmer"))).click()
			print("You found a golden cookie!")

		if (strategy.lower().lstrip().rstrip() == "a"):

			if (len(unlocked) > 0): driver, upgrades = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
			if (len(upgrades) > 0): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

		elif (strategy.lower().lstrip().rstrip() == "b"):

			if (len(unlocked) > 0): driver, upgrades = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
			if (len(upgrades) > 0): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

		elif (strategy.lower().lstrip().rstrip() == "c"):

			if (delay != None):

				stop = float(time.time())
				t = stop - begin

				if (t >= float(delay)*60):

					if ((len(unlocked) > 0) & (len(upgrades) == 0)): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
					elif ((len(upgrades) > 0) & (len(unlocked) == 0)): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

					elif ((len(unlocked) > 0) & (len(upgrades) > 0)):

						parity = random.randint(0, 1)

						if (parity%2 == 0): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
						else: driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

					begin = float(time.time())

			elif (minimum != None):

				if (int(amount.replace(",", "")) >= int(minimum.replace(",", ""))):

					if ((len(unlocked) > 0) & (len(upgrades) == 0)): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
					elif ((len(upgrades) > 0) & (len(unlocked) == 0)): driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

					elif ((len(unlocked) > 0) & (len(upgrades) > 0)):

						parity = random.randint(0, 1)

						if (parity%2 == 0): driver = purchaseItem(driver, unlocked, strategy.lower().lstrip().rstrip(), "item")
						else: driver = purchaseItem(driver, upgrades, strategy.lower().lstrip().rstrip(), "upgrade")

		end = float(time.time())
		dt = end - start

		if (dt >= save_interval):

			driver = saveProgress(driver, bakery)
			start = float(time.time())
			cookie = driver.find_element_by_id("bigCookie")

		if keyboard.is_pressed("x"):

			driver.quit()
			break

		elif ((opened == True) and keyboard.is_pressed("esc")):

			driver.quit()
			opened = False
			driver = initializeDriver(True)
			driver.get(URL)
			driver.maximize_window()
			WebDriverWait(driver, timeout = 30).until(EC.visibility_of_element_located((By.ID, "langSelect-EN")))
			language = driver.find_element_by_id("langSelect-EN")
			driver.execute_script("arguments[0].click();", language)
			WebDriverWait(driver, timeout = 30).until(EC.visibility_of_element_located((By.ID, "bakeryName")))
			driver = loadCheckpoint(driver, bakery, opened)
			got_it = driver.find_elements_by_css_selector(".cc_btn.cc_btn_accept_all")
			if (len(got_it) > 0): got_it[0].click()
			cookie = driver.find_element_by_id("bigCookie")




if __name__ == "__main__":

	botManager()
