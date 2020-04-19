from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import sys
import time
import os

Debug = False

driver = None
wait = None

def __initialize():
    global driver
    global wait
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=2000x2000")
    if (not Debug): chrome_options.add_argument("--log-level=3")
    chrome_driver = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    wait = WebDriverWait(driver, 10)

def close():
    global driver
    driver.close()


def certcheck():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=2000x2000")
    chrome_driver = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get("https://cacert.org/")
    if (Debug): print(driver.page_source)
    driver.close()

def multi_scrape(username, password, website, url, delay=5):
    if (Debug): print("Start of switch")
    global driver
    if (driver == None): __initialize()

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
    global driver
    if (driver == None): __initialize()
    driver.get(url)
    time.sleep(delay)
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    return scraped


def __pixiv_scrape(username, password, url, delay):
    """Scrapes the pixiv url after logging in with the username and password"""
    global driver
    global wait

    try:
        driver.get("https://accounts.pixiv.net/login")
        if ((wait.until(EC.title_contains("Login | pixiv"))) or (wait.until(EC.title_contains("[pixiv]")))):
            if (EC.title_contains("Login | pixiv")):
                username_field = driver.find_element_by_xpath("//input[@autocomplete='username']")
                password_field = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                wait.until(EC.title_contains("[pixiv]"))
    except Exception as err:
        __print_error(err)

    if (driver.current_url != url): driver.get(url)
    time.sleep(delay)
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    return scraped

def __newgrounds_scrape(username, password, url, delay):
    global driver
    global wait

    try:
        driver.get("https://www.newgrounds.com/passport")
        if ((wait.until(EC.title_contains("Newgrounds Passport"))) or (wait.until(EC.title_contains("Your Feed")))):
            if (EC.title_contains("Newgrounds Passport")):
                username_field = driver.find_element_by_id("username")
                password_field = driver.find_element_by_id("password")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                wait.until(EC.title_contains("Your Feed"))
    except Exception as err:
        __print_error(err)

    if (driver.current_url != url): driver.get(url)
    time.sleep(delay)
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    if (Debug): print(scraped)
    return scraped

def __twitter_scrape(username, password, url, delay):
    global driver
    global wait
    
    try:
        driver.get("https://twitter.com/login")
        if ((wait.until(EC.presence_of_element_located((By.NAME,"session[username_or_email]"))))\
            or (wait.until(EC.title_contains("Home / Twitter")))):
            if (EC.presence_of_element_located((By.NAME,"session[username_or_email]"))):
                username_field = driver.find_element_by_name("session[username_or_email]")
                password_field = driver.find_element_by_name("session[password]")
                username_field.send_keys(username)
                password_field.send_keys(password)
                password_field.submit()
                wait.until(EC.title_contains("Home / Twitter"))
    except Exception as err:
        __print_error(err)

    if (driver.current_url != url): driver.get(url)
    time.sleep(delay)
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    if (Debug): print(scraped)
    return scraped

def __print_error(err):
    global driver
    print("~~~~~~ ERROR ~~~~~~")
    print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
    traceback.print_tb(sys.exc_info()[2])
    if (driver != None): print(driver.title)
    print("~~~~~~~~~~~~~~~~~~~")