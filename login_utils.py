from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils import *
from urllib import parse
import pickle
import time
import os


class BrowserWindow:

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

    def __initialize(self, force_debug=False):
        """Initializes the headless browser instance"""
        try:
            self.driver
            self.wait
            driver_options = Options()
            if self.debug_mode == False and force_debug == False:
                driver_options.headless = True
            self.driver = webdriver.Firefox(
                service_log_path=os.devnull, options=driver_options
            )
            self.wait = WebDriverWait(self.driver, 5)
        except Exception as err:
            self.log("Error starting browser")
            self.log((str(err) + "\n"))
        

    def start(self):
        if self.driver is None:
            if self.is_aborted():
                return False
            self.__initialize()
        if self.driver is not None:
            return True
        else:
            return False

    def login_check(self, channels):
        websites = {}
        for channel in channels:
            if channel.logged_URL is not None:
                domain = parse.urlparse(channel.logged_URL).netloc
                if domain not in websites.keys() and domain not in self.logged_in:
                    websites[domain] = (
                        domain,
                        channel.logged_URL,
                        channel.logged_title,
                    )
        logged_out = []
        if len(websites) > 0:
            if self.is_aborted():
                return
            self.start()
            self.log("Login Check:")
            for domain in websites.keys():
                self.log(domain)
                if self.is_aborted():
                    return
                if not self.is_logged_in(websites[domain]):
                    logged_out.append(websites[domain])
        if len(logged_out) > 0:
            if self.debug_mode == False:
                self.driver.close()
                self.driver = None
                time.sleep(5)
                self.__initialize(True)
            for website in logged_out:
                if self.is_aborted():
                    return
                self.manual_login(website)
            if self.debug_mode == False:
                self.driver.close()
                self.driver = None
            self.login_check(channels)

    def manual_login(self, website):
        domain = website[0]
        url = website[1]
        title = website[2]
        self.driver.switch_to.window(self.driver.current_window_handle)
        print("\a")  # prints ASCII bell sound
        self.wait = WebDriverWait(self.driver, 300)  # Set wait to 300 seconds
        if self.is_aborted():
            return
        try:
            self.driver.get(url)
            self.wait.until(EC.title_is(title))
            create_folders_to_file("cookies/" + str(domain))
            pickle.dump(
                self.driver.get_cookies(), open("cookies/" + str(domain) + ".pkl", "wb")
            )
            self.wait = WebDriverWait(self.driver, 5)
            self.wait = WebDriverWait(self.driver, 5)
        except Exception as err:
            print("\a")  # prints ASCII bell sound
            self.log("Failed to log in to " + domain)
            self.log("Shutting down generator")
            self.shell.stop_generator()

    def is_logged_in(self, website):
        domain = website[0]
        url = website[1]
        title = website[2]
        if domain not in self.logged_in:
            try:
                if self.is_aborted():
                    return
                self.driver.get(url)
                if self.is_aborted():
                    return
                if os.path.isfile("cookies/" + str(domain) + ".pkl"):
                    for cookie in pickle.load(
                        open("cookies/" + str(domain) + ".pkl", "rb")
                    ):
                        self.driver.add_cookie(cookie)
                if self.is_aborted():
                    return
                self.driver.get(url)
                if self.is_aborted():
                    return
                self.wait.until(EC.title_is(title))
                pickle.dump(
                    self.driver.get_cookies(),
                    open("cookies/" + str(domain) + ".pkl", "wb"),
                )
                self.logged_in.append(domain)
                return True
            except Exception as err:
                self.log("Not logged in: " + str(domain))
                return False
        else:
            return True

    def close(self):
        """Closes the headless browser instance"""
        if self.driver is not None:
            self.driver.close()
        self.logged_in = []
        self.driver = None
        self.shell.browser_stopped_signal.set()

    def generic_scrape(self, url, delay):
        """Scrapes the html from URL

        Parameters:

        url (str):  The url to scrape

        delay (int): How many seconds selenium should wait before scraping
        """
        if self.debug_mode:
            self.log("Starting scrape")
        if self.is_aborted():
            return
        if self.driver == None:
            self.__initialize()
        if self.is_aborted():
            return
        self.driver.get(url)
        time.sleep(1)
        height = self.driver.execute_script("return document.body.scrollHeight")
        x = 0
        while x < height:
            time.sleep(0.05)
            self.driver.execute_script("window.scrollTo(0, " + str(x) + ");")
            x = x + 100
        time.sleep(0.05)
        if self.is_aborted():
            return ""
        while x > 0:
            time.sleep(0.05)
            self.driver.execute_script("window.scrollTo(0, " + str(x) + ");")
            x = x - 100
        time.sleep(1)
        if self.is_aborted():
            return ""
        if delay is not None:
            time.sleep(delay)
        if self.is_aborted():
            return ""
        scraped = self.driver.execute_script(
            "return document.documentElement.outerHTML"
        )
        return scraped

    def is_aborted(self):
        if self.shell.generator_stop_signal.is_set():
            self.close()
            return 1
        else:
            return 0
