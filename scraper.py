import json
import os
import shutil
import requests
import time
from for_driver import *
from publish_rent import publish_q
from datetime import datetime
from publish_buy import publish
from funqciebi import submit_error

def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"

def scrape_and_post(id, price = "", area = ""):
    try:
        driver = cdriver()
        link = f"https://www.myhome.ge/pr/{id}"
        driver.get(link)

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
        }



        #------- fotoebis mxare
        wait_until_cs("img.object-contain", 30, driver).click()
        time.sleep(0.5)
        gancxadebisid = str(data["id"])
        if not os.path.exists(f"images/{gancxadebisid}"):
            os.makedirs(f"images/{gancxadebisid}")

        images = driver.find_elements(By.CSS_SELECTOR, "img.absolute")
        count = 1

        for image in images:
            url = image.get_attribute("src")
            response = requests.get(url, stream=True)
            with open(f"images/{gancxadebisid}/{count}.png", "wb") as img:
                shutil.copyfileobj(response.raw, img)
            response.close()
            count += 1

        # ------- fotoebis mxare
        print(scraped_dict)


        driver.quit()

        #fasis da kvadratulobis shecvla tu gui-shi shecvlilia

        if int(price) > 0:
            scraped_dict["fasi"] = str(price)
        if int(area) > 0:
            scraped_dict["area"] = str(area)

    except:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
            log.write(f"{current_time} <||> {id} | Scraper-ის შეცდომა.\n")

        submit_error(id, current_time, "Scraper")


    if check_type(data["dynamic_title"]) == "ქირავდება":
        desc = "ქირავდება პირველი და ბოლო თვის წინასწარი გადახდით!!!ქირავდება კეთილმოწყობილი ბინა ყველანაირი ავეჯითა და ტექნიკით რაც დაგჭირდებათ უზრუნველყოფილად ცხოვრებისთვის ბინა არის კარგ ადგილას ყველა საჭირო ობიექტით გარშემორტყმული"
        publish_q(link,scraped_dict,desc)
    else:
        desc = "იყიდება ნათელი და ლამაზი ბინა იდეალურ ადგილას დეტალური ინფორმაციისთვის დამიკავშირდით გვაქვს ბევრი ვარიანტი,რომელიც მაქსიმალურად მორგებული იქნება თქვენზე"
        publish(link,scraped_dict,desc)

    #return json.dumps(scraped_dict, ensure_ascii=False, indent=4)
    return scraped_dict
