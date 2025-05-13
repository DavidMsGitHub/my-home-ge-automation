from wsgiref import headers

from for_driver import *
import time



def payment_part(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    container = wait_until_cs( "div.fixed.bottom-0.left-0.right-0.z-20.flex",10, driver)
    buttons = container.find_elements(By.TAG_NAME, "button")
    upload_button = buttons[1]
    try:
        upload_button.click()
    except:
        driver.execute_script("arguments[0].click();", upload_button)

    payment_choice = wait_until_clickable_xpath(
        '//*[@id="root"]/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", payment_choice)
    time.sleep(5)
    balance_choice = wait_until_clickable_xpath(
        '//*[@id="root"]/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", balance_choice)
    pay_button = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div[1]/div[2]/div/div/div/div[3]/button', 30,
                                            driver)
    driver.execute_script("arguments[0].click();", pay_button)
    success = wait_until_xpath(300, driver, "//h1[contains(text(), 'გადახდა წარმატებით განხორციელდა')]")

    if success:
        return True
    else:
        return False

def find_id_myhome(driver):
    def wait_for_page_to_load(driver):
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(1)

    open_site('https://www.myhome.ge/user-profile/my-statements/', driver)
    wait_for_page_to_load(driver)

    time.sleep(2)

    id = wait_until_xpath(20,driver,"(//span[contains(text(), 'ID:')])[1]").text
    print(id)
    return id.replace("ID: ", "")

def find_id_ss(driver):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('https://home.ss.ge/ka/user/my-applications')
    time.sleep(1.5)
    try:
        click('//*[@id="__next"]/main/div/div/div[2]/div/div/div[2]/div[2]/div[1]', driver)
    except:
        byxpath('//*[@id="__next"]/main/div/div/div[2]/div/div/div[2]/div[2]/div[1]', driver).click()

    main_div = byxpath('//*[@id="__next"]/main/div/div/div[2]/div/div/div[2]', driver)

    first_a_tag = main_div.find_element(By.XPATH, ".//a")

    first_href = first_a_tag.get_attribute("href")


    return first_href

import requests
import json
#info_for_database = {'MYHOME-ID': '20134412', 'MYHOME-LINK': 'https://myhome.ge/pr/20134412', 'OWNER NAME': 'Nino', 'OWNER NUMBER': '599 155 158', 'PARTI': '50', 'OTAXI': 1, 'BEDROOMS': 1, 'CONDITION': 'None', 'PRICE': '18', 'ADDRESS': 'ვაჟა-ფშაველას გამზირი ', 'REGION': 'gela',  'AGENTISSAXELI': 'Davita', 'TARIGI': '[Jan 05 17:52]', 'SS_LINK': 'https://home.ss.ge/ka/udzravi-qoneba/qiravdeba-1-otaxiani-bina-saburtaloze-31026316'}
def to_database(ifd):
    if ifd["OWNER NUMBER"] == "":
        ifd["OWNER NUMBER"] = "NUMBER ERROR"

    body = {
        "maindb": {
            "ownerNumber": ifd["OWNER NUMBER"],
            "myhomeLink": ifd["MYHOME-LINK"],
            "myhomeId": ifd["MYHOME-ID"],
            "ssGeLink": ifd["SS_LINK"],
            "ssGeId": ifd["SS_LINK"].rsplit('-', 1)[-1],
            "area": ifd["PARTI"],
            "room": ifd["OTAXI"],
            "bedroom": ifd["BEDROOMS"],
            "condition": ifd["CONDITION"],
            "price": ifd["PRICE"],
            "address": ifd["ADDRESS"],
            "region": ifd["REGION"],
            "agentName": ifd["AGENTISSAXELI"],
            "limitations": "",
            "date": ifd["TARIGI"],
        }
    }

    try:
        link = 'https://api.sheety.co/baa35ba46d9a518aa8cbd06376d3727d/everBrokerDb/maindb'
        gela = requests.post(link, json=body)

        print("SENT TO DB", f"\n {gela.text}")
    except:
        print("database error")





