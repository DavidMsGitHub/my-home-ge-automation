from for_driver import *
import os
import time
import glob
import json
from pay_and_upload import find_id_ss, to_database

#scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება 3 ოთახიანი ბინა ვაკეში', 'qalaqi': 'თბილისი', 'id': '17496132', 'misamarti': 'ილია ჭავჭავაძის გამზირი ', 'fasi': '570000', 'parti': '132', 'otax-raodenoba': 3, 'sadzinebeli': 2, 'sartuli': 10, 'sartuli-sul': 22, 'status': 'ახალი აშენებული', 'build_year': '>2000', 'condition': '1', 'bathroom_type_id': '2', 'balconies': '1', 'balcony_area': '900', 'hot_water_type': None, 'heating_type': None, 'parking_type': None, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['furniture', 'porch', 'telephone', 'conditioner']}

def publish_ss(scraped, description, driver, info_for_database ):

    open_site('https://home.ss.ge/ka/udzravi-qoneba/create', driver)


    def click(xpath, time=10):
        return driver.execute_script("arguments[0].click();", wait_until_xpath(time, driver, xpath=xpath))

    def click_element(element):
        return driver.execute_script("arguments[0].click();", element)

    def into_view(element):
        return driver.execute_script("arguments[0].scrollIntoView();", element)

    def into_view_xpath(xpath):
        return driver.execute_script("arguments[0].scrollIntoView();", wait_until_xpath(10, driver, xpath=xpath))


    def byxpath(xpath, time=10):
        return wait_until_xpath(time, driver, xpath)

    def set_field_value_with_js(driver, element, value):
        driver.execute_script("""
            arguments[0].value = arguments[1]; // Set the value
            arguments[0].dispatchEvent(new Event('input', { bubbles: true })); // Trigger input event
            arguments[0].dispatchEvent(new Event('change', { bubbles: true })); // Trigger change event
        """, element, value)



    with open("config.json", "r", encoding="utf-8") as cfg:
        encoded_config = json.load(cfg)["encoded_data"]
        decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

        # mhemail = decoded_config["credentials"]["myhome"]["email"]
        # mhpassword = decoded_config["credentials"]["myhome"]["password"]
        mhemail = decoded_config["credentials"]["ss.ge"]["email"]
        mhpassword = decoded_config["credentials"]["ss.ge"]["password"]
        contact_name = decoded_config["contact"]["name"]
        contact_number = decoded_config["contact"]["number"]


    # LOGIN
    try:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div/div[2]/button[2]'))
    except:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div[1]/div'))

    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[1]/input').send_keys(mhemail)
    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[2]/input').send_keys(mhpassword)
    driver.execute_script("arguments[0].click();",
                          wait_until_xpath(10, driver, '//*[@id="card"]/div/div/div[2]/div/form/button[2]'))

    if byxpath("//button[text()='გააგრძელე განთავსება']", 10):  # TU WINA GANCXADEBIS DAMATEBIS POPUPI
        click('//*[@id="__next"]/div[1]/div[1]/div/div/div[2]/button[1]')

    def upload_photos(scraped_id):
        """Handles uploading photos for a given scraped ID."""
        try:
            click('//*[@id="create-app-type"]/div[2]/div[1]')
            click('//*[@id="create-app-type"]/div[3]/div[1]')

            # Locate and prepare photo files
            photo_folder = os.path.join("images", str(scraped_id))
            photo_files = glob.glob(os.path.join(photo_folder, "*.jpg"))

            if not photo_files:
                raise FileNotFoundError(f"No JPG images found in {photo_folder}")

            file_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
            )

            # Join file paths with newline and send to input
            file_input.send_keys("\n".join(map(os.path.abspath, photo_files)))
            print("Photos uploaded successfully.")

        except Exception as e:
            print(f"Error in upload_photos: {e}")
            raise

    def retry_upload_photos(scraped_id, retries=2):
        """Retries the photo upload process in case of failure."""
        for attempt in range(retries):
            try:
                upload_photos(scraped_id)
                return  # Exit if successful
            except Exception as e:
                print(f"Retry {attempt + 1}/{retries} failed: {e}")
        print("Photo upload failed after multiple attempts.")

    # Example usage
    scraped_id = scraped["id"]  # Ensure this is an integer or string
    retry_upload_photos(scraped_id)

