import selenium
from selenium import webdriver
from subprocess import DEVNULL, STDOUT
from selenium.webdriver.common.keys import Keys
import subprocess, os, sys
import time
import random
import psutil
import textwrap


class OrderFood(Downloader):

    options = ["A", "a", "B", "b", "C", "c"]
    numbers = lambda self, start, end: [str(index) for index in range(start, end + 1)]
    
    def __init__(self, browser_path, mrDFood_admin, mrDFood_password):

        self.directory = browser_path
        self.mrDFood_admin = mrDFood_admin
        self.mrDFood_password = mrDFood_password
        self.reset_browser()


    def reset_browser(self, status = True):

        subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE", stdout = DEVNULL, stderr = STDOUT)
        settings = webdriver.ChromeOptions()
        settings.headless = status
        settings.add_experimental_option("excludeSwitches", ["enable-logging"])

        try: 

            self.driver = webdriver.Chrome(executable_path = self.directory, options = settings)

        except:

            settings.add_argument("--remote-debugging-port=9222")
            self.driver = webdriver.Chrome(executable_path = self.directory, options = settings)

        self.driver.implicitly_wait(5)
        self.kill_chrome()


    def kill_chrome(self):

        folder = os.listdir(os.getcwd())
        parent = psutil.Process(self.driver.service.process.pid)
        children = parent.children(recursive = True)

        if ("chrome_tabs.txt" in folder):
    
            with open("chrome_tabs.txt", "r") as file: ID = file.readlines()

            for pid in ID:

                try: os.kill(int(pid.strip("\n")), signal.SIGTERM)
                except: continue

        with open("chrome_tabs.txt", "w") as file:

            file.write(f"{self.driver.service.process.pid}")
            for child in children: file.write(f"\n{child.pid}")


    def login(self):

        login_menu = self.driver.find_element_by_xpath("//a[@ng-click='_rc.hideMenu();']")
        self.driver.execute_script("arguments[0].click();", login_menu)
        username = self.driver.find_element_by_id("username")
        username.send_keys(self.mrDFood_admin)
        password = self.driver.find_element_by_id("password")
        password.send_keys(self.mrDFood_password)
        login_button = self.driver.find_element_by_id("btnLogin")
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", login_button)
        time.sleep(2)


    def find_address(self):

        url = "https://www.mrdfood.com/"
        done = False

        while not done:

            os.system("cls")
            self.driver.get(url)
            self.address = input("\nPlease specify the delivery address (format; [house/appartment number] [street name]): ")

            while not self.address.split()[0].isdigit():

                os.system("cls")
                self.address = input("\nInvalid format, the address must be specified as follows; [house/appartment number] [street name]: ")

            search = self.driver.find_element_by_id("addressSearchInput_primary")
            search.send_keys(self.address)
            time.sleep(2)
            suburb = self.driver.find_elements_by_css_selector("a span.start")
            city = self.driver.find_elements_by_css_selector("a span.end")

            if (len(city) > 0):

                os.system("cls")
                print("\nHere is a list of areas matching your search:\n")
                for index in range(len(city)): print(f"{index + 1}. {suburb[index].text} ({city[index].text})")
                location = input(f"\nPlease select a delivery location (0 [input another address] - {len(city)}): ")

                while location.rstrip().lstrip() not in self.numbers(0, len(city)):

                    os.system("cls"), print()
                    for index in range(len(city)): print(f"{index + 1}. {suburb[index].text} ({city[index].text})")
                    location = input(f"\nInvalid entry, please select an available option (0 [input another address] - {len(city)}): ")

                if (location.rstrip().lstrip() != "0"):

                    done = True
                    area = suburb[int(location.rstrip().lstrip()) - 1]
                    self.driver.execute_script("arguments[0].click();", area)
                    time.sleep(2)

            elif (len(city) == 0):

                os.system("cls")
                exit = input(f"\nThere are no results matching your requested search; '{address}', do you want to try and input a more precise address?: \n\nA: yes \nB: no \n\n")

                while exit.lower().rstrip().lstrip() not in self.options[0:4]:

                    os.system("cls")
                    exit = input(f"\nInvalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                if (exit.lower().rstrip().lstrip() == "a"): done = False
                elif (exit.lower().rstrip().lstrip() == "b"): done = True
                if (done == True): sys.exit()


    def mrDFood(self):

        opened = True
        self.find_address()
        url = self.driver.current_url
        self.driver.get(url)
        restaurants = self.driver.find_elements_by_css_selector("h2.ng-binding")
        offline = self.driver.find_elements_by_css_selector("div.status")
        if (len(offline) == len(restaurants)): opened = False

        if (opened == True):

            self.login()
            displacement, takeaway = [], []
            position, location = [], []
            available, online, opened = True, True, True
            done, exit, complete = False, False, False
            main_tick, food = None, []
            stay, another = True, False
            drinks = ["coke", "coca", "coca-cola", "cola", "coca cola", "granadilla", "fanta orange", "fanta pineapple"]
            types = ["light", "zero", "sugar", "free"]
            remove = ["onion", "garnish", "garlic", "ginger"]
            restaurants = self.driver.find_elements_by_css_selector("h2.ng-binding")
            distances = self.driver.find_elements_by_css_selector("span.distance.hidden.ng-binding")
            cards = self.driver.find_elements_by_xpath("//li[@ng-repeat='item in _lc.filteredItems = (_lc.restaurants.items | searchFilterIds: _lc.searchIds)']")
            offline = self.driver.find_elements_by_css_selector("div.status")
            website = str(self.driver.page_source)
            eateries = [restaurant.text for restaurant in restaurants]

            with open("restaurant_webpage.txt", "w+") as file:

                file.write(website)
                file.seek(0)

                for line in file:

                    result = line
                    start = '<span class="distance hidden ng-binding">'
                    end = '</span>'
                    try: result = line.split(start)[1].split(end)[0]
                    except: pass
                    if (result != line): position.append(int(result.replace("&nbsp;", "").replace("m", "").replace("away", "").rstrip()))

            while not complete:

                done, complete = False, False
                os.system("cls")
                interface = input(f"\nSelect an interaction mode: \n\nA: automatic \nB: manual \n\n")

                while interface.rstrip().lstrip() not in self.options[0:4]:

                    os.system("cls")
                    interface = input(f"\nInvalid entry, please select an available option: \n\nA: automatic mode \nB: interactive mode \n\n")

                if (interface.lower().rstrip().lstrip() == "a"): interface = "automatic"
                elif (interface.lower().rstrip().lstrip() == "b"): interface = "manual"

                while not done:

                    displacement = position.copy()
                    takeaway, location = [], []
                    available, online, opened = True, True, True
                    done, exit, complete = False, False, False
                    main_tick, food = None, []
                    stay, another = True, False
                    self.driver.get(url)
                    restaurants = self.driver.find_elements_by_css_selector("h2.ng-binding")
                    distances = self.driver.find_elements_by_css_selector("span.distance.hidden.ng-binding")
                    cards = self.driver.find_elements_by_xpath("//li[@ng-repeat='item in _lc.filteredItems = (_lc.restaurants.items | searchFilterIds: _lc.searchIds)']")
                    offline = self.driver.find_elements_by_css_selector("div.status")
                    eateries = [restaurant.text for restaurant in restaurants]

                    for item in offline:

                        index = cards.index(item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath(".."))
                        cards.pop(index), distances.pop(index), restaurants.pop(index), displacement.pop(index), eateries.pop(index)

                    if (len(eateries) > 0):

                        if (interface == "automatic"):

                            restaurants = self.driver.find_elements_by_css_selector("h2.ng-binding")
                            eateries = [restaurant.text for restaurant in restaurants]
                            os.system("cls")
                            eatery = input("\nPlease input the name of an eatery that you want to order food from: ")

                            for item in eateries:

                                if eatery.lower().rstrip().lstrip() in item.lower().rstrip().lstrip():

                                    available = True
                                    break
                                
                                elif ((item == eateries[-1]) & (eatery.lower().rstrip().lstrip() not in item.lower().rstrip().lstrip())):

                                    available = False
                                    os.system("cls")
                                    print("\nThe requested eatery in not available in your area\n")
                                    other = input("Do you want to try a different restaurant?: \n\nA: yes \nB: no \n\n")

                                    while other not in self.options[0:4]:
            
                                        os.system("cls")
                                        other = input("Invalid entry, please select an available option: \n\nA: search for a different restaurant \nB: exit program \n\n")

                                    if (other.lower().rstrip().lstrip() == "a"): done = False
                                    elif (other.lower().rstrip().lstrip() == "b"): done, exit, complete = True, True, True

                            if (available == True):

                                displacement = position.copy()
                                distances = self.driver.find_elements_by_css_selector("span.distance.hidden.ng-binding")
                                cards = self.driver.find_elements_by_xpath("//li[@ng-repeat='item in _lc.filteredItems = (_lc.restaurants.items | searchFilterIds: _lc.searchIds)']")
                                offline = self.driver.find_elements_by_css_selector("div.status")

                                for item in offline:

                                    index = cards.index(item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath(".."))
                                    cards.pop(index), distances.pop(index), restaurants.pop(index), displacement.pop(index), eateries.pop(index)

                                for item in eateries:

                                    if eatery.lower().rstrip().lstrip() in item.lower().rstrip().lstrip():

                                        online, done = True, True
                                        break
                                    
                                    elif ((item == eateries[-1]) & (eatery.lower().rstrip().lstrip() not in item.lower().rstrip().lstrip())):

                                        online = False
                                        os.system("cls")
                                        print("\nThe requested eatery in not available at this hour\n")
                                        other = input("Do you want to try a different restaurant?: \n\nA: yes \nB: no \n\n")

                                        while other not in self.options[0:4]:
                
                                            os.system("cls")
                                            other = input("Invalid entry, please select an available option: \n\nA: select a different restaurant \nB: exit program \n\n")

                                        if (other.lower().rstrip().lstrip() == "a"): done = False
                                        elif (other.lower().rstrip().lstrip() == "b"): done, exit, complete = True, True, True

                                if ((online == True) & (exit == False)):

                                    for index in range(len(restaurants)):

                                        if eatery.lower().rstrip().lstrip() in eateries[index].lower():

                                            takeaway.append(restaurants[index])
                                            location.append(displacement[index])
                                            food.append(eateries[index])

                                    nearest = min(location)
                                    address = location.index(nearest)
                                    takeout = takeaway[address]
                                    restaurant = food[address]

                        elif (interface == "manual"):

                            os.system("cls")
                            print("\nHere is a list of all the restaurants in your area available at this hour: \n\n")
                            for index in range(len(eateries)): print(f"{index + 1}. {eateries[index]}")
                            eatery = input(f"\nPlease select an eatery that you want to order food from (1 - {len(eateries)}): ")

                            while eatery not in self.numbers(0, len(eateries)):

                                os.system("cls"), print()
                                for index in range(len(eateries)): print(f"{index + 1}. {eateries[index]}")
                                eatery = input(f"\nInvalid entry, please select an available option (1 - {len(eateries)}): ")

                            done = True
                            takeout = restaurants[int(eatery) - 1]
                            restaurant = eateries[int(eatery) - 1]

                    else:

                        online, exit = False, True
                        press, done = None, True
                        os.system("cls")
                        print("\nSorry, but there are no eateries available in your area at this hour\n")
                        while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")

                if ((online == True) & (exit == False)):

                    self.driver.execute_script("arguments[0].click();", takeout)
                    time.sleep(2)
                    page = self.driver.current_url

                    while (stay == True):

                        checkbox, main_tick = [], None
                        another, indices = False, []
                        self.driver.get(page)
                        time.sleep(2)
                        meals = self.driver.find_elements_by_css_selector("span.title.ng-binding")
                        foods = [meal for meal in meals if (meal.text != "")]
                        menu = [food.text for food in foods]
                        links = self.driver.find_elements_by_css_selector("div.menu-item.ng-scope")
                        time.sleep(2)
                        unavailable = self.driver.find_elements_by_css_selector("div.menu-item.ng-scope.soldout")
                        finished = [item.find_element_by_css_selector("span.title.ng-binding").text for item in unavailable]
                        values = self.driver.find_elements_by_xpath("//span[@ng-class=\"{\'red\': item._old_price || item.menu_deal_action === \'buy_1_get_1_free\'}\"]")
                        amount = [value.text for value in values]
                        for item in finished: foods.pop(menu.index(item)), links.pop(menu.index(item)), amount.pop(menu.index(item)), menu.pop(menu.index(item))
                        collect_only = self.driver.find_elements_by_css_selector("span.collect-only.ng-scope")

                        for item in collect_only:

                            if item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..") in links:

                                index = links.index(item.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath(".."))
                                foods.pop(index), links.pop(index), menu.pop(index), amount.pop(index)
                                indices.append(index)

                        sections = self.driver.find_elements_by_xpath("//li[@ng-repeat='section in _mc.menu_sections_a']")
                        sections += self.driver.find_elements_by_xpath("//li[@ng-repeat='section in _mc.menu_sections_b']")
                        headings = [item.find_element_by_css_selector("div.section-header.ng-binding").text for item in sections]
                        prices = [[] for index in range(len(headings))]
                        tags = [[] for index in range(len(headings))]
                        anchors = [[] for index in range(len(headings))]
                        current = headings[0]
                        previous, count = current, 0

                        for index in range(len(menu)):

                            current = links[index].find_element_by_xpath("..").find_element_by_css_selector("div.section-header.ng-binding").text
                            if (current != previous): count += 1
                            anchors[count].append(links[index])
                            tags[count].append(menu[index])
                            prices[count].append(amount[index])
                            previous = current

                        Anchors, Tags, Prices = anchors.copy(), tags.copy(), prices.copy()

                        for index in range(len(headings)):

                            if (len(anchors[index]) == 0): Anchors.pop(Anchors.index(anchors[index]))
                            if (len(tags[index]) == 0): Tags.pop(Tags.index(tags[index]))
                            if (len(prices[index]) == 0): Prices.pop(Prices.index(prices[index]))

                        anchors, tags, prices = Anchors.copy(), Tags.copy(), Prices.copy()

                        if (interface == "manual"):

                            while not another:

                                os.system("cls")
                                print(f"\nWhat type of meal are you having from {restaurant} today?:\n")
                                for index in range(len(headings)): print(f"{index + 1}. {headings[index]}")
                                number = input(f"\nPlease select a menu from the list above (1 - {len(headings)}): ")

                                while number not in self.numbers(1, len(headings)):

                                    os.system("cls")
                                    print(f"\nInvalid entry, please select an available meal number from the menu:\n")
                                    for index in range(len(headings)): print(f"{index + 1}. {headings[index]}")
                                    number = input(f"\n\nPlease select a meal type from the list (1 - {len(headings)}): ")

                                heading = headings[int(number) - 1]
                                tag = tags[int(number) - 1]
                                price = prices[int(number) - 1]
                                link = anchors[int(number) - 1]
                                os.system("cls")
                                print(f"\n{heading}:\n")
                                for index in range(len(tag)): print(f"{index + 1}. {tag[index]} ({price[index]})")
                                meal = input(f"\nPlease select a meal from the {heading.title()} menu (0 [go back to menu selection] - {len(tag)}): ")

                                while meal not in self.numbers(0, len(tag)):

                                    print(f"\nInvalid entry, please choose an available number from the {heading} menu:\n")
                                    for index in range(len(tag)): print(f"{index + 1}. {tag[index]} ({price[index]})")
                                    meal = input(f"\n\nPlease select a meal option from the list above (0 [go back to menu selection] - {len(tag)}): ")

                                if (meal == "0"): another = False
                                else: another = True

                            self.driver.execute_script("arguments[0].click();", link[int(meal) - 1])
                            time.sleep(2)
                            main, options, extras, addons = self.split_cards()
                            time.sleep(2)
                            main_nameTags, main_priceTags, main_headerTags = self.website_data(main, 0)
                            main_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.variantSelect2(variant)\"]")
                            main_checkboxes = self.partition(main_anchors, main_nameTags)
                            meal_card = main_nameTags[0]
                            meal_price = main_priceTags[0]

                            if (len(meal_card) > 1):

                                os.system("cls")
                                print(f"\n{main_headerTags[0][0]}: \n\n")
                                for index in range(len(meal_card)): print(f"{index + 1}. {meal_card[index] if (meal_card[index] not in ['------', '----']) else tag[int(meal) - 1]} ({meal_price[index]})")
                                select = input(f"\n\nPlease choose one of the meal plans above (1 - {len(meal_card)}): ")

                                while select.lower().rstrip().lstrip() not in self.numbers(1, len(meal_card)):

                                    os.system("cls")
                                    print(f"\n{main_headerTags[0][0]}: \n\n")
                                    for index in range(len(meal_card)): print(f"{index + 1}. {meal_card[index] if (meal_card[index] not in ['------', '----']) else tag[int(meal) - 1]} ({meal_price[index]})")
                                    select = input(f"\n\nInvalid entry, please select an available option (1 - {len(meal_card)}): ")

                                main_tick = main_checkboxes[0][int(select) - 1]

                            if (main_tick != None): self.driver.execute_script("arguments[0].click();", main_tick), time.sleep(2)
                            main, options, extras, addons = self.split_cards()
                            option_nameTags, option_priceTags, option_headerTags = self.website_data(options, 1)
                            extra_nameTags, extra_priceTags, extra_headerTags = self.website_data(extras, 2)
                            addon_nameTags, addon_priceTags, addon_headerTags = self.website_data(addons, 3)
                            option_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('option', option_item, option)\"]")
                            extra_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('extra', extra_item, extra)\"]")
                            addon_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('addon', addon_item, addon)\"]")
                            option_checkboxes = self.partition(option_anchors, option_nameTags)
                            extra_checkboxes = self.partition(extra_anchors, extra_nameTags)
                            addon_checkboxes = self.partition(addon_anchors, addon_nameTags)
                            name_tags = [option_nameTags, extra_nameTags, addon_nameTags]
                            price_tags = [option_priceTags, extra_priceTags, addon_priceTags]
                            header_tags = [option_headerTags, extra_headerTags, addon_headerTags]
                            checkboxes = [option_checkboxes, extra_checkboxes, addon_checkboxes]

                            for address in range(len(name_tags)):

                                for index in range(len(name_tags[address])):

                                    os.system("cls")
                                    print(f"\n{header_tags[address][index][0]}: \n\n")

                                    if (len(name_tags[address][index]) == 1):

                                        print(f"{name_tags[address][index][0]} ({price_tags[address][index][0]}) \n")
                                        select = input(f"\nA: yes \nB: no \n\n")

                                        while select.lower().rstrip().lstrip() not in self.options[0:4]:

                                            os.system("cls")
                                            print(f"\n{header_tags[address][index][0]}: \n\n")
                                            print(f"{name_tags[address][index][0]} ({price_tags[address][index][0]}) \n")
                                            select = input(f"Invalid entry, please select an available option: \n\nA: yes \nB: no \n\n")

                                        if (select.lower().rstrip().lstrip() == "a"): tick = checkboxes[address][index][0]
                                        elif (select.lower().rstrip().lstrip() == "b"): tick = None
                                        checkbox.append(tick)

                                    elif ((("add" in header_tags[address][index][0].lower()) & ("extra" in header_tags[address][index][0].lower())) |
                                          (("add" in header_tags[address][index][0].lower()) & ("extra" not in header_tags[address][index][0].lower())) |
                                          (("add" not in header_tags[address][index][0].lower()) & ("extra" in header_tags[address][index][0].lower())) |
                                          ("remove" in header_tags[address][index][0].lower())):

                                        for counter in range(len(name_tags[address][index])):

                                            os.system("cls")
                                            print(f"\n{header_tags[address][index][0]}: \n\n")
                                            for count in range(len(name_tags[address][index])): print(f"{count + 1}. {name_tags[address][index][count]} ({price_tags[address][index][count]})")
                                            if ("remove" in header_tags[address][index][0].lower()): select = input(f"\n\nPlease select an option (0 [exit item removal selection] - {len(name_tags[address][index])}): ")
                                            else: select = input(f"\n\nPlease select an option (0 [exit extras selection] - {len(name_tags[address][index])}): ")

                                            while select not in self.numbers(0, len(name_tags[address][index])):

                                                os.system("cls")
                                                print(f"\n{header_tags[address][index][0]}: \n\n")
                                                for count in range(len(name_tags[address][index])): print(f"{count + 1}. {name_tags[address][index][count]} ({price_tags[address][index][count]})")
                                                if "remove" in header_tags[address][index][0].lower(): select = input(f"\n\nInvalid entry, please select an available option (0 [exit item removal selection] - {len(name_tags[address][index])}): ")
                                                else: select = input(f"\n\nInvalid entry, please select an available option (0 [exit extras selection] - {len(name_tags[address][index])}): ")

                                            if (select == "0"):

                                                tick = None
                                                checkbox.append(tick)
                                                break

                                            else:

                                                tick = checkboxes[address][index][int(select) - 1]
                                                checkbox.append(tick)
        
                                    else:

                                        for count in range(len(name_tags[address][index])): print(f"{count + 1}. {name_tags[address][index][count]} ({price_tags[address][index][count]})")
                                        select = input(f"\n\nPlease select an option (1 - {len(name_tags[address][index])}): ")

                                        while select not in self.numbers(1, len(name_tags[address][index])):

                                            os.system("cls")
                                            print(f"\n{header_tags[address][index][0]}: \n\n")
                                            for count in range(len(name_tags[address][index])): print(f"{count + 1}. {name_tags[address][index][count]} ({price_tags[address][index][count]})")
                                            select = input(f"\n\nInvalid entry, please select an available option (1 - {len(name_tags[address][index])}): ")

                                        tick = checkboxes[address][index][int(select) - 1]
                                        checkbox.append(tick)

                            os.system("cls")
                            for item in checkbox: self.driver.execute_script("arguments[0].click();", item) if (item != None) else None
                            add = self.driver.find_element_by_xpath("//span[@ng-bind-html='_mc.addToCartText()']")
                            self.driver.execute_script("arguments[0].click();", add), time.sleep(2)

                        elif (interface == "automatic"):

                            while not another:

                                os.system("cls")
                                eat = input(f"\nWhat meal are you having from {restaurant}?: ")
                                matches = [item for item in menu if eat in item.lower()]
                                headers = [item for item in headings if eat in item.lower()]
                                price_match, link_match = [], []

                                if (len(headers) > 0):

                                    for item in headers:
        
                                        address = headings.index(item)

                                        for item in tags[address]: matches.append(item) if item not in matches else None

                                for item in matches:

                                    address = menu.index(item)
                                    link_match.append(links[address])
                                    price_match.append(amount[address])

                                if (len(matches) > 1):

                                    os.system("cls")
                                    another = True
                                    print("\nHere is a list of meals matching your search request: \n\n")
                                    for index in range(len(matches)): print(f"{index + 1}. {matches[index]} ({price_match[index]})")
                                    choose = input(f"\nPlease choose an item from the search results (0 [search for a different meal] - {len(matches)}): ")

                                    while choose not in self.numbers(0, len(matches)):

                                        os.system("cls"), print()
                                        for index in range(len(matches)): print(f"{index + 1}. {matches[index]} ({price_match[index]})")
                                        choose = input(f"\n\nInvalid entry, please select an available item from the menu (0 [search for a different meal] - {len(headings)}): ")

                                    if (choose.rstrip().lstrip() == "0"):

                                        os.system("cls")
                                        another, press = False, None

                                elif (len(matches) == 1):
                                       
                                    os.system("cls")
                                    print(f"\nThere is only one meal available that matches your input request; {matches[0]} ({price_match[0]}): \n")
                                    choose = input(f"\nDo you want to add this item to your order?: \n\nA: yes \nB: no \n\n")

                                    while choose not in self.options[0:4]:

                                        os.system("cls"), print()
                                        choose = input(f"\n\nInvalid entry, please select an available option: \n\nA: add {meal[0]} to order \nB: search for a different meal \n\n")

                                    if (choose.lower().rstrip().lstrip() == "a"): another, choose = True, "1"
                                    elif (choose.lower().rstrip().lstrip() == "b"): another = False

                                elif (len(matches) == 0):

                                    os.system("cls")
                                    another, press = False, None
                                    print("\nThere are no results matching your input request, please try searching for a different meal\n")
                                    while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")

                            self.driver.execute_script("arguments[0].click();", link_match[int(choose) - 1])
                            time.sleep(2)
                            main, options, extras, addons = self.split_cards()
                            time.sleep(2)
                            main_nameTags, main_priceTags, main_headerTags = self.website_data(main, 0)
                            main_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.variantSelect2(variant)\"]")
                            main_checkboxes = self.partition(main_anchors, main_nameTags)
                            meal_card = main_nameTags[0]
                            meal_price = main_priceTags[0]

                            if (len(meal_card) > 1):

                                os.system("cls")
                                print(f"\n{main_headerTags[0][0]}: \n\n")
                                for index in range(len(meal_card)): print(f"{index + 1}. {meal_card[index] if (meal_card[index] not in ['------', '----']) else tag[int(meal) - 1]} ({meal_price[index]})")
                                select = input(f"\n\nPlease choose one of the meal plans above (1 - {len(meal_card)}): ")

                                while select.lower().rstrip().lstrip() not in self.numbers(1, len(meal_card)):

                                    os.system("cls")
                                    print(f"\n{main_headerTags[0][0]}: \n\n")
                                    for index in range(len(meal_card)): print(f"{index + 1}. {meal_card[index] if (meal_card[index] not in ['------', '----']) else tag[int(meal) - 1]} ({meal_price[index]})")
                                    select = input(f"\n\nInvalid entry, please select an available option (1 - {len(meal_card)}): ")

                                main_tick = main_checkboxes[0][int(select) - 1]

                            if (main_tick != None): self.driver.execute_script("arguments[0].click();", main_tick), time.sleep(2)
                            main, options, extras, addons = self.split_cards()
                            option_nameTags, option_priceTags, option_headerTags = self.website_data(options, 1)
                            extra_nameTags, extra_priceTags, extra_headerTags = self.website_data(extras, 2)
                            addon_nameTags, addon_priceTags, addon_headerTags = self.website_data(addons, 3)
                            option_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('option', option_item, option)\"]")
                            extra_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('extra', extra_item, extra)\"]")
                            addon_anchors = self.driver.find_elements_by_xpath("//div[@ng-click=\"_mc.activeSelect2('addon', addon_item, addon)\"]")
                            option_checkboxes = self.partition(option_anchors, option_nameTags)
                            extra_checkboxes = self.partition(extra_anchors, extra_nameTags)
                            addon_checkboxes = self.partition(addon_anchors, addon_nameTags)
                            name_tags = [option_nameTags, extra_nameTags, addon_nameTags]
                            price_tags = [option_priceTags, extra_priceTags, addon_priceTags]
                            header_tags = [option_headerTags, extra_headerTags, addon_headerTags]
                            checkboxes = [option_checkboxes, extra_checkboxes, addon_checkboxes]
                            required = self.driver.find_elements_by_css_selector("span.required.ng-binding.ng-scope")
                            select = ""
                            os.system("cls")

                            for address in range(len(name_tags)):

                                for index in range(len(name_tags[address])):

                                    if (len(name_tags[address][index]) == 1):

                                        tick = None
                                        checkbox.append(tick)

                                    elif "remove" in header_tags[address][index][0].lower():

                                        for counter in range(len(name_tags[address][index])):

                                            for item in remove:

                                                if item in name_tags[address][index][counter].lower():

                                                    tick = checkboxes[address][index][counter]
                                                    checkbox.append(tick)

                                    else:

                                        for item in required:

                                            if header_tags[address][index][0].lower().rstrip().lstrip() in item.find_element_by_xpath("..").text.replace("Require min. 1", "").lower().rstrip().lstrip():

                                                select = ""

                                                for count in range(len(name_tags[address][index])):

                                                    for drink in drinks:

                                                        if drink in name_tags[address][index][count].lower():

                                                            select = count

                                                            for exclude in types:

                                                                if exclude in name_tags[address][index][count].lower():

                                                                    break

                                                                elif ((exclude == types[-1]) & (exclude not in name_tags[address][index][count].lower())):

                                                                        select = count
                                                                        break

                                                        if (select != ""): break

                                                    if (select != ""): break
                                                
                                                if (select != ""):
                    
                                                    tick = checkboxes[address][index][int(select)]
                                                    checkbox.append(tick)
                                                    break

                                                else:

                                                    select = "0"
                                                    if (("no " in name_tags[address][index][0].lower()) | ("none" in name_tags[address][index][0].lower())): select = "1"
                                                    tick = checkboxes[address][index][int(select)]
                                                    checkbox.append(tick)
                                                    break

                                                time.sleep(10)

                            os.system("cls")
                            for item in checkbox: self.driver.execute_script("arguments[0].click();", item) if (item != None) else None
                            add = self.driver.find_element_by_xpath("//span[@ng-bind-html='_mc.addToCartText()']")
                            self.driver.execute_script("arguments[0].click();", add), time.sleep(2)

                        more = input(f"\nDo you want to add anything else to your order from this restaurant, would you like to try another restaurant or do you want to checkout and finalize your order?: \n\nA: add to order from {restaurant} \nB: add to order from another restaurant \nC: checkout \n\n")

                        while more.lower().rstrip().lstrip() not in self.options:

                            os.system("cls")
                            more = input(f"\nInvalid entry, please select an available option: \n\nA: add to order from {restaurant} \nB: add to order from another restaurant \nC: checkout \n\n")

                        if (more.lower().rstrip().lstrip() == "a"): complete, stay, page = False, True, self.driver.current_url
                        elif (more.lower().rstrip().lstrip() == "b"): complete, stay = False, False
                        elif (more.lower().rstrip().lstrip() == "c"): complete, stay = True, False

                        if (stay == False):

                            os.system("cls"), time.sleep(2)
                            finalized, count = False, 0
                            cart = self.driver.find_element_by_xpath("//button[@ng-click='_mc.goToCart()']")
                            self.driver.execute_script("arguments[0].click();", cart)
                            fetch = self.driver.find_elements_by_css_selector("span.disabled")

                            if (len(fetch) == 0):

                                button = self.driver.find_element_by_xpath("//span[@ng-click='_cart.deliveryClick()']")
                                self.driver.execute_script("arguments[0].click();", button)
                                time.sleep(2)
                                total = self.driver.find_elements_by_css_selector("span.ng-binding")[-1].text
                                hours = self.driver.find_element_by_css_selector("div.order-time.ng-scope").text
                                close = self.driver.find_elements_by_xpath("//div[@ng-click='_cart.removeItem(item)']")
                                everything = self.driver.find_elements_by_css_selector("div.first")
                                note = "NO ONIONS PLEASE  **AND**  NO GARNISH PLEASE  **AND**  NO GARLIC PLEASE  **AND**  NO GINGER PLEASE"
                                order_request = self.driver.find_element_by_xpath("//input[@ng-model='_rc.cart.restaurant.order_notes']")
                                order_request.send_keys(note)
                                card_titles = self.driver.find_elements_by_css_selector("span.title.ng-binding")
                                card_heading = [card.text for card in card_titles]
                                text_html = [item for item in everything if ((item.text not in card_heading) & (item.text != "- 1 +"))]
                                text = [item.text for item in everything if ((item.text not in card_heading) & (item.text != "- 1 +"))]
                                costs = self.driver.find_elements_by_css_selector("div.second.price")
                                subtotal = [cost.text for cost in costs if "r" in cost.text.lower()]
                                bill = [cost.text for cost in costs if cost.text not in subtotal]
                                food_tag = [[] for index in range(len(card_heading))]
                                pay_tag = [[] for index in range(len(card_heading))]
                                current = card_heading[0]
                                previous = current

                                for index in range(len(text)):

                                    try:

                                        current = text_html[index].find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_css_selector("span.title.ng-binding").text

                                        if current in card_heading:
        
                                            if (current != previous): count += 1
                                            food_tag[count].append(text[index])
                                            pay_tag[count].append(bill[index])
                                            previous = current

                                    except:


                                        current = text_html[index].find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_css_selector("span.title.ng-binding").text

                                        if current in card_heading:
        
                                            if (current != previous): count += 1
                                            food_tag[count].append(text[index])
                                            pay_tag[count].append(bill[index])
                                            previous = current

                                for counter in range(len(card_heading)):
        
                                    self.receipt(card_heading, food_tag, pay_tag, hours, subtotal, total)
                                    print("\n".join(textwrap.wrap(f"Your meal from {restaurant} will be delivered to you soon, please expect your order to arrive within the indicated time-frame", 90, break_long_words = False)))
                                    print(), print("*"*100), print("*"*100), print()
                                    if (len(card_heading) == 1): delete = input(f"\n\n\nDo you want to remove any of the items from your order? (0 [clear cart] - 1 [press enter to confirm order]): ")
                                    else: delete = input(f"\n\n\nDo you want to remove any of the items from your order? (0 [clear cart] - {len(card_heading)} [press enter to confirm order]): ")

                                    while delete.rstrip().lstrip() not in self.numbers(0, len(card_heading)) + [""]:

                                        self.receipt(card_heading, food_tag, pay_tag, hours, subtotal, total)
                                        print("\n".join(textwrap.wrap(f"Your meal from {restaurant} will be delivered to you soon, please expect your order to arrive within the indicated time-frame", 90, break_long_words = False)))
                                        print(), print("*"*100), print("*"*100), print()
                                        if (len(card_heading) == 1): delete = input(f"\n\nInvalid entry, please select an available option (0 [clear cart] - 1 [press enter to confirm order])?: ")
                                        else: delete = input(f"\n\nInvalid entry, please choose an available item to remove from your order (0 [clear cart] - {len(card_heading)} [press enter to confirm order])?: ")

                                    if (delete.rstrip().lstrip() == "0"):

                                        for x in close: self.driver.execute_script("arguments[0].click();", x)
                                        card_heading, subtotal = [], []
                                        food_tag, pay_tag = [], []
                                        close = []
                                        break

                                    elif (delete.rstrip().lstrip() != ""):

                                        delete = delete.rstrip().lstrip()
                                        X = close[int(delete) - 1]
                                        self.driver.execute_script("arguments[0].click();", X)
                                        card_heading.pop(int(delete) - 1), subtotal.pop(int(delete) - 1)
                                        food_tag.pop(int(delete) - 1), pay_tag.pop(int(delete) - 1)
                                        close.pop(int(delete) - 1)
                                        time.sleep(2)
                                        total = self.driver.find_elements_by_css_selector("span.ng-binding")[-1].text
                                        hours = self.driver.find_element_by_css_selector("div.order-time.ng-scope").text

                                    if (delete.rstrip().lstrip() == ""): break

                                verify = self.driver.find_elements_by_xpath("//span[@class=\"ready-reason ng-binding ng-scope\"]")

                                if ((len(card_heading) > 0) & (len(verify) == 0)):

                                    os.system("cls")
                                    confirm = self.driver.find_element_by_css_selector("button.submit-button.submit-button-narrower.submit-button-loader.ng-scope")
                                    time.sleep(2)
                                    self.driver.execute_script("arguments[0].click();", confirm), time.sleep(2)
                                    time.sleep(5)
                                    house = self.driver.find_element_by_xpath("//input[@name=\"street_number\"]")
                                    house.send_keys(self.address.split()[0])
                                    building = self.driver.find_element_by_xpath("//a[@title=\"House\"]")
                                    self.driver.execute_script("arguments[0].click();", building)
                                    payment = self.driver.find_element_by_id("cash")
                                    self.driver.execute_script("arguments[0].click();", payment)

                                    try:

                                        tip = self.driver.find_element_by_xpath("//input[@ng-model=\"_rc.variables.tip_percentage\"]")
                                        self.driver.execute_script("arguments[0].click();", tip)

                                    except:

                                        pass

                                    finalize = self.driver.find_element_by_xpath("//button[@ng-click=\"_checkout.initiatePayment()\"]")
                                    self.driver.execute_script("arguments[0].click();", finalize)

                                elif ((stay == False) & (len(verify) > 0)):

                                    os.system("cls")
                                    press = None
                                    for x in close: self.driver.execute_script("arguments[0].click();", x)
                                    print(f"\nYour order will now be cancelled and you will be taken back to select a menu from a another restaurant because {verify[0].text.lower().replace('min', 'minimum')} \n")
                                    while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")

                                elif ((stay == True) & (len(verify) > 0)):

                                    os.system("cls")
                                    press = None
                                    print(f"\nYou will now be taken back to the {restaurant} menu to schedule another order because {verify[0].text.lower().replace('min', 'minimum')} \n")
                                    while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")

                                elif (len(card_heading) == 0):

                                    os.system("cls")
                                    press = None
                                    if (stay == False): print(f"\nYour order will now be cancelled and you will be taken back to select a menu from a another restaurant because your cart is empty \n")
                                    else: print(f"\nYou will now be taken back to the {restaurant} menu to schedule another order because your cart is empty \n")
                                    while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")


                            elif (fetch[0].text.lower().rstrip().lstrip() == "mr d delivery"):

                                os.system("cls")
                                print(f"\nMr D has no drivers currently available to fetch your meal and so your order must be collected from {restaurant} instead, which requires your credit card details\n")
                                more = input(f"\nWould you like to place an order from another restaurant or do you want to exit the program?: \n\nA: try a different restaurant \nB: exit \n\n")

                                while more.lower().rstrip().lstrip() not in self.options[0:4]:

                                    os.system("cls")
                                    more = input(f"\nInvalid entry, please select an available option: \n\nA: try another eatery \nB: exit \n\n")

                                if (more.lower().rstrip().lstrip() == "a"): complete, stay = False, False
                                elif (more.lower().rstrip().lstrip() == "b"): complete, stay = True, False

                                if (complete == False):

                                    os.system("cls")
                                    press = None
                                    print(f"\nYour order from {restaurant} will now be cancelled and you will be taken back to select a menu from a another restaurant\n")
                                    while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")

            self.driver.quit()

        else: 

            os.system("cls")
            press = None
            print("\nSorry, but there are no eateries available in your area at this hour \n")
            while (press == None): press = input("HIT ENTER TO CONTINUE....\n\n")


    def split_cards(self):

        main_card = '<div class="variant">'
        option_card = '<div class="variant options ng-scope" ng-repeat="option in _mc.activeVariant.options">'
        extra_card = '<div class="variant extras ng-scope" ng-repeat="extra in _mc.activeVariant.extras">'
        addon_card = '<div class="variant addons ng-scope" ng-repeat="addon in _mc.activeVariant.addons">'
        website = str(self.driver.page_source)
        main = website.split(main_card)
        main = main[0:-1] + [main[-1].split(option_card)[0]]
        options = website.split(option_card)
        options = options[0:-1] + [options[-1].split(extra_card)[0]]
        extras = website.split(extra_card)
        extras = extras[0:-1] + [extras[-1].split(addon_card)[0]]
        addons = website.split(addon_card)
        main.pop(0), options.pop(0), extras.pop(0), addons.pop(0)

        if (len(options) == 0):

            main = website.split(main_card)
            main = main[0:-1] + [main[-1].split(extra_card)[0]]
            options = website.split(option_card)
            options = options[0:-1] + [options[-1].split(extra_card)[0]]
            extras = website.split(extra_card)
            extras = extras[0:-1] + [extras[-1].split(addon_card)[0]]
            addons = website.split(addon_card)
            main.pop(0), options.pop(0), extras.pop(0), addons.pop(0)

        return main, options, extras, addons


    def receipt(self, titles, tags, prices, duration, subtotals, total):

        os.system("cls")
        print(), print("*"*100), print()
        print("PLEASE CONFIRM YOUR ORDER:")
        print(), print("*"*100)

        for index in range(len(titles)):

            print("*"*100), print()
            print(f"{index + 1}. {titles[index]}:\n\n")
            for address in range(len(tags[index])): print(f"{tags[index][address] if (tags[index][address] not in ['------', '----']) else titles[index]} ({prices[index][address]})")
            print(f"\nSUBTOTAL: {subtotals[index]}\n")

        print("*"*100), print("*"*100), print()
        print("TOTAL COST:", total), print()
        print(duration)
        print(), print("*"*100), print("*"*100), print()


    def website_data(self, cards, indicator):

        previous = ""
        collect_tags, collect_prices, collect_titles = [], [], []
        mainPrice_tag = '<span class="number ng-binding ng-scope" ng-if="!variant.old_price&amp;&amp;variant.price > 0" ng-class="{\'red\': variant.menu_deal_action === \'buy_1_get_1_free\'}">'
        discountPrice_tag = '<span class="new-price ng-binding">'
        optionPrice_tag = '<span class="number ng-binding" ng-class="{\'hidden\' : option_item.price == 0, \'hidden\' : option_item.availability.status == \'sold_out\'}">'
        extraPrice_tag = '<span class="number ng-binding" ng-class="{\'hidden\' : extra_item.price == 0, \'hidden\' : extra_item.availability.status == \'sold_out\'}">'
        addonPrice_tag = '<span class="number ng-binding" ng-class="{\'hidden\' : addon_item.price == 0, \'hidden\' : addon_item.availability.status == \'sold_out\'}">'
        name_tag = '<span class="name ng-binding">'
        main_heading = '<div class="variant-heading">'
        option_heading = '<span class="description ng-binding ng-scope" ng-if="option.label">'
        extra_heading = '<span class="description ng-binding ng-scope" ng-if="extra.label">'
        addon_heading = '<span class="description ng-binding ng-scope" ng-if="addon.label">'
        tag_start, title_start = name_tag, main_heading
        tag_end, title_end = "</span>", "</div>"
        if (indicator == 0): price_start, price_end = [mainPrice_tag, discountPrice_tag], ["</span>", "</span>"]
        elif (indicator == 1): price_start, price_end = optionPrice_tag, "</span>"
        elif (indicator == 2): price_start, price_end = extraPrice_tag, "</span>"
        elif (indicator == 3): price_start, price_end = addonPrice_tag, "</span>"

        for index in range(len(cards)):

            with open(f"webpage{index}.txt", "w+", encoding = "utf-8") as file:

                tags, prices, titles = [], [], []
                page = cards[index]
                file.write(page)
                file.seek(0)

                for line in file:

                    tag, title, price = line, line, line
                    try: tag = line.split(tag_start)[1].split(tag_end)[0]
                    except: pass

                    try:

                        if (((discountPrice_tag in line) & (indicator == 0)) | 
                              ((mainPrice_tag in line) & (indicator == 0))):

                            for address in range(len(price_start)):

                                test = line.split(price_start[address])[-1].split(price_end[address])[0]

                                if (test[-1].isdigit() == True): 

                                    price = test
                                    break

                        elif ((extraPrice_tag in previous) & (indicator == 2)): price = line.lstrip().rstrip()
                        elif ((addonPrice_tag in previous) & (indicator == 3)): price = line.lstrip().rstrip()
                        else: price = line.split(price_start)[1].split(price_end)[0]

                    except: 

                        pass

                    try:

                        if option_heading in previous: title = line.lstrip().replace("\n", "")
                        elif extra_heading in previous: title = line.lstrip().replace("\n", "")
                        elif addon_heading in previous: title = line.lstrip().replace("\n", "")
                        else: title = line.split(title_start)[1].split(title_end)[0]

                    except: 

                        pass

                    if (tag != line): tags.append(tag.replace("&amp;", "&"))
                    if ((price != line) | (extraPrice_tag in previous)): prices.append(price) if (price[-1].isdigit() == True) else None
                    if ((title != line) | (option_heading in previous)): titles.append(title) if ((title != "\n") & (title != "Quantity")) else None
                    previous = line

            if (len(tags) != 0): collect_tags.append(tags)
            if (len(prices) != 0): collect_prices.append(prices)
            if (len(titles) != 0): collect_titles.append(titles)

        return collect_tags, collect_prices, collect_titles


    def partition(self, array, target):

        matrix = []

        for component in target:

            end = len(component)
            matrix.append(array[0:end])
            for index in range(end): array.pop(0)

        return matrix




if __name__ == "__main__":

    # sign up to Mr D Food and get a username and password
    path = os.getcwd() + "\\chromedriver" # place the chromium driver in the same folder as this program
    admin = "" # Mr D Food account email
    password = "" # Mr D Food account password
    waiter =  OrderFood(path, admin, password)
    waiter.mrDFood()
    os.system("cls")
    waiter.driver.quit()
