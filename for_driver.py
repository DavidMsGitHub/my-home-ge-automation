from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import json
import base64
with open("config.json", "r", encoding="utf-8") as cfg:
    encoded_config = json.load(cfg)["encoded_data"]
    decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

    mhemail = decoded_config["credentials"]["myhome"]["email"]
    mhpassword = decoded_config["credentials"]["myhome"]["password"]
    ssemail = decoded_config["credentials"]["ss.ge"]["email"]
    sspassword = decoded_config["credentials"]["ss.ge"]["password"]
    contact_name = decoded_config["contact"]["name"]
    contact_number = decoded_config["contact"]["number"]


path_to_driver = "chromedriver.exe"




def open_site(url, driver):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


def cdriver():
    chromedriver_path = path_to_driver

    service = Service(chromedriver_path)
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    options.add_argument("--enable-javascript")
    options.add_argument('--incognito')
    options.binary_location = "chrome-win64/chrome.exe"

    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()
    #driver.maximize_window()
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)

    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    driver.set_window_size(1200, 1080)
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
def wait_until_tag(time, driver, tag):
    gela = WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.TAG_NAME, tag))
    )
    return gela

def wait_until_visible_id(driver, id, time=10):
    input_field = WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.ID, id))
    )
    return input_field

def wait_until_xpath(time, driver, xpath):
    try:
        gela = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return gela
    except:
        return False

def wait_until_cs(cssselector, time, driver):
    gela = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cssselector))
    )
    return gela




def click(xpath, driver, time=10):
    return driver.execute_script("arguments[0].click();", wait_until_xpath(time, driver, xpath=xpath))

# def click_css(css_selector, driver, time=10):
#     return driver.execute_script("arguments[0].click();", wait_until_cs(time, driver, css_selector))

def click_element(element, driver):
    return driver.execute_script("arguments[0].click();", element)

def into_view(element, driver):
    return driver.execute_script("arguments[0].scrollIntoView();", element)

def into_view_xpath(xpath, driver):
    return driver.execute_script("arguments[0].scrollIntoView();", wait_until_xpath(10, driver, xpath=xpath))


def byxpath(xpath,driver ,time=10):
    return wait_until_xpath(time, driver, xpath)