
from for_driver import *
import json


def scrape_the_post(link,driver):

    # Target URL
    url = link

    # Open the page using Selenium
    driver.get(url)

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

    return data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"]["statement"]


gela = scrape_the_post("https://www.myhome.ge/pr/17884484/iyideba-3-otaxiani-bina-did-dighomshi/", driver=cdriver())
print(gela)