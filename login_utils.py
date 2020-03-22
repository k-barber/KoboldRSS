from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

Debug = True

def certcheck():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")
    chrome_driver = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get("https://cacert.org/")
    print(driver.page_source)
    driver.close()

def multi_scrape(username, password, website, url):
    if (Debug): print("Start of switch")

    if (website == "Newgrounds"):
        result = newgrounds_scrape(username, password, url)
    elif (website == "Pixiv"):
        result = pixiv_scrape(username, password, url)
    elif (website == "Twitter"):
        result = twitter_scrape(username, password, url)
    else:
        result = "Test"

    if (Debug): print("End of Switch")

    if (Debug): print(result)

    return result


def pixiv_scrape(username, password, url):
    """Scrapes the pixiv url after logging in with the username and password"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")

    chrome_driver = os.path.join(os.getcwd(), "chromedriver")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

    wait = WebDriverWait(driver, 10)

    driver.get("https://accounts.pixiv.net/login")
    assert "Login".lower() in driver.title.lower()
    
    username_field = driver.find_element_by_xpath("//input[@autocomplete='username']")
    password_field = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()

    wait.until(EC.title_is("[pixiv]"))

    driver.get(url)
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    driver.close()
    return scraped

def newgrounds_scrape(username, password, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")

    chrome_driver = os.path.join(os.getcwd(), "chromedriver")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

    wait = WebDriverWait(driver, 10)

    driver.get("https://www.newgrounds.com/passport")
    if (Debug): driver.get_screenshot_as_file("login.png")
    assert "Passport".lower() in driver.title.lower()
    
    username_field = driver.find_element_by_id("username")
    password_field = driver.find_element_by_id("password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()

    wait.until(EC.title_is("Your Feed"))

    driver.get(url)

    if (Debug): driver.get_screenshot_as_file("feed.png")
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    driver.close()
    if (Debug): print(scraped)
    return scraped

def twitter_scrape(username, password, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1024x1400")

    chrome_driver = os.path.join(os.getcwd(), "chromedriver")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

    wait = WebDriverWait(driver, 10)

    driver.get("https://twitter.com/login")
    if (Debug): driver.get_screenshot_as_file("get.png")
    wait.until(EC.presence_of_element_located((By.NAME,"session[username_or_email]")))
    if (Debug): driver.get_screenshot_as_file("login.png")
    assert "login".lower() in driver.title.lower()
    
    username_field = driver.find_element_by_name("session[username_or_email]")
    password_field = driver.find_element_by_name("session[password]")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))

    # Wait 5 seconds for content to load. I could get more specific, but it might not hold up for pages other than twitter.com/home
    time.sleep(5)
    assert "home".lower() in driver.title.lower()

    if (Debug): driver.get_screenshot_as_file("feed.png")
    scraped = driver.execute_script("return document.documentElement.outerHTML")
    driver.close()
    if (Debug): print(scraped)
    return scraped