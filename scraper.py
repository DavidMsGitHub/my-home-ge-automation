import os
import shutil
import requests
import time
from for_driver import *
from publish_rent import publish_q, publish_q_house, publish_q_com_area
from datetime import datetime
from publish_buy import publish, publish_house,publish_com_area
from publish_buy_ss import publish_ss, publish_ss_house, publish_ss_com
from publish_rent_ss import publish_ss_q, publish_ss_q_com, publish_ss_q_house
from funqciebi import submit_error

def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"

def scrape_and_post(id, price = 0.0, area = 0.0, agencyid = "0", agent = "Home", to_myhome = False, to_ssge = False):

    print(to_myhome)
    print(to_ssge)
    def into_view(element):
        return driver.execute_script("arguments[0].scrollIntoView();", element)

    def into_view_xpath(xpath):
        return driver.execute_script("arguments[0].scrollIntoView();", wait_until_xpath(10, driver, xpath=xpath))
    #try:

    start = time.time()


    driver = cdriver()
    link = f"https://www.myhome.ge/pr/{id}"
    driver.get(link)


    try:
        click('//*[@id="CookieAgreement"]/div[3]/button', driver)
    except:
        pass





    # NOMRIS NAXVA
    def get_phone_number(driver):
        """Clicks the 'Show Number' button until the phone number appears, then extracts it."""

        button_xpath = '//*[@id="__next"]/div[2]/div/div[2]/div[2]/div/div[3]/button/div/div/span[2]'
        number_xpath = '//button/span[contains(text(), "+995")]'

        while True:
            try:
                return driver.find_element(By.XPATH, number_xpath).text.strip()
            except:
                pass  # Number not found yet, continue clicking

            try:
                btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.5)  # Minimal delay
                ActionChains(driver).move_to_element(btn).click().perform()
            except:
                break  # If button disappears, exit loop

        # Try extracting from network requests
        logs = driver.get_log("performance")
        for entry in logs:
            try:
                log = json.loads(entry["message"])["message"]
                if log["method"] == "Network.responseReceived":
                    request_id = log["params"]["requestId"]
                    response = driver.execute_script(
                        f"return window.performance.getEntries().find(e => e.name.includes('{request_id}'))"
                    )
                    if response:
                        return json.loads(response["name"])["data"]["phone_number"]
            except:
                continue

        return None  # Return None if phone number is not found

    # Example usage:
    nomeri = get_phone_number(driver).replace("+995 ", "")








    script = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
    )
    try:
        raw_data = script.get_attribute('innerHTML')
        data = json.loads(raw_data)
        data = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["statement"]
    except:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
            log.write(f"{current_time} <||> {id} | Scraper-ის შეცდომა, დიდი ალბათობით არარსებული განცხადება.\n")
        return



    status_id = ""
    if data["status_id"] == 3:
        status_id = "მშენებარე"
    elif data["status_id"] == 2:
        status_id = "ახალი აშენებული"
    elif data["status_id"] == 1:
        status_id = "ძველი აშენებული"

    # ------- PARAMETREBI

    parameter_list = []

    for parameter in data["parameters"]:
        if "id" in parameter and "key" in parameter:
            parameter_list.append(parameter["key"])

    # ------ PARAMETREBI



    # import random
    #
    # nomeri = str(data["user_phone_number"])
    # random_digits = ''.join(str(random.randint(0, 9)) for _ in range(3))
    # modified_number = nomeri[:-3] + random_digits
    # print(modified_number)


    scraped_dict = {
        "tipi": check_type(data["dynamic_title"]),
        "saxeli": data["dynamic_title"],
        "qalaqi": data["city_name"],
        "id": str(data["id"]),
        "misamarti": data["address"],
        "fasi": str(data["price"]["2"]["price_total"]),
        "parti": str(data["area"]),
        "otax-raodenoba": int(data["room_type_id"]),
        "sadzinebeli": data["bedroom_type_id"],
        "sartuli": data["floor"],
        "sartuli-sul": data["total_floors"],
        "status": status_id,
        "build_year": data["build_year"],
        "condition": str(data["condition_id"]), #mdgomareobis id
        "bathroom_type_id": str(data["bathroom_type_id"]), #sveli wertili
        "balconies": str(data["balconies"]), #balkoni
        "balcony_area": str(data["balcony_area"]), #balkonis parti
        "hot_water_type": data["hot_water_type_id"], # cxeli wylis tipi
        "heating_type": data["heating_type_id"], # gatbobis tipi
        "parking_type": data["parking_type_id"], # parkingis tipi
        "porch_area": data["porch_area"], # verandis parti
        "loggia_area": data["loggia_area"], # lojis parti
        "store_room_area": data["storeroom_area"], # sacavis parti
        "additions": parameter_list, # damatebiti parametrebis listi [kitchen, investment, washing_machine ..etc]
        "yard_area": data["yard_area"],

        "district_name": data["district_name"],

        # OWNER INFO
        "owner-number": nomeri,
        "owner-name": data["owner_name"],

        "agenti": agent
    }
    print(scraped_dict["owner-number"], scraped_dict["owner-name"])

    #------- fotoebis mxare
    gallery = data["images"]
    gancxadebisid = str(data["id"])
    if not os.path.exists(f"images/{gancxadebisid}"):
        os.makedirs(f"images/{gancxadebisid}")

    count = 1
    for item in gallery:
        url = item["large"]

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f"images/{gancxadebisid}/{count}.jpg", "wb") as img:
                shutil.copyfileobj(response.raw, img)
            response.close()
            print(f"Downloaded {url} to images/{gancxadebisid}/{count}.jpg")
        else:
            print(f"Failed to download {url}")
        count += 1





    # ------- fotoebis mxare

    #fasis da kvadratulobis shecvla tu gui-shi shecvlilia
    fasi = scraped_dict["fasi"]

    if int(price) > 0:
        scraped_dict["price"] = int(fasi) + int(price)
    if int(area) > 0:
        scraped_dict["area"] = str(area)

    print(scraped_dict)


