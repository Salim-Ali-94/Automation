import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os, random


def initializeDriver(state = False):

	settings = webdriver.ChromeOptions()
	settings.headless = state
	settings.add_experimental_option("excludeSwitches", ["enable-logging"])
	driver = webdriver.Chrome(executable_path = "chromedriver", options = settings)
	return driver

def saveProgress(browser, shop, info = True):

	root = os.getcwd()
	if (os.path.isdir("Save Files") == False): os.makedirs("Save Files")
	os.chdir("Save Files")
	options = browser.find_element_by_id("prefsButton")
	browser.execute_script("arguments[0].click();", options)
	export = browser.find_element_by_link_text("Export save")
	browser.execute_script("arguments[0].click();", export)
	tag = browser.find_element_by_id("textareaPrompt")
	with open(f"CC_{'_'.join(shop.split())}_save_file.txt", "w") as file: file.write(f"{tag.text}")
	done = browser.find_element_by_id("promptOption0")
	browser.execute_script("arguments[0].click();", done)
	options = browser.find_element_by_id("prefsButton")
	browser.execute_script("arguments[0].click();", options)
	browser, stats = getStats(browser)

	if (info == True):

		print("\nCheckpoint saved with the following stats:\n")
		for stat in stats: print(f"\t{stat}: {stats[stat]}")

	print()
	os.chdir(root)
	return browser

