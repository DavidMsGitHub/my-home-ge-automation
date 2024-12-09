
from for_driver import *
import os, shutil, requests, json, time


def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"
def scrape_the_post(link):
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

    scraped_dict = {
        "tipi": check_type(data["dynamic_title"]),
        "saxeli": data["dynamic_title"],
        "id": str(data["id"]),
        "misamarti": data["address"],
        "fasi": str(data["price"]["1"]["price_total"]),
        "parti": str(data["area"]),
        "otax-raodenoba": str(data["room_type_id"]),
        "sadzinebeli": str(data["bedroom_type_id"]),
        "sartuli": str(data["floor"]),
        "sartuli-sul": str(data["total_floors"]),
        "status": status_id,


        "balconies": str(data["balconies"]),
        "balcony_area": str(data["balcony_area"]),
        "hot_water_type": str(data["hot_water_type_id"])
        "heating_type":
        "parking_type":
    }

    driver.find_element(By.CSS_SELECTOR, "img.object-contain").click()
    time.sleep(0.5)

    # fotoebis mxare
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

    driver.quit()

    return json.dumps(scraped_dict, ensure_ascii=False, indent=4)






print(scrape_the_post("https://www.myhome.ge/pr/19857955/iyideba-1-otaxiani-bina-bagebshi/"))
#print(scrape_the_post("https://www.myhome.ge/pr/19940020/qiravdeba-dghiurad-9-otaxiani-bina-bakurianshi/"))
#print(scrape_the_post("https://www.myhome.ge/pr/19857955/iyideba-1-otaxiani-bina-bagebshi/"))
#print(scrape_the_post("https://www.myhome.ge/pr/19523903/qiravdeba-dghiurad-1-otaxiani-bina-saburtaloze/"))