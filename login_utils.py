from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import pickle
import traceback
import sys
import time
import os

class ChromeWindow:

    debug_mode = False
    logged_in = None
    driver = None
    wait = None
    shell = None

    def log(self, text):
        self.shell.print_generator_output(text)

    def __init__(self, debug_mode, shell):
        self.debug_mode = debug_mode
        self.logged_in = []
        self.shell = shell

    def __initialize(self, force_debug = False):
        """Initializes the headless chrome instance
        """
        self.driver
        self.wait
        chrome_options = Options()
        self.log("Utils Debug mode: " + str(self.debug_mode))
        if (self.debug_mode): self.log("Initializing Chrome")
        if (self.debug_mode == False and force_debug == False):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=2000,2000")
        chrome_options.add_argument("--enable-file-cookies")
        home = str(Path.home())
        default_profile = "user-data-dir=" + home + "\\AppData\\Local\\Google\\Chrome\\User Data"
        chrome_options.add_argument(default_profile)
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        if (self.is_aborted()): return
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def start(self):
        if self.driver is None:
            if (self.is_aborted()): return False
            self.__initialize()
        if self.driver is not None:
            return True
        else:
            return False

    def login_check(self, channels):
        websites = []
        for channel in channels:
            if channel.website is not None and channel.website not in websites and channel.website not in self.logged_in:
                websites.append(channel.website)
        print(websites)
        logged_out = []
        if len(websites) > 0 :
            if (self.is_aborted()): return
            self.start()
            print("Login Check")
            for website in websites:
                print(website)
                if (self.is_aborted()): return
                if (not self.is_logged_in(website)):
                    print("Not Logged in")
                    logged_out.append(website)
        if len(logged_out) > 0:
            if (self.debug_mode == False):
                self.driver.close()
                self.driver = None
                time.sleep(5)
                self.__initialize(True)
            for website in logged_out:
                if (self.is_aborted()): return
                self.manual_login(website)
            if (self.debug_mode == False):
                self.driver.close()
                self.driver = None
            self.login_check(channels)
        
                    
    def manual_login(self, website):
        self.driver.switch_to.window(self.driver.current_window_handle)
        print('\a') # prints ASCII bell sound
        self.wait = WebDriverWait(self.driver, 300) #Set wait to 300 seconds
        if (self.is_aborted()): return
        try:
            if (website == "Newgrounds"):
                self.driver.get("https://www.newgrounds.com/social")
                self.wait.until(EC.title_is("Your Feed"))
                pickle.dump(self.driver.get_cookies(), open("cookies/newgrounds.pkl", "wb"))
            elif (website == "Pixiv"):
                self.driver.get("https://www.pixiv.net/setting_profile.php")
                self.wait.until(EC.title_contains("Settings: Profile"))
                pickle.dump(self.driver.get_cookies(), open("cookies/pixiv.pkl", "wb"))
            elif (website == "Twitter"):
                self.driver.get("https://twitter.com/login")
                self.wait.until(EC.title_contains("Home / Twitter"))
                pickle.dump(self.driver.get_cookies(), open("cookies/pixiv.pkl", "wb"))
            self.wait = WebDriverWait(self.driver, 5)
        except Exception as err:
            self.log("Failed to log in to " + website)
            self.log("Shutting down generator")
            self.shell.stop_generator()
        
    def is_logged_in(self, website):
        if website not in self.logged_in:
            try:
                if (website == "Newgrounds"):
                    if (self.is_aborted()): return
                    self.driver.get("https://www.newgrounds.com/social")
                    if (self.is_aborted()): return
                    if (os.path.isfile("cookies/newgrounds.pkl")):
                        for cookie in pickle.load(open("cookies/newgrounds.pkl", "rb")):
                            self.driver.add_cookie(cookie)
                    self.driver.get("https://www.newgrounds.com/social")
                    self.wait.until(EC.title_is("Your Feed"))
                elif (website == "Pixiv"):
                    if (self.is_aborted()): return
                    self.driver.get("https://www.pixiv.net/setting_profile.php")
                    if (self.is_aborted()): return
                    if (os.path.isfile("cookies/pixiv.pkl")):
                        for cookie in pickle.load(open("cookies/pixiv.pkl", "rb")):
                            self.driver.add_cookie(cookie)
                    self.driver.get("https://www.pixiv.net/setting_profile.php")
                    self.wait.until(EC.title_contains("Settings: Profile"))
                elif (website == "Twitter"):
                    if (self.is_aborted()): return
                    self.driver.get("https://twitter.com/login")
                    if (self.is_aborted()): return
                    if (os.path.isfile("cookies/twitter.pkl")):
                        for cookie in pickle.load(open("cookies/twitter.pkl", "rb")):
                            self.driver.add_cookie(cookie)
                    self.driver.get("https://twitter.com/login")
                    self.wait.until(EC.title_contains("Home / Twitter"))
                    pickle.dump(self.driver.get_cookies(), open("cookies/twitter.pkl", "wb"))
                else:
                    self.log("Unknown website")
                    return False
                self.logged_in.append(website)
                return True
            except Exception as err:
                print(self.driver.title)
                return False
        else:
            return True

    def close(self):
        """Closes the headless chrome instance
        """
        if self.driver is not None:
            self.driver.close()
        self.logged_in = []
        self.driver = None
        self.shell.chrome_stopped_signal.set()

    def certcheck(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=2000x2000")
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        if (self.is_aborted()): return
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        if (self.is_aborted()): return
        self.driver.get("https://cacert.org/")
        if (self.debug_mode): self.log(self.driver.page_source)
        self.driver.close()

    def generic_scrape(self, url, delay):
        """Scrapes the html from URL
        
        Parameters:

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """
        if (self.debug_mode): self.log("Starting scrape")
        if (self.is_aborted()): return
        if (self.driver == None): self.__initialize()
        if (self.is_aborted()): return
        self.driver.get(url)
        time.sleep(1)
        height = self.driver.execute_script("return document.body.scrollHeight")
        x = 0
        while x < height:
            time.sleep(0.05)
            self.driver.execute_script("window.scrollTo(0, " + str(x) +");")
            x = x + 100
        time.sleep(0.05)
        if (self.is_aborted()): return
        while x > 0:
            time.sleep(0.05)
            self.driver.execute_script("window.scrollTo(0, " + str(x) +");")
            x = x - 100
        time.sleep(1)
        if (self.is_aborted()): return
        if delay is not None: time.sleep(delay)
        if (self.is_aborted()): return
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped
    
    def is_aborted(self):
        if (self.shell.stop_signal.is_set()):
            self.close()
            return 1
        else: 
            return 0
