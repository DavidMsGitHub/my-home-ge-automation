from for_driver import *
import os, shutil, requests, json, time


def check_type(post_element):
    if "იყიდება" in post_element:
        return "იყიდება"
    elif "ქირავდება" in post_element:
        return "ქირავდება"


def scrape_the_post():
    driver = cdriver()
    start = 19804448
    for i in range(200):

        url = f"https://www.myhome.ge/pr/{start}"
        driver.get(url)

        try:
            script = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
            )

            raw_data = script.get_attribute('innerHTML')
            data = json.loads(raw_data)


            data = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["statement"]



            for parameter in data["parameters"]:
                if "id" in parameter and "key" in parameter:
                    print(parameter["key"])
        except:
            start += 10
            continue
        start += 1


scrape_the_post()