#------------------qalaqi----------------------------------------------
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[1]/div/div/div[1]/div[2]')
    into_view(dropdown)
    dropdown.click()
    city_option = byxpath(f"//div[contains(@class, 'select__option') and text()='{scraped['qalaqi']}']")
    into_view(city_option)
    click_element(city_option)
#------------------qucha------------------------------------------------

    # Split the scraped address into individual words
    words = scraped["misamarti"].split()
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[1]/div[1]/div')
    into_view(dropdown)
    dropdown.click()

    for word in words:
        forbidden = ["ა.","ბ.","გ.","დ.","ე.""ვ.","ზ.","თ.","ი.","კ.","ლ.","მ.","ნ.","ო.","პ.","ჟ.","რ.","ს.","ტ.","უ.","ჭ.","წ."]
        if word in forbidden:
            continue
        try:
            city_option = byxpath(f"//div[contains(@class, 'select__option') and contains(text(), '{word}')]")
            into_view(city_option)
            click_element(city_option)
            print(f"Clicked option containing word: {word}")
            break  # dacheris shemdeg gamodis loopidan
        except Exception as ex:
            print(f"shecdoma misamartshi: {word}, error: {ex}")
#-----------------------------------saxlis nomeri--------------------------------------
    try:
        click('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input')
    except:
        byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').click()
    byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').send_keys("3")
#--------------------otaxebi----------------------------------------------
    otaxebis_container = byxpath('//*[@id="create-app-details"]/div[2]/div[1]/div[2]')
    if scraped["otax-raodenoba"] >= 9:
        click(byxpath('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[9]'))
    else:
        click_element(wait_until_xpath(10, otaxebis_container, f".//*[contains(text(), '{scraped['otax-raodenoba']}')]"))
#-----------------------sadzinebeli-------------------------------------------
    sadzinebeli_container = byxpath('//*[@id="create-app-details"]/div[2]/div[2]/div[2]/div')
    if scraped["sadzinebeli"] != None:
        click_element(wait_until_xpath(10, sadzinebeli_container, f".//*[contains(text(), '{scraped['sadzinebeli']}')]"))
    else:
        click_element(
            wait_until_xpath(10, sadzinebeli_container, f".//*[contains(text(), '1')]"))
#-------------------------saerto parti-----------------------------------------

    byxpath('//*[@id="create-app-details"]/div[2]/div[3]/div[2]/div[1]/label/div/input').send_keys(scraped["parti"])
#------------------------------sartuli/sartulianoba------------------------------------
    byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div[1]/label/div/input').send_keys(scraped["sartuli"])
    byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div[2]/label/div/input').send_keys(scraped["sartuli-sul"])
#--------------------------------sartulis tipi----------------------------------
    try:
        byxpath('//*[@id="create-app-details"]/div[2]/div[5]/div[2]/div/div[1]').click()
    except:
        click('//*[@id="create-app-details"]/div[2]/div[5]/div[2]/div/div[1]')
#-------------------------------aivani lojia-----------------------------------

    loggia = 0
    if scraped["balconies"] is None or scraped["balconies"] == 'None':
        scraped["balconies"] = 0
    else:
        scraped["balconies"] = int(scraped["balconies"])

    if scraped["loggia_area"] is None or scraped["loggia_area"] == 'None':
        loggia = 0
    else:
        loggia = 1

    sul_raodenoba = int(scraped["balconies"]) + loggia

    bandl_container = byxpath('//*[@id="create-app-details"]/div[2]/div[6]/div[2]/div')
    if sul_raodenoba != 0:
        click_element(
            wait_until_xpath(10, bandl_container, f".//*[contains(text(), '{sul_raodenoba}')]"))
    else:
        click('//*[@id="create-app-details"]/div[2]/div[6]/div[2]/div/div[6]')

#------------------------------sveli wertili------------------------------------

    sveli_container = byxpath('//*[@id="create-app-details"]/div[2]/div[7]/div[2]/div')


    if scraped["bathroom_type_id"] == None or scraped["bathroom_type_id"] == 'None':
        click('//*[@id="create-app-details"]/div[2]/div[7]/div[2]/div/div[6]')
    elif int(scraped["bathroom_type_id"]) > 5:
        click('//*[@id="create-app-details"]/div[2]/div[7]/div[2]/div/div[5]')
    else:
        click_element(
            wait_until_xpath(10, sveli_container, f".//*[contains(text(), '{scraped['bathroom_type_id']}')]"))

