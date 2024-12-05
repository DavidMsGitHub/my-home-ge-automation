from scraper import scrape_bina_iyideba, scrape_bina_qiravdeba
from for_driver import *
import os
import time

#TODO 1 AXALI INFOS GADAMUSHAVEBA
#TODO 2 AM INFOS GAMOYENEBA DA IM DAMATEBIT GILAKEBZE DACHERA


def scrape_and_publish_q(link, description=""):
    # get credentials
    with open("config.json", "r") as cfg:
        json_string = json.load(cfg)
        mhemail = json_string["credentials"]["email"]
        mhpassword = json_string["credentials"]["password"]
        contact_name = json_string["contact"]["name"]
        contact_number = json_string["contact"]["number"]

    scraped = scrape_bina_qiravdeba(link)

    driver = cdriver()

    driver.get("https://statements.tnet.ge/ka/statement/create?referrer=myhome")

    wait_until_cs( "button.luk-px-5",10, driver).click()

    wait_until_id(10, driver, "Email").send_keys(mhemail)
    wait_until_id(10, driver, "Password").send_keys(mhpassword)
    wait_until_cs( "button.gradient-button",10, driver).click()

    bina_gilaki = wait_until_xpath(10, driver,'//*[@id="0"]/div[2]/div/div/div/div[1]/label')
    bina_gilaki.click()

    wait_until_xpath(10, driver, '//*[@id="0"]/div[3]/div/div/div/div[2]/label').click()
    six_months = wait_until_xpath(10, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/label')
    driver.execute_script("arguments[0].click();", six_months)

    airchiet_gaqiravebis_tipi = wait_until_xpath(10, driver, '//*[@id="0"]/div[5]/div/div/div/div')
    airchiet_gaqiravebis_tipi.click()
    mtliani_qoneba = wait_until_cs( 'li.luk-w-full.luk-p-2.luk-rounded-md.luk-text-sm.luk-font-regular.luk-outline-0.luk-cursor-pointer.luk-text-black-70',10, driver)
    driver.execute_script("arguments[0].click();", mtliani_qoneba)

    #agarmaxsovs aq raiyo :D
    # wait_until_xpath(10, driver, '//*[@id="0"]/div[5]/div/div/div/div').click()
    # driver.find_element(By.CSS_SELECTOR,
    #                     "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12").click()


    wait_until_xpath(10, driver, '//*[@id="0"]/div[6]/div/div/div/div').click()

    tbilisi = wait_until_xpath(60, driver,'//*[@id="0"]/div[6]/div/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", tbilisi)

    wait_until_xpath(10, driver, "//label[@for=':ro:']/input").send_keys(scraped["misamarti"])
    listo = wait_until_cs( 'ul.list-none',10, driver)
    first_result = wait_until_cs( "li.cursor-pointer",10, listo)
    driver.execute_script("arguments[0].click();", first_result)

    label_element = wait_until_xpath(10, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
    driver.execute_script("arguments[0].scrollIntoView(true);", label_element)

    wait_until_xpath(f"//label[.//span[text()='{scraped['otax-raodenoba']}']]", 10, driver)

    driver.execute_script("arguments[0].click();", label_element)



    element = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[4]')
    elements = element.find_elements(By.TAG_NAME, "span")
    count = 0
    if int(scraped["sadzinebeli"]) >= 1:
        for i in elements:
            if i.text == scraped["sadzinebeli"]:
                driver.execute_script("arguments[0].click();", i)

    wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[1]/div/label').send_keys(scraped["sartuli"])
    wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[2]/div/label').send_keys(scraped["sartuli-sul"])

    el = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[10]/div/div/div')
    driver.execute_script("arguments[0].click();", el)

    status_xpath = ''
    if scraped["status"] == "ძველი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[1]'
    elif scraped["status"] == "ახალი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[2]'
    elif scraped["status"] == "მშენებარე":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[3]'

    status = wait_until_xpath(10, driver, status_xpath)
    driver.execute_script("arguments[0].click();", status)

    status_dropdown = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[1]')
    driver.execute_script("arguments[0].click();", status_dropdown)
    arastandartuli = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", arastandartuli)

    wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
    wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])

    # contact information
    wait_until_xpath(10, driver, '//*[@id=":r1p:"]').send_keys(contact_name)
    wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            Keys.BACKSPACE,
                                                                                            contact_number)
    # description geo,eng,rus
    wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[2]/textarea').send_keys(description)
    # eng
    eng_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[1]/button[2]')
    driver.execute_script("arguments[0].click();", eng_button)
    translate_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
    driver.execute_script("arguments[0].click();", translate_button)
    # rus
    rus_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[1]/button[3]')
    driver.execute_script("arguments[0].click();", rus_button)
    translate_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
    driver.execute_script("arguments[0].click();", translate_button)
    # photo upload
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


    # upload
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    container = wait_until_cs( "div.fixed.bottom-0.left-0.right-0.z-20.flex",10, driver)
    buttons = container.find_elements(By.TAG_NAME, "button")
    upload_button = buttons[1]
    try:
        upload_button.click()
    except:
        driver.execute_script("arguments[0].click();", upload_button)


    payment_choice = wait_until_xpath(60, driver,'//*[@id="root"]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/label')

    driver.execute_script("arguments[0].click();", payment_choice)

    balance_choice = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/label', 60, driver)
    driver.execute_script("arguments[0].click();", balance_choice)
    pay_button = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div/div[2]/div/div/div/div[3]/button', 60, driver)
    driver.execute_script("arguments[0].click();", pay_button)
    gela = wait_until_xpath(30, driver, "//h1[contains(text(), 'გადახდა წარმატებით განხორციელდა')]")
    if not gela:
        driver.quit()
    else:
        driver.quit()


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

    wait_until_cs( "button.luk-px-5",10, driver).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Email"))
    ).send_keys(mhemail)
    wait_until_id(10, driver, "Password").send_keys(mhpassword)
    wait_until_cs( "button.gradient-button",10, driver).click()

    bina_gilaki = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="0"]/div[2]/div/div/div/div[1]/label'))
    )

    bina_gilaki.click()
    if scraped["tipi"] == "იყიდება":
        wait_until_xpath(10, driver, '//*[@id="0"]/div[3]/div/div/div/div[1]/label').click()
    wait_until_cs( "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12",10, driver).click()

    tbilisi = wait_until_xpath(10, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", tbilisi)

    wait_until_xpath(10, driver, "//label[@for=':ri:']/input").send_keys(scraped["misamarti"])
    listo = wait_until_cs( 'ul.list-none',10, driver)
    first_result = wait_until_cs( "li.cursor-pointer",10, listo)
    driver.execute_script("arguments[0].click();", first_result)


    label_element = wait_until_xpath(10, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
    driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
    wait_until_xpath(10, driver,f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
    driver.execute_script("arguments[0].click();", label_element)


    element = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[4]')
    elements = element.find_elements(By.TAG_NAME, "span")
    count = 0
    if int(scraped["sadzinebeli"]) >= 1:
        for i in elements:
            if i.text == scraped["sadzinebeli"]:
                driver.execute_script("arguments[0].click();", i)

    wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[1]/div/label').send_keys(scraped["sartuli"])
    wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[2]/div/label').send_keys(scraped["sartuli-sul"])
    ###-----#_#_#__##__##__#
    el = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[10]/div/div/div')
    driver.execute_script("arguments[0].click();", el)
    #_#_#__#_#_#_#_#_#_

    status_xpath = ''
    if scraped["status"] == "ძველი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[1]'
    elif scraped["status"] == "ახალი აშენებული":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[2]'
    elif scraped["status"] == "მშენებარე":
        status_xpath = '//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[3]'

    status = wait_until_xpath(10, driver, status_xpath)
    driver.execute_script("arguments[0].click();", status)

    status_dropdown = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[1]')
    driver.execute_script("arguments[0].click();", status_dropdown)
    arastandartuli = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[2]/ul/li[1]')
    driver.execute_script("arguments[0].click();", arastandartuli)

    wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
    wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])

    #contact information
    wait_until_xpath(10, driver, '//*[@id=":r1j:"]').send_keys(contact_name)
    wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE ,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, contact_number)
    #description geo,eng,rus
    wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[2]/textarea').send_keys(description)
    #eng
    eng_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[1]/button[2]')
    driver.execute_script("arguments[0].click();", eng_button)
    translate_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
    driver.execute_script("arguments[0].click();", translate_button)
    #rus
    rus_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[1]/button[3]')
    driver.execute_script("arguments[0].click();", rus_button)
    translate_button = wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[1]/div[2]/div')
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

    #upload
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    container = wait_until_cs( "div.fixed.bottom-0.left-0.right-0.z-20.flex",10, driver)
    buttons = container.find_elements(By.TAG_NAME, "button")
    upload_button = buttons[1]
    try:
        upload_button.click()
    except:
        driver.execute_script("arguments[0].click();", upload_button)

    payment_choice = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", payment_choice)

    balance_choice = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", balance_choice)
    pay_button = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div/div[2]/div/div/div/div[3]/button', 30, driver)
    driver.execute_script("arguments[0].click();", pay_button)
    gela = wait_until_xpath(30, driver, "//h1[contains(text(), 'გადახდა წარმატებით განხორციელდა')]")

    if not gela:
        driver.quit()
        print("Something Went Wrong...")
    else:
        driver.quit()
        print("everything went well")