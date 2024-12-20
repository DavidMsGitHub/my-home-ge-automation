from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

with open("config.json", "r", encoding="utf-8") as cfg:
    json_string = json.load(cfg)
    webdriver_location = json_string["webdriver-location"]

path_to_driver = webdriver_location
def cdriver():
    chromedriver_path = path_to_driver

    service = Service(chromedriver_path)
    chrome_options = Options()

    chrome_options.binary_location = "chrome-win64/chrome.exe"
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
def wait_until_clickable_xpath(xpath, time, driver):
    gela = WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    return gela

def wait_until_id(time, driver, id):
    gela = WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.ID, id))
    )
    return gela



def wait_until_xpath(time, driver, xpath):
    gela = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return gela


def wait_until_cs(cssselector, time, driver):
    gela = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cssselector))
    )
    return gela