#______________________________________________________________

    now = datetime.now()
    current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"

    db_info_for_myhomeskip = {
        "MYHOME-ID": "No MyHome",
        "MYHOME-LINK": f"No MyHome",
        "OWNER NAME": scraped_dict["owner-name"],
        "OWNER NUMBER": scraped_dict["owner-number"],
        "PARTI": scraped_dict["parti"],
        "OTAXI": scraped_dict["otax-raodenoba"],
        "BEDROOMS": scraped_dict["sadzinebeli"],
        "CONDITION": scraped_dict["status"],
        "PRICE": scraped_dict["fasi"],
        "ADDRESS": scraped_dict["misamarti"],
        "REGION": scraped_dict["district_name"],
        "AGENTISSAXELI": scraped_dict["agenti"],
        "TARIGI": current_time,
    }


    desc_qira = f"ქირავდება ბინა პირველი და ბოლო თვის წინასწარი გადახდით! კეთილმოწყობილი ბინა სრულად აღჭურვილია ყველა საჭირო ავეჯითა და ტექნიკით, რაც უზრუნველყოფს კომფორტულ ცხოვრებას. ბინა მდებარეობს კარგ ადგილას, სადაც ყველაფერი აუცილებელი ახლოსაა."
    desc_yidva = f"იყიდება ნათელი და ლამაზი ბინა იდეალურ ადგილას. დეტალური ინფორმაციისთვის დამიკავშირდით – გვაქვს მრავალი ვარიანტი, რომელიც სრულად შეეფერება თქვენს მოთხოვნებს."

    if check_type(data["dynamic_title"]) == "ქირავდება":
        if "ბინა" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss_q(scraped_dict, desc_qira, driver, db_info_for_myhomeskip)
            else:
                publish_q(scraped_dict,desc_qira, driver, to_ssge)

        elif "სახლი" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss_q_house(scraped_dict, desc_qira, driver, db_info_for_myhomeskip)
            else:
                publish_q_house(scraped_dict, desc_qira, driver, to_ssge)

        elif "კომერციული ფართი" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss_q_com(scraped_dict, desc_qira, driver, db_info_for_myhomeskip)
            else:
                publish_q_com_area(scraped_dict, desc_qira, driver, to_ssge)

    else:
        if "ბინა" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss(scraped_dict, desc_yidva, driver, db_info_for_myhomeskip)
            else:
                publish(scraped_dict,desc_yidva, driver, to_ssge)

        elif "სახლი" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss_house(scraped_dict, desc_yidva, driver, db_info_for_myhomeskip)
            else:
                publish_house(scraped_dict, desc_yidva, driver, to_ssge)

        elif "კომერციული ფართი" in data["dynamic_title"]:
            if to_myhome == False and to_ssge == True:
                publish_ss_com(scraped_dict, desc_yidva, driver, db_info_for_myhomeskip)
            else:
                publish_com_area(scraped_dict, desc_yidva, driver, to_ssge)

    # except:
    #     now = datetime.now()
    #     current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
    #     with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
    #         log.write(f"{current_time} <||> {id} | Scraper-ის შეცდომა.\n")
    #
    #     submit_error(id, current_time, "Scraper")

    return json.dumps(data, ensure_ascii=False, indent=4)


# scrape_and_post('18873395')
# scrape_and_post('20547178')
# scrape_and_post("11537535")
# scrape_and_post("19444848")
# scrape_and_post("20499024")
# start = time.time()
# # IYIDEBA BINA
# scrape_and_post("20362168")
# scrape_and_post("20390533")
# scrape_and_post("20417266")
# # QIRAVDEBA BINA
# scrape_and_post("20410522")
# scrape_and_post("20179129")
# scrape_and_post("20338367")
# # IYIDEBA SAXLI
# scrape_and_post("20372934")
# scrape_and_post("19444848")
# scrape_and_post("18845445")
# # QIRAVDEBA SAXLI
# scrape_and_post("19599801")
# scrape_and_post("20140291")
# scrape_and_post("20401652")
#
# end = time.time()
# print(f"FOR ALL: {(end - start):2f}")