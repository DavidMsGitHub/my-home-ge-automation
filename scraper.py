import json
import os
import shutil
import requests
import time
from for_driver import *
from publish_rent import publish_q
from publish_buy import publish

def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"

def scrape_and_post(link, desc=""):
    driver = cdriver()
    url = link
    driver.get(url)

    script = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
    )

    raw_data = script.get_attribute('innerHTML')
    data = json.loads(raw_data)


    data = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["statement"]



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
        "id": str(data["id"]),
        "misamarti": data["address"],
        "fasi": str(data["price"]["1"]["price_total"]),
        "parti": str(data["area"]),
        "otax-raodenoba": str(data["room_type_id"]),
        "sadzinebeli": int(data["bedroom_type_id"]),
        "sartuli": str(data["floor"]),
        "sartuli-sul": str(data["total_floors"]),
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

    # ------- fotoebis mxare
    print(scraped_dict)


    driver.quit()

    if check_type(data["dynamic_title"]) == "იყიდება":
        publish(link,scraped_dict,desc)
    else:
        publish_q(link,scraped_dict,desc)

    #return json.dumps(scraped_dict, ensure_ascii=False, indent=4)
    return scraped_dict