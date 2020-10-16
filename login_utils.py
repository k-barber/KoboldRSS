from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
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
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1280,720")
        home = str(Path.home())
        default_profile = "user-data-dir=" + home + "\\AppData\\Local\\Google\\Chrome\\User Data"
        chrome_options.add_argument(default_profile)
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def start(self):
        if self.driver is None:
            self.__initialize()
        if self.driver is not None:
            return True
        else:
            return False

    def login_check(self, channels):
        websites = []
        for channel in channels:
            if channel.website is not None and channel.website not in websites:
                websites.append(channel.website)
        print(websites)
        logged_out = []
        if len(websites) > 0 :
            self.start()
            print("Login Check")
            for website in websites:
                print(website)
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
                self.manual_login(website)
        if (self.debug_mode == False):
            self.driver.close()
            self.driver = None
        
                    
    def manual_login(self, website):
        self.driver.switch_to.window(self.driver.current_window_handle)
        print('\a') # prints ASCII bell sound
        self.wait = WebDriverWait(self.driver, 300) #Set wait to 300 seconds
        try:
            if (website == "Newgrounds"):
                self.driver.get("https://www.newgrounds.com/social")
                self.wait.until(EC.title_is("Your Feed"))
            elif (website == "Pixiv"):
                self.driver.get("https://www.pixiv.net/setting_profile.php")
                self.wait.until(EC.title_contains("Settings: Profile"))
            elif (website == "Twitter"):
                self.driver.get("https://twitter.com/login")
                self.wait.until(EC.title_contains("Home / Twitter"))
            self.wait = WebDriverWait(self.driver, 5)
            self.logged_in.append(website)
        except Exception as err:
            self.log("Failed to log in to " + website)
            self.log("Shutting down generator")
            self.shell.stop_generator()
        
    def is_logged_in(self, website):
        if website not in self.logged_in:
            try:
                if (website == "Newgrounds"):
                    self.driver.get("https://www.newgrounds.com/social")
                    self.wait.until(EC.title_is("Your Feed"))
                elif (website == "Pixiv"):
                    self.driver.get("https://www.pixiv.net/setting_profile.php")
                    self.wait.until(EC.title_contains("Settings: Profile"))
                elif (website == "Twitter"):
                    self.driver.get("https://twitter.com/login")
                    self.wait.until(EC.title_contains("Home / Twitter"))
                else:
                    self.log("Unknown website")
                    return False
                self.logged_in.append(website)
                return True
            except Exception as err:
                print(self.driver.title)
                return False

    def close(self, chrome_stopped_signal):
        """Closes the headless chrome instance
        """
        self.driver.close()
        self.driver = None
        chrome_stopped_signal.set()

    def certcheck(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=2000x2000")
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
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
        if (self.driver == None): self.__initialize()
        self.driver.get(url)
        time.sleep(5)
        if delay is not None: time.sleep(delay)
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped