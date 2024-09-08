from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

with open("config.json", "r") as cfg:
    json_string = json.load(cfg)
    webdriver_location = json_string["webdriver-location"]

path_to_driver = webdriver_location
def cdriver():
    chromedriver_path = path_to_driver
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service)
    return driver