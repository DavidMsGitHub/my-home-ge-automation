from scraper import scrape_bina_iyideba
from for_driver import *
import time

def scrape_and_publish(link):
    # get credentials
    with open("config.json", "r") as cfg:
        json_string = json.load(cfg)
        mhemail = json_string["credentials"]["email"]
        mhpassword = json_string["credentials"]["password"]

    scraped = scrape_bina_iyideba(link)

    driver = cdriver()

    driver.get("https://statements.tnet.ge/ka/statement/create?referrer=myhome")

    driver.find_element(By.CSS_SELECTOR, "button.luk-px-5").click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Email"))
    ).send_keys(mhemail)
    driver.find_element(By.ID, "Password").send_keys(mhpassword)
    driver.find_element(By.CSS_SELECTOR, "button.gradient-button").click()

    bina_gilaki = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="0"]/div[2]/div/div/div/div[1]/label'))
    )

    bina_gilaki.click()
    if scraped["tipi"] == "იყიდება":
        driver.find_element(By.XPATH, '//*[@id="0"]/div[3]/div/div/div/div[1]/label').click()
    driver.find_element(By.CSS_SELECTOR, "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12").click()
    time.sleep(1)

    tbilisi = driver.find_element(By.XPATH, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", tbilisi)

    driver.find_element(By.XPATH, "//label[@for=':ri:']/input").send_keys(scraped["misamarti"])

    label_element = driver.find_element(By.XPATH, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
    driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")))
    driver.execute_script("arguments[0].click();", label_element)

    time.sleep(1.5)

    element = driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[4]')
    elements = element.find_elements(By.TAG_NAME, "span")
    count = 0
    for i in elements:
        if i.text == scraped["sadzinebeli"]:
            driver.execute_script("arguments[0].click();", i)

    driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[8]/div[1]/div/label').send_keys(scraped["sartuli"])
    driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[8]/div[2]/div/label').send_keys(scraped["sartuli-sul"])

    driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[10]/div/div/div').click()
    status_xpath = ''
    if scraped["status"] == "ძველი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[1]'
    elif scraped["status"] == "ახალი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[2]'
    elif scraped["status"] == "მშენებარე":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[3]'

    status = driver.find_element(By.XPATH, status_xpath)
    driver.execute_script("arguments[0].click();", status)

    status_dropdown = driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[1]')
    driver.execute_script("arguments[0].click();", status_dropdown)
    arastandartuli = driver.find_element(By.XPATH, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", arastandartuli)

    driver.find_element(By.XPATH, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
    driver.find_element(By.XPATH, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])
    time.sleep(1)

    time.sleep(50)