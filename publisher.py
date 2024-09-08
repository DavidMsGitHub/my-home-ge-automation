from scraper import scrape_bina_iyideba
from for_driver import *
import time
import os

def scrape_and_publish(link, description=""):
    # get credentials
    with open("config.json", "r") as cfg:
        json_string = json.load(cfg)
        mhemail = json_string["credentials"]["email"]
        mhpassword = json_string["credentials"]["password"]
        contact_name = json_string["contact"]["name"]
        contact_number = json_string["contact"]["number"]

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
    time.sleep(1)
    listo = driver.find_element(By.CSS_SELECTOR, 'ul.list-none')
    first_result = listo.find_element(By.CSS_SELECTOR, "li.cursor-pointer")
    driver.execute_script("arguments[0].click();", first_result)


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

    #contact information
    driver.find_element(By.XPATH, '//*[@id=":r1j:"]').send_keys(contact_name)
    driver.find_element(By.XPATH, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE ,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, contact_number)
    #description geo,eng,rus
    driver.find_element(By.XPATH, '//*[@id="4"]/div[2]/div[2]/textarea').send_keys(description)
    #eng
    eng_button = driver.find_element(By.XPATH, '//*[@id="4"]/div[2]/div[1]/div[1]/button[2]')
    driver.execute_script("arguments[0].click();", eng_button)
    translate_button = driver.find_element(By.XPATH, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
    driver.execute_script("arguments[0].click();", translate_button)
    time.sleep(0.1)
    #rus
    rus_button = driver.find_element(By.XPATH, '//*[@id="4"]/div[2]/div[1]/div[1]/button[3]')
    driver.execute_script("arguments[0].click();", rus_button)
    translate_button = driver.find_element(By.XPATH, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
    driver.execute_script("arguments[0].click();", translate_button)
    #photo upload
    photo_folder = f'{scraped["id"]}/'
    photo_files = []
    for f in os.listdir(photo_folder):
        if f.endswith(".png"):
            photo_files.append(os.path.abspath(os.path.join(photo_folder, f)))
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "browse"))
    )
    file_paths = "\n".join(photo_files)
    file_input.send_keys(file_paths)

    time.sleep(1)
    #upload
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    container = driver.find_element(By.CSS_SELECTOR, "div.fixed.bottom-0.left-0.right-0.z-20.flex")
    buttons = container.find_elements(By.TAG_NAME, "button")
    upload_button = buttons[1]
    try:
        upload_button.click()
    except:
        driver.execute_script("arguments[0].click();", upload_button)
    payment_choice = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/label'))
    )
    driver.execute_script("arguments[0].click();", payment_choice)
    balance_choice = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/label'))
    )
    time.sleep(0.1)
    driver.execute_script("arguments[0].click();", balance_choice)
    pay_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div/div/div[3]/button'))
    )
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", pay_button)
    time.sleep(500)
    driver.quit()