#------------------------------------------------------------------
    status_container = byxpath('//*[@id="create-app-details"]/div[2]/div[8]/div[2]/div')
    click_element(
        wait_until_xpath(10, status_container, f".//*[contains(text(), '{scraped['status']}')]"))
#-----------------------------proeqt tipi-------------------------------------

    click('//*[@id="create-app-details"]/div[2]/div[9]/div[2]/div/div[13]') # arastandartuli only
#----------------------------damatebiti algostvis--------------------------------------
    click('//*[@id="create-app-details"]/div[2]/div[10]/div[2]/div/div[1]')
    click('//*[@id="create-app-details"]/div[2]/div[10]/div[2]/div/div[2]')
    click('//*[@id="create-app-details"]/div[2]/div[10]/div[2]/div/div[3]')
    click('//*[@id="create-app-details"]/div[2]/div[10]/div[2]/div/div[4]')
#-----------------------------mdgomareoba-------------------------------------
    if scraped["condition"] == "1":
        click('//*[@id="create-app-details"]/div[2]/div[11]/div[2]/div/div[5]')
    elif scraped["condition"] == "2":
        click('//*[@id="create-app-details"]/div[2]/div[11]/div[2]/div/div[3]')
    else:
        click('//*[@id="create-app-details"]/div[2]/div[11]/div[2]/div/div[1]')
