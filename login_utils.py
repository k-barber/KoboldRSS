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

class Login_Utils:

    Debug = None
    logged_in = None
    driver = None
    wait = None

    def __init__(self, debug):
        self.Debug = debug
        self.logged_in = []

    def __initialize():
        """Initializes the headless chrome instance
        """
        self.driver
        self.wait
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=2000x2000")
        home = str(Path.home())
        default_profile = "user-data-dir=" + home + "\\AppData\\Local\\Google\\Chrome\\User Data\\"
        chrome_options.add_argument(default_profile)
        if (not Debug): chrome_options.add_argument("--log-level=3")
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        self.wait = WebDriverWait(self.driver, 5)

    def close():
        """Closes the headless chrome instance
        """
        self.driver.close()


    def certcheck():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=2000x2000")
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        self.driver.get("https://cacert.org/")
        if (Debug): print(self.driver.page_source)
        self.driver.close()

    def multi_scrape(username, password, website, url, delay=5):
        """Scrapes the html from URL
        
        Parameters:

        username (str):  The username to login with

        password (str):  The password to login with

        website (str):  The website the page is on

        url (str):  The url to scrape
        """
        if (Debug): print("Start of switch")
        if (self.driver == None): __initialize()

        if (website == "Newgrounds"):
            result = __newgrounds_scrape(username, password, url, delay)
        elif (website == "Pixiv"):
            result = __pixiv_scrape(username, password, url, delay)
        elif (website == "Twitter"):
            result = __twitter_scrape(username, password, url, delay)
        else:
            result = "Test"

        if (Debug): print("End of Switch")

        if (Debug): print(result)

        return result

    def generic_scrape(url, delay):
        """Scrapes the html from URL
        
        Parameters:

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """
        if (self.driver == None): __initialize()
        self.driver.get(url)
        time.sleep(delay)
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped


    def __pixiv_scrape(username, password, url, delay):
        """Scrapes the html from the pixiv URL
        
        Parameters:

        username (str):  The username to login with

        password (str):  The password to login with

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """

        if ("pixiv" not in logged_in):
            try:
                self.driver.get("https://accounts.pixiv.net/login")
                username_field = self.driver.find_element_by_xpath("//input[@autocomplete='username']")
                password_field = self.driver.find_element_by_xpath("//input[@autocomplete='current-password']")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                self.wait.until(EC.title_contains("[pixiv]"))
                self.logged_in.append("pixiv")
            except Exception as err:
                if (EC.title_contains("[pixiv]")):
                    self.logged_in.append("pixiv")
                else:
                    __print_error(err)
        
        if (self.driver.current_url != url): self.driver.get(url)
        time.sleep(delay)
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped

    def __newgrounds_scrape(username, password, url, delay):
        """Scrapes the html from the newgrounds URL
        
        Parameters:

        username (str):  The username to login with

        password (str):  The password to login with

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """

        if ("newgrounds" not in logged_in):
            try:
                self.driver.get("https://www.newgrounds.com/passport")
                self.wait.until(EC.title_contains("Newgrounds Passport"))
                username_field = self.driver.find_element_by_id("username")
                password_field = self.driver.find_element_by_id("password")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                self.wait.until(EC.title_contains("Your Feed"))
                self.logged_in.append("newgrounds")
            except Exception as err:
                if (EC.title_contains("Your Feed")):
                    self.logged_in.append("newgrounds")
                else:
                    __print_error(err)

        if (self.driver.current_url != url): self.driver.get(url)
        time.sleep(delay)
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped

    def __twitter_scrape(username, password, url, delay):
        """Scrapes the html from the twitter URL
        
        Parameters:

        username (str):  The username to login with

        password (str):  The password to login with

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """

        if ("twitter" not in logged_in):
            try:
                self.driver.get("https://twitter.com/login")
                self.wait.until(EC.presence_of_element_located((By.NAME,"session[username_or_email]")))
                username_field = self.driver.find_element_by_name("session[username_or_email]")
                password_field = self.driver.find_element_by_name("session[password]")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                self.wait.until(EC.title_contains("Home / Twitter"))
                self.logged_in.append("twitter")
            except Exception as err:
                if (EC.title_contains("Home / Twitter")):
                    self.logged_in.append("twitter")
                else:
                    __print_error(err)

        if (self.driver.current_url != url): self.driver.get(url)
        time.sleep(delay)
        scraped = self.driver.execute_script("return document.documentElement.outerHTML")
        return scraped

    def __print_error(err):
        print("~~~~~~ ERROR ~~~~~~")
        print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        traceback.print_tb(sys.exc_info()[2])
        if (driver != None): print(self.driver.title)
        print("~~~~~~~~~~~~~~~~~~~")