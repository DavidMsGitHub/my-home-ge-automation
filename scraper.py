import json
import os
import shutil
import requests
import time
from for_driver import *
from advanced_scraper import scrape_the_post

#TODO 0 GADAKETEBA SCRAPERIS UFRO MARTIV XERXZE
#TODO 1 METI INFOS GAMOTANA MARTIVI XERXIT
#TODO 2 AM INFOS GADACEMA PUBLISHERISTVIS
#TODO 3 AUTOMATURAD AGQMA GANCXADEBIS TIPIS



def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"

def scrape_bina_qiravdeba(link):
    driver = cdriver()
    driver.get(link)
    time.sleep(0.5)
    cookie_confirmation_popup = driver.find_element(By.XPATH, '//*[@id="CookieAgreement"]/div[3]/button')
    if cookie_confirmation_popup:
        cookie_confirmation_popup.click()

    try:
        # Use WebDriverWait to wait until the element is available
        script = WebDriverWait(driver, 20).until(  # Increased waiting time
            EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
        )

        # Extract the JSON data from the script tag
        raw_data = script.get_attribute('innerHTML')

        # Decode the raw data using UTF-8
        data = json.loads(raw_data)
    except Exception as e:
        print(f"Error: {e}")

    # Close the WebDriver after scraping
    driver.quit()

    data = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["statement"]
    data2 = data["props"]["pageProps"]

    gancxadebisid = data2["_nextI18Next"]["statementId"],


    status_id = ""
    if data["status_id"] == 3:
        status_id = "მშენებარე"

    scraped_dict = {
        "tipi": check_type(data["dynamic_title"]),
        "saxeli": data["dynamic_title"],
        "id": data2["_nextI18Next"]["statementId"],
        "misamarti": data["address"],
        "fasi": data["price"][1]["price_total"],
        "parti": data["area"],
        "otax-raodenoba": data["room_type_id"],
        "sadzinebeli": data["bedroom_type_id"],
        "sartuli": data["floor"],
        "sartuli-sul": data["total_floors"],
        "status": status_id
    }

    print(scraped_dict)
    driver.find_element(By.CSS_SELECTOR, "img.object-contain").click()
    time.sleep(0.5)

    # fotoebis mxare
    # vqmnit folders tu ar gvaqvs
    if not os.path.exists(gancxadebisid):
        os.makedirs(gancxadebisid)

    images = driver.find_elements(By.CSS_SELECTOR, "img.absolute")
    count = 1

    for image in images:
        url = image.get_attribute("src")
        response = requests.get(url, stream=True)
        with open(f"{gancxadebisid}/{count}.png", "wb") as img:
            shutil.copyfileobj(response.raw, img)
        response.close()
        count += 1

    driver.quit()
    return scraped_dict



def scrape_bina_iyideba(link):
    driver = cdriver()
    driver.get(link)
    time.sleep(0.5)
    cookie_confirmation_popup = driver.find_element(By.XPATH, '//*[@id="CookieAgreement"]/div[3]/button')
    if cookie_confirmation_popup:
        cookie_confirmation_popup.click()
    gancxadeba = driver.find_element(By.CSS_SELECTOR, "div.flex.flex-row.gap-4.font-tbcx-bold")
    gancxadeba = gancxadeba.text
    gancxadebisid = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/span[3]').text.replace("ID: ", "")
    misamarti = driver.find_element(By.CSS_SELECTOR, "div.flex.items-center.gap-2.mt-2.text-sm").text
    fasi = driver.find_elements(By.CSS_SELECTOR, ".text-2xl.font-tbcx-bold")
    fasi = fasi[1].text.replace(",","").replace("\n₾", "")
    parti = driver.find_elements(By.CSS_SELECTOR, "span.flex.mt-0.text-sm.font-tbcx-medium")
    parti = parti[3].text.replace("ფართი: ", "").replace(" მ²", "")
    info_table = driver.find_elements(By.CSS_SELECTOR, "div.flex.items-center.gap-3")
    otaxebi = info_table[1].text.replace("ოთახი\n", "")
    try:
        sadzinebel = info_table[2].text.replace("საძინებელი\n", "")
        sartulebi = info_table[3].text.replace("სართული\n", "").replace(" ", "").split("/")
    except:
        sadzinebel = "0"
        sartulebi = info_table[2].text.replace("სართული\n", "").replace(" ", "").split("/")

    info_grid = driver.find_element(By.CSS_SELECTOR, "div.grid.gap-4.grid-cols-1")
    info_in_info_grid = info_grid.find_element(By.CSS_SELECTOR, "div.flex.text-sm")
    statusis_elementi = info_in_info_grid.find_element(By.TAG_NAME, "div").text.replace("სტატუსი\n", "")

    scraped_dict = {
        "tipi": check_type(gancxadeba),
        "saxeli": gancxadeba,
        "id": gancxadebisid,
        "misamarti": misamarti,
        "fasi": fasi,
        "parti": parti,
        "otax-raodenoba": otaxebi,
        "sadzinebeli": sadzinebel,
        "sartuli":sartulebi[0],
        "sartuli-sul": sartulebi[1],
        "status": statusis_elementi
    }

    driver.find_element(By.CSS_SELECTOR, "img.object-contain").click()
    time.sleep(0.5)

    # fotoebis mxare
    # vqmnit folders tu ar gvaqvs
    if not os.path.exists(gancxadebisid):
        os.makedirs(gancxadebisid)

    images = driver.find_elements(By.CSS_SELECTOR, "img.absolute")
    count = 1

    for image in images:
        url = image.get_attribute("src")
        response = requests.get(url, stream=True)
        with open(f"{gancxadebisid}/{count}.png","wb") as img:
            shutil.copyfileobj(response.raw, img)
        response.close()
        count += 1

    driver.quit()
    return scraped_dict