#------------------------------damatebiti informeishen------------------------------------

    if scraped["heating_type"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[5]')

    match scraped["additions"]:
        case "elevator":
            click('//*[@id="create-app-additional-info"]/div[2]/div[3]')
        case "refrigerator":
            click('//*[@id="create-app-additional-info"]/div[2]/div[6]')
        case "pets-allowed":
            click('//*[@id="create-app-additional-info"]/div[2]/div[20]')


    if scraped["balconies"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[1]') # aivani
    if scraped["store_room_area"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[8]') # satavso
    # if scraped["sartuli"] == scraped["sartuli-sul"]:
    #     click('//*[@id="create-app-additional-info"]/div[2]/div[6]') #bolo sartuli
        #GARAJI DA SARDAPI AR GVAQVS
#--------------------------descripsheni----------------------------------------
    byxpath('//*[@id="create-app-desc"]/div[2]/textarea').send_keys(description)
    click('//*[@id="create-app-desc"]/div[2]/div/button')
    time.sleep(5)
#----------------------------fasi--------------------------------------
    try:
        click('//*[@id="create-app-price"]/div[3]/label[2]/div[1]')
    except:
        byxpath('//*[@id="create-app-price"]/div[3]/label[2]/div[1]').click()

    byxpath('//*[@id="create-app-price"]/div[3]/label[2]/input').send_keys(scraped["fasi"])
    time.sleep(2)
#----------------------------dasruleba--------------------------------------
    try:
        into_view_xpath("//button[contains(text(), 'გაგრძელება')]")
        click("//button[contains(text(), 'გაგრძელება')]")
    except:
        click('//*[@id="__next"]/div[1]/div[1]/button')

    try:
        try:
            print("CLICKING BALANSIT")
            into_view_xpath('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
            click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
        except:
            print("CLICKING EXTERNALLY BALANSIT")
            into_view_xpath("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
            click("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
    except:
        print("SKIPPING BALANSIT")
        pass

    try:
        print("CLICKING GANCXADEBIS GANTAVSEBA")
        into_view_xpath("//button[contains(text(), 'განაცხადის განთავსება')]")
        click("//button[contains(text(), 'განაცხადის განთავსება')]")
    except:
        print("CLICKING EXTERNALLY GANCXADEBIS GANTAVSEBA")
        click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[2]/div[2]/button')

    # -----------------------------gadaxda-------------------------------------
    if byxpath("//h6[contains(text(), 'განცხადება წარმატებით აიტვირთა')]", 15):
        print("FOUND")
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()
    else:
        time.sleep(5)
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()

#------------------------------------------------------------------
#------------------------------------------------------//*[@id="create-app-type"]/div[2]/div[2]------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------


#scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება 3 ოთახიანი ბინა ვაკეში', 'qalaqi': 'თბილისი', 'id': '17496132', 'misamarti': 'ილია ჭავჭავაძის გამზირი ', 'fasi': '570000', 'parti': '132', 'otax-raodenoba': 3, 'sadzinebeli': 2, 'sartuli': 10, 'sartuli-sul': 22, 'status': 'ახალი აშენებული', 'build_year': '>2000', 'condition': '1', 'bathroom_type_id': '2', 'balconies': '1', 'balcony_area': '900', 'hot_water_type': None, 'heating_type': None, 'parking_type': None, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['furniture', 'porch', 'telephone', 'conditioner']}

def publish_ss_house(scraped, description, driver, info_for_database ):

    open_site("https://home.ss.ge/ka/udzravi-qoneba/create", driver)


    def click(xpath):
        return driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, xpath=xpath))

    def click_element(element):
        return driver.execute_script("arguments[0].click();", element)

    def into_view(element):
        return driver.execute_script("arguments[0].scrollIntoView();", element)

    def into_view_xpath(xpath):
        return driver.execute_script("arguments[0].scrollIntoView();", wait_until_xpath(10, driver, xpath=xpath))


    def byxpath(xpath, time=10):
        return wait_until_xpath(time, driver, xpath)

    def set_field_value_with_js(driver, element, value):
        driver.execute_script("""
            arguments[0].value = arguments[1]; // Set the value
            arguments[0].dispatchEvent(new Event('input', { bubbles: true })); // Trigger input event
            arguments[0].dispatchEvent(new Event('change', { bubbles: true })); // Trigger change event
        """, element, value)


    with open("config.json", "r", encoding="utf-8") as cfg:
        encoded_config = json.load(cfg)["encoded_data"]
        decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

        # mhemail = decoded_config["credentials"]["myhome"]["email"]
        # mhpassword = decoded_config["credentials"]["myhome"]["password"]
        mhemail = decoded_config["credentials"]["ss.ge"]["email"]
        mhpassword = decoded_config["credentials"]["ss.ge"]["password"]
        contact_name = decoded_config["contact"]["name"]
        contact_number = decoded_config["contact"]["number"]

      #  mhemail = "iceobladey21@gmail.com"
      #  mhpassword = "Dato2006"
       # contact_number = "599544130"

    # LOGIN
    try:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div/div[2]/button[2]'))
    except:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div[1]/div'))
    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[1]/input').send_keys(mhemail)
    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[2]/input').send_keys(mhpassword)
    driver.execute_script("arguments[0].click();",
                          wait_until_xpath(10, driver, '//*[@id="card"]/div/div/div[2]/div/form/button[2]'))

    if byxpath("//button[text()='გააგრძელე განთავსება']", 10):  # TU WINA GANCXADEBIS DAMATEBIS POPUPI
        click('//*[@id="__next"]/div[1]/div[1]/div/div/div[2]/button[1]')

    def until_photos(scraped_id):
        try:
            click('//*[@id="create-app-type"]/div[2]/div[2]')
            click('//*[@id="create-app-type"]/div[3]/div[1]')

            # Locate and prepare photo files
            photo_folder = f"images/{scraped_id}"
            photo_files = glob.glob(os.path.join(photo_folder, "*.jpg"))  # More efficient

            if not photo_files:
                raise FileNotFoundError(f"No JPG images found in {photo_folder}")

            file_paths = "\n".join(os.path.abspath(f) for f in photo_files)

            file_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
            )
            file_input.send_keys(file_paths)

        except Exception as e:
            print(f"Error in until_photos: {e}")

    def retry_until_photos(scraped_id, retries=2):
        """Retries uploading photos in case of failure."""
        for attempt in range(retries):
            try:
                until_photos(scraped_id)
                return  # Exit if successful
            except Exception as e:
                print(f"Retry {attempt + 1}/{retries} failed: {e}")

    retry_until_photos(scraped["id"])

#------------------qalaqi----------------------------------------------
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[1]/div/div/div[1]/div[2]', 10)
    into_view(dropdown)
    dropdown.click()
    city_option = byxpath(f"//div[contains(@class, 'select__option') and text()='{scraped['qalaqi']}']")
    into_view(city_option)
    click_element(city_option)
#------------------qucha------------------------------------------------

    # Split the scraped address into individual words
    words = scraped["misamarti"].split()
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[1]/div[1]/div')
    into_view(dropdown)
    dropdown.click()

    for word in words:
        forbidden = ["ა.","ბ.","გ.","დ.","ე.""ვ.","ზ.","თ.","ი.","კ.","ლ.","მ.","ნ.","ო.","პ.","ჟ.","რ.","ს.","ტ.","უ.","ჭ.","წ."]
        if word in forbidden:
            continue
        try:
            city_option = byxpath(f"//div[contains(@class, 'select__option') and contains(text(), '{word}')]")
            into_view(city_option)
            click_element(city_option)
            print(f"Clicked option containing word: {word}")
            break  # dacheris shemdeg gamodis loopidan
        except Exception as ex:
            print(f"shecdoma misamartshi: {word}, error: {ex}")
#-----------------------------------saxlis nomeri--------------------------------------
    try:
        click('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input')
    except:
        byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').click()
    byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').send_keys("3")

#--------------------otaxebi----------------------------------------------
    otaxebis_container = byxpath('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div')
    if scraped["otax-raodenoba"] >= 9:
        click_element(wait_until_xpath(10, otaxebis_container, f".//*[contains(text(), '8')]"))
    else:
        click_element(wait_until_xpath(10, otaxebis_container, f".//*[contains(text(), '{scraped['otax-raodenoba']}')]"))
#-----------------------sadzinebeli-------------------------------------------
    sadzinebeli_container = byxpath('//*[@id="create-app-details"]/div[2]/div[2]/div[2]/div')
    if scraped["sadzinebeli"] != None:
        try:
            click_element(
                wait_until_xpath(10, sadzinebeli_container, f".//*[contains(text(), '{scraped['sadzinebeli']}')]"))
        except:
            wait_until_xpath(10, sadzinebeli_container, f".//*[contains(text(), '{scraped['sadzinebeli']}')]").click()

    else:
        click_element(
            wait_until_xpath(10, sadzinebeli_container, f".//*[contains(text(), '1')]"))


#-------------------------saerto parti-----------------------------------------

    byxpath('//*[@id="create-app-details"]/div[2]/div[3]/div[2]/div/label/div/input').send_keys(scraped["parti"])
    if scraped["yard_area"] == "None" or scraped["yard_area"] == None:
        byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div/label/div/input').send_keys("1")
    else:
        byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div/label/div/input').send_keys(scraped["yard_area"])
#------------------------------sartuli/sartulianoba------------------------------------
    #byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div[1]/label/div/input').send_keys(scraped["sartuli"])
    #byxpath('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div[2]/label/div/input').send_keys(scraped["sartuli-sul"])
#--------------------------------statusis tipi----------------------------------

    click('//*[@id="create-app-details"]/div[2]/div[5]/div[2]/div/div[1]')
    #axali remontit
    click('//*[@id="create-app-details"]/div[2]/div[6]/div[2]/div/div[5]')
#-----------------------------proeqt tipi-------------------------------------

#-----------------------------mdgomareoba-------------------------------------
#------------------------------damatebiti informeishen------------------------------------

    if scraped["heating_type"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[5]')
    if scraped["hot_water_type"] == 6: #cent gatboba
        click('//*[@id="create-app-additional-info"]/div[2]/div[6]')


    match scraped["additions"]:
        case "elevator":
            click('//*[@id="create-app-additional-info"]/div[2]/div[5]')



    if scraped["balconies"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[1]') # aivani
    if scraped["store_room_area"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[7]') # satavso
#--------------------------descripsheni----------------------------------------
    byxpath('//*[@id="create-app-desc"]/div[2]/textarea').send_keys(description)
    click('//*[@id="create-app-desc"]/div[2]/div/button')
    time.sleep(4)
#----------------------------fasi--------------------------------------
    try:
        click('//*[@id="create-app-price"]/div[3]/label[2]/div[1]')
    except:
        byxpath('//*[@id="create-app-price"]/div[3]/label[2]/div[1]').click()

    byxpath('//*[@id="create-app-price"]/div[3]/label[2]/input').send_keys(scraped["fasi"])
    time.sleep(2)


#----------------------------dasruleba--------------------------------------
    try:
        into_view_xpath("//button[contains(text(), 'გაგრძელება')]")
        click("//button[contains(text(), 'გაგრძელება')]")
    except:
        click('//*[@id="__next"]/div[1]/div[1]/button')

    try:
        try:
            print("CLICKING BALANSIT")
            into_view_xpath('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
            click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
        except:
            print("CLICKING EXTERNALLY BALANSIT")
            into_view_xpath("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
            click("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
    except:
        print("SKIPPING BALANSIT")
        pass

    try:
        print("CLICKING GANCXADEBIS GANTAVSEBA")
        into_view_xpath("//button[contains(text(), 'განაცხადის განთავსება')]")
        click("//button[contains(text(), 'განაცხადის განთავსება')]")
    except:
        print("CLICKING EXTERNALLY GANCXADEBIS GANTAVSEBA")
        click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[2]/div[2]/button')

    # -----------------------------gadaxda-------------------------------------
    if byxpath("//h6[contains(text(), 'განცხადება წარმატებით აიტვირთა')]", 15):
        print("FOUND")
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()
    else:
        time.sleep(5)
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()

#------------------------------------------------------------------
#------------------------------------------------------//*[@id="create-app-type"]/div[2]/div[2]------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------


def publish_ss_com(scraped, description, driver, info_for_database):

    open_site('https://home.ss.ge/ka/udzravi-qoneba/create', driver)


    def click(xpath, time=10):
        return driver.execute_script("arguments[0].click();", wait_until_xpath(time, driver, xpath=xpath))

    def click_element(element):
        return driver.execute_script("arguments[0].click();", element)

    def into_view(element):
        return driver.execute_script("arguments[0].scrollIntoView();", element)

    def into_view_xpath(xpath):
        return driver.execute_script("arguments[0].scrollIntoView();", wait_until_xpath(10, driver, xpath=xpath))


    def byxpath(xpath, time=10):
        return wait_until_xpath(time, driver, xpath)

    def set_field_value_with_js(driver, element, value):
        driver.execute_script("""
            arguments[0].value = arguments[1]; // Set the value
            arguments[0].dispatchEvent(new Event('input', { bubbles: true })); // Trigger input event
            arguments[0].dispatchEvent(new Event('change', { bubbles: true })); // Trigger change event
        """, element, value)


    with open("config.json", "r", encoding="utf-8") as cfg:
        encoded_config = json.load(cfg)["encoded_data"]
        decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

        # mhemail = decoded_config["credentials"]["myhome"]["email"]
        # mhpassword = decoded_config["credentials"]["myhome"]["password"]
        mhemail = decoded_config["credentials"]["ss.ge"]["email"]
        mhpassword = decoded_config["credentials"]["ss.ge"]["password"]
        contact_name = decoded_config["contact"]["name"]
        contact_number = decoded_config["contact"]["number"]

    # LOGIN
    try:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div/div[2]/button[2]'))
    except:
        driver.execute_script("arguments[0].click();",
                              wait_until_xpath(10, driver, '//*[@id="__next"]/header/div[1]/div'))

    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[1]/input').send_keys(mhemail)
    byxpath('//*[@id="card"]/div/div/div[2]/div/form/div/label[2]/input').send_keys(mhpassword)
    driver.execute_script("arguments[0].click();",
                          wait_until_xpath(10, driver, '//*[@id="card"]/div/div/div[2]/div/form/button[2]'))

    if byxpath("//button[text()='გააგრძელე განთავსება']", 10):  # TU WINA GANCXADEBIS DAMATEBIS POPUPI
        click('//*[@id="__next"]/div[1]/div[1]/div/div/div[2]/button[1]')

    def upload_photos(scraped_id):
        """Handles uploading photos for a given scraped ID."""
        try:
            click('//*[@id="create-app-type"]/div[2]/div[5]')
            click('//*[@id="create-app-type"]/div[3]/div[1]')

            # Locate and prepare photo files
            photo_folder = os.path.join("images", str(scraped_id))
            photo_files = glob.glob(os.path.join(photo_folder, "*.jpg"))

            if not photo_files:
                raise FileNotFoundError(f"No JPG images found in {photo_folder}")

            file_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
            )

            # Join file paths with newline and send to input
            file_input.send_keys("\n".join(map(os.path.abspath, photo_files)))
            print("Photos uploaded successfully.")

        except Exception as e:
            print(f"Error in upload_photos: {e}")
            raise

    def retry_upload_photos(scraped_id, retries=2):
        """Retries the photo upload process in case of failure."""
        for attempt in range(retries):
            try:
                upload_photos(scraped_id)
                return  # Exit if successful
            except Exception as e:
                print(f"Retry {attempt + 1}/{retries} failed: {e}")
        print("Photo upload failed after multiple attempts.")

    # Example usage
    scraped_id = scraped["id"]  # Ensure this is an integer or string
    retry_upload_photos(scraped_id)

#------------------qalaqi----------------------------------------------
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[1]/div/div/div[1]/div[2]')
    into_view(dropdown)
    dropdown.click()
    city_option = byxpath(f"//div[contains(@class, 'select__option') and text()='{scraped['qalaqi']}']")
    into_view(city_option)
    click_element(city_option)
#------------------qucha------------------------------------------------

    # Split the scraped address into individual words
    words = scraped["misamarti"].split()
    dropdown = byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[1]/div[1]/div')
    into_view(dropdown)
    dropdown.click()

    for word in words:
        forbidden = ["ა.","ბ.","გ.","დ.","ე.""ვ.","ზ.","თ.","ი.","კ.","ლ.","მ.","ნ.","ო.","პ.","ჟ.","რ.","ს.","ტ.","უ.","ჭ.","წ."]
        if word in forbidden:
            continue
        try:
            city_option = byxpath(f"//div[contains(@class, 'select__option') and contains(text(), '{word}')]")
            into_view(city_option)
            click_element(city_option)
            print(f"Clicked option containing word: {word}")
            break  # dacheris shemdeg gamodis loopidan
        except Exception as ex:
            print(f"shecdoma misamartshi: {word}, error: {ex}")
#-----------------------------------saxlis nomeri--------------------------------------
    try:
        click('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input')
    except:
        byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').click()
    byxpath('//*[@id="create-app-loc"]/div[2]/div[2]/div[2]/label/div[1]/input').send_keys("3")
#-------------------------saerto parti-----------------------------------------

    byxpath('//*[@id="create-app-details"]/div[2]/div[2]/div[2]/div/label/div/input').send_keys(scraped["parti"])

#KOM PARTIS TIPIS ARCHEVA
    match True:
        case _ if "სპეციალური" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[7]')
        case _ if "საოფისე" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[2]')
        case _ if "სავაჭრო" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[6]')
        case _ if "სასაწყობე" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[1]')
        case _ if "საწარმოო" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[1]')
        case _ if "კვების ობიექტი" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[3]')
        case _ if "ავტოფარეხი" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[4]')
        case _ if "სარდაფი" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[5]')
        case _ if "ნახევარსარდაფი" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[5]')
        case _ if "მთლიანი შენობა" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[7]')
        case _ if "ავტოსამრეცხაო" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[7]')
        case _ if "ავტოსერვისი" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[4]')
        case _ if "უნივერსალური" in scraped["saxeli"]:
            click('//*[@id="create-app-details"]/div[2]/div[1]/div[2]/div/div[7]')
#------------------------------------------------------------------
    status_container = byxpath('//*[@id="create-app-details"]/div[2]/div[3]/div[2]/div')
    click_element(
        wait_until_xpath(10, status_container, f".//*[contains(text(), '{scraped['status']}')]"))
#-----------------------------mdgomareoba-------------------------------------
    click('//*[@id="create-app-details"]/div[2]/div[4]/div[2]/div/div[5]') # axali remontit only
#------------------------------damatebiti informeishen------------------------------------

    if scraped["heating_type"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[12]')
        click('//*[@id="create-app-additional-info"]/div[2]/div[9]')

    match scraped["additions"]:
        case "elevator":
            click('//*[@id="create-app-additional-info"]/div[2]/div[3]')
        case "refrigerator":
            click('//*[@id="create-app-additional-info"]/div[2]/div[5]')
        case "conditioner":
            click('//*[@id="create-app-additional-info"]/div[2]/div[1]')
        case "internet":
            click('//*[@id="create-app-additional-info"]/div[2]/div[10]')
        case "tv":
            click('//*[@id="create-app-additional-info"]/div[2]/div[16]')
            click('//*[@id="create-app-additional-info"]/div[2]/div[4]')
        case 'furniture':
            click('//*[@id="create-app-additional-info"]/div[2]/div[6]')
        case 'telephone':
            click('//*[@id="create-app-additional-info"]/div[2]/div[15]')

    if scraped["balconies"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[2]') # aivani
    if scraped["store_room_area"] != None:
        click('//*[@id="create-app-additional-info"]/div[2]/div[14]') # satavso

    # if scraped["sartuli"] == scraped["sartuli-sul"]:
    #     click('//*[@id="create-app-additional-info"]/div[2]/div[6]') #bolo sartuli
        #GARAJI DA SARDAPI AR GVAQVS
#--------------------------descripsheni----------------------------------------
    byxpath('//*[@id="create-app-desc"]/div[2]/textarea').send_keys(description)
    click('//*[@id="create-app-desc"]/div[2]/div/button')
    time.sleep(4)
#----------------------------fasi--------------------------------------
    try:
        click('//*[@id="create-app-price"]/div[3]/label[2]/div[1]')
    except:
        byxpath('//*[@id="create-app-price"]/div[3]/label[2]/div[1]').click()

    byxpath('//*[@id="create-app-price"]/div[3]/label[2]/input').send_keys(scraped["fasi"])
    time.sleep(2)
#----------------------------dasruleba--------------------------------------
    try:
        into_view_xpath("//button[contains(text(), 'გაგრძელება')]")
        click("//button[contains(text(), 'გაგრძელება')]")
    except:
        click('//*[@id="__next"]/div[1]/div[1]/button')

    try:
        try:
            print("CLICKING BALANSIT")
            into_view_xpath('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
            click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[1]/div[1]')
        except:
            print("CLICKING EXTERNALLY BALANSIT")
            into_view_xpath("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
            click("//div[contains(@class, 'default_pointer_cs') and .//div[text()='ბალანსით']]")
    except:
        print("SKIPPING BALANSIT")
        pass

    try:
        print("CLICKING GANCXADEBIS GANTAVSEBA")
        into_view_xpath("//button[contains(text(), 'განაცხადის განთავსება')]")
        click("//button[contains(text(), 'განაცხადის განთავსება')]")
    except:
        print("CLICKING EXTERNALLY GANCXADEBIS GANTAVSEBA")
        click('//*[@id="__next"]/div[1]/div/div/div[3]/div/div[2]/div[2]/button')

    # -----------------------------gadaxda-------------------------------------
    if byxpath("//h6[contains(text(), 'განცხადება წარმატებით აიტვირთა')]", 15):
        print("FOUND")
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()
    else:
        time.sleep(5)
        ss_link = find_id_ss(driver)
        info_for_database["SS_LINK"] = ss_link
        to_database(info_for_database)
        driver.quit()

# iyideba_scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება სავაჭრო კომერციული ფართი დიდ დიღომში', 'qalaqi': 'თბილისი', 'id': '20547178', 'misamarti': 'ფარსადანის ქ. ', 'fasi': '51000', 'parti': '60', 'otax-raodenoba': 1, 'sadzinebeli': None, 'sartuli': 1, 'sartuli-sul': 12, 'status': '', 'build_year': '>2000', 'condition': '3', 'bathroom_type_id': 'None', 'balconies': 'None', 'balcony_area': 'None', 'hot_water_type': None, 'heating_type': None, 'parking_type': 4, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['internet', 'tv', 'gas', 'water', 'sewerage', 'electricity'], 'yard_area': None, 'district_name': 'ვაკე-საბურთალო', 'owner-number': '511 111 847', 'owner-name': 'ლუკა', 'agenti': 'SafeHome'}
# qiravdeba_scraped = {'tipi': 'ქირავდება', 'saxeli': 'ქირავდება მთლიანი შენობა კომერციული ფართი დიდ დიღომში', 'qalaqi': 'თბილისი', 'id': '18873395', 'misamarti': 'ფარსადანის ქ. 9', 'fasi': '2300', 'parti': '258', 'otax-raodenoba': 1, 'sadzinebeli': None, 'sartuli': 1, 'sartuli-sul': 16, 'status': '', 'build_year': '>2000', 'condition': '5', 'bathroom_type_id': 'None', 'balconies': 'None', 'balcony_area': 'None', 'hot_water_type': 8, 'heating_type': 7, 'parking_type': 2, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['gas', 'water', 'sewerage', 'electricity'], 'yard_area': None, 'district_name': 'ვაკე-საბურთალო', 'owner-number': '595 999 974', 'owner-name': 'ნინო', 'agenti': 'SafeHome'}
# publish_ss_com(iyideba_scraped,"gela", cdriver(), {})