def loadCheckpoint(browser, shop, opened = True):

	root = os.getcwd()

	if (os.path.isdir("Save Files") == True):

		os.chdir("Save Files")

		if f"CC_{'_'.join(shop.split())}_save_file.txt" in os.listdir(os.getcwd()):

			with open(f"CC_{'_'.join(shop.split())}_save_file.txt", "r") as file: previous = file.readlines()
			options = browser.find_element_by_id("prefsButton")
			browser.execute_script("arguments[0].click();", options)
			WebDriverWait(browser, timeout = 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.option.smallFancyButton")))
			load = browser.find_element_by_link_text("Import save")
			browser.execute_script("arguments[0].click();", load)
			save_file = browser.find_element_by_id("textareaPrompt")
			save_file.send_keys(previous[0].rstrip().lstrip())
			done = browser.find_element_by_id("promptOption0")
			browser.execute_script("arguments[0].click();", done)

			if not opened:

				volume = browser.find_element_by_id("volumeSlider")
				browser.execute_script("arguments[0].setAttribute('value', 0)", volume)
				browser.execute_script("arguments[0].dispatchEvent(new Event('change'))", volume)

			options = browser.find_element_by_id("prefsButton")
			browser.execute_script("arguments[0].click();", options)
			browser, stats = getStats(browser)
			print(f"\nLoaded latest checkpoint for {shop} with the following stats:\n")
			for stat in stats: print(f"\t{stat}: {stats[stat]}")
			print()

		else:
		
			print(f"NO SAVE FILE FOUND FOR BAKERY '{shop}'")

		os.chdir(root)

	else:
	
		print(f"NO SAVE FILE FOUND FOR BAKERY '{shop}'")

	return browser

def getStats(browser):

	record = {}
	stats = browser.find_element_by_id("statsButton")
	browser.execute_script("arguments[0].click();", stats)
	WebDriverWait(browser, timeout = 30).until(EC.visibility_of_element_located((By.ID, "statsGeneral")))
	section = browser.find_element_by_id("statsGeneral")
	statistics = section.find_elements_by_css_selector(".listing")
	record[statistics[0].text.split(":", 1)[0]] = statistics[0].find_element_by_css_selector(".price.plain").text.lstrip().rstrip()
	record[statistics[1].text.split(":", 1)[0]] = statistics[1].find_element_by_css_selector(".price.plain").text.lstrip().rstrip()
	record[statistics[2].text.split(":", 1)[0]] = statistics[2].find_element_by_css_selector(".price.plain").text.lstrip().rstrip()
	record[statistics[3].text.split(":", 1)[0]] = " ".join(statistics[3].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[4].text.split(":", 1)[0]] = " ".join(statistics[4].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[5].text.split(":", 1)[0]] = " ".join(statistics[5].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[6].text.split(":", 1)[0]] = " ".join(statistics[6].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[7].text.split(":", 1)[0]] = " ".join(statistics[7].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[8].text.split(":", 1)[0]] = " ".join(statistics[8].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[9].text.split(":", 1)[0]] = " ".join(statistics[9].text.split(":", 1)[1:]).lstrip().rstrip()
	record[statistics[10].text.split(":", 1)[0]] = " ".join(statistics[10].text.split(":", 1)[1:]).lstrip().rstrip()
	stats = browser.find_element_by_id("statsButton")
	browser.execute_script("arguments[0].click();", stats)
	return browser, record

def nameBakery(browser, shop, replace = False):

	counter = 0
	root = os.getcwd()
	if (os.path.isdir("Save Files") == False): os.makedirs("Save Files")
	os.chdir("Save Files")
	WebDriverWait(browser, timeout = 30).until(EC.visibility_of_element_located((By.ID, "bakeryName")))

	if (shop == ""):

		shop = browser.find_element_by_id("bakeryName").text

		if (replace == False):

			placeholder = shop

			while f"CC_{'_'.join(shop.split())}_save_file.txt" in os.listdir(os.getcwd()):

				shop = placeholder + str(counter)
				counter += 1

	else:

		if (replace == False):

			placeholder = shop

			while f"CC_{'_'.join(shop.split())}_save_file.txt" in os.listdir(os.getcwd()):

				shop = placeholder + str(counter)
				counter += 1

		name = browser.find_element_by_id("bakeryName")
		browser.execute_script("arguments[0].click();", name)
		change_name = browser.find_element_by_id("bakeryNameInput")
		change_name.clear()
		change_name.send_keys(shop)
		confirm = browser.find_element_by_id("promptOption0")
		browser.execute_script("arguments[0].click();", confirm)

	os.chdir(root)
	return browser, shop

def purchaseItem(browser, inventory, strategy, category):

	if ((strategy == "a") or (strategy == "b")):

		if (category == "item"):

			items = [int(item.text.split()[-1].replace(",", "")) for item in inventory]
			index = items.index(max(items) if (strategy == "a") else min(items))
			buy = inventory[index]

		else:

			highest, lowest = 0, float("inf")

			for element in inventory:

				actions = ActionChains(browser)
				actions.move_to_element(element).perform()
				WebDriverWait(browser, timeout = 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#tooltip div.name")))
				tool = ' '.join(browser.find_element_by_css_selector("div#tooltip div.name").text.split())
				price = browser.find_element_by_css_selector("div#tooltip span.price").text.replace(",", "")

				if ((strategy == "a") and (int(price) > highest)):

					buy = element
					highest = int(price)
					selection = tool
					break

				elif ((strategy == "b") and (int(price) < lowest)):

					buy = element
					lowest = int(price)
					selection = tool
					break

		if (category == "item"): buy_text = buy.text.split()[0:-2 if (len(buy.text.split()) >= 3) else -1]
		else: buy_text = selection.split()
		browser.execute_script("arguments[0].click();", buy)
		print(f"You bought the {' '.join(buy_text)} {category}")

		if (category == "item"):

			upgrades = browser.find_elements_by_css_selector(".crate.upgrade.enabled")
			return browser, upgrades

		elif (category == "upgrade"):

			return browser

	elif (strategy == "c"):

		item = random.randint(0, len(inventory) - 1)
		buy = inventory[item]

		if (category == "upgrade"):

			actions = ActionChains(browser)
			actions.move_to_element(buy).perform()
			WebDriverWait(browser, timeout = 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#tooltip div.name")))
			selection = browser.find_element_by_css_selector("div#tooltip div.name")

		if (category == "item"): buy_text = buy.text.split()[0:-2 if (len(buy.text.split()) >= 3) else -1]
		else: buy_text = selection.text.split()
		browser.execute_script("arguments[0].click();", buy)
		print(f"You bought the {' '.join(buy_text)} {category}")
		return browser
