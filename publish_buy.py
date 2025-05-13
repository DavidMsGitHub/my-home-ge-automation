from for_driver import *
from pay_and_upload import payment_part, find_id_myhome, to_database
import os
from datetime import datetime
import re
import time
from funqciebi import submit_error
from publish_buy_ss import publish_ss, publish_ss_house, publish_ss_com

def publish(scraped,description, driver, to_ssge):
    try:
        with open("config.json", "r", encoding="utf-8") as cfg:
            encoded_config = json.load(cfg)["encoded_data"]
            decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

            mhemail = decoded_config["credentials"]["myhome"]["email"]
            mhpassword = decoded_config["credentials"]["myhome"]["password"]
            print(mhemail, mhpassword)
            # ssemail = decoded_config["credentials"]["ss.ge"]["email"]
            # sspassword = decoded_config["credentials"]["ss.ge"]["password"]
            contact_name = decoded_config["contact"]["name"]
            contact_number = decoded_config["contact"]["number"]


        open_site('https://statements.tnet.ge/ka/statement/create?referrer=myhome', driver)

        wait_until_cs("button.luk-px-5", 10, driver).click()
        wait_until_id(10, driver, "Email").send_keys(mhemail)
        wait_until_id(10, driver, "Password").send_keys(mhpassword)
        wait_until_cs("button.gradient-button", 10, driver).click()

        bina_gilaki = wait_until_clickable_xpath('//*[@id="0"]/div[2]/div/div/div/div[1]/label', 30, driver)
        bina_gilaki.click()


        if scraped["tipi"] == "იყიდება":
            wait_until_xpath(10, driver, '//*[@id="0"]/div[3]/div/div/div/div[1]/label').click()
        wait_until_cs( "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12",10, driver).click()

        match scraped["qalaqi"]:
            case "თბილისი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[1]'))
            case "ბათუმი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[2]'))
            case "ბაკურიანი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[8]'))

        field = wait_until_xpath(10, driver, "//label[@for=':ri:']/input")
        misamarti = scraped["misamarti"]
        try:
            field.send_keys(misamarti)
            listo = wait_until_cs( 'ul.list-none',5, driver)
            first_result = wait_until_cs( "li.cursor-pointer",5, listo)
            driver.execute_script("arguments[0].click();", first_result)
        except:
            field.clear()
            field.send_keys(re.sub(r"[-#,0-9]", "", misamarti))
            listo = wait_until_cs('ul.list-none', 10, driver)
            first_result = wait_until_cs("li.cursor-pointer", 10, listo)
            driver.execute_script("arguments[0].click();", first_result)

        label_element = wait_until_xpath(30, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
        driver.execute_script("arguments[0].click();", label_element)

        if scraped["sadzinebeli"] != None and scraped["sadzinebeli"] > 0:
            element = wait_until_clickable_xpath(time=10, driver=driver, xpath='//*[@id="1"]/div[2]/div/div[4]/div/div')
            elements = element.find_elements(By.TAG_NAME, "span")
            for i in elements:
                if i.text == str(scraped["sadzinebeli"]):
                    driver.execute_script("arguments[0].click();", i)
                    break

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

        driver.execute_script("arguments[0].click();",
                              wait_until_clickable_xpath('//*[@id="2"]/div[3]/div[3]/div[2]/div[2]/div[2]', 20, driver))
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])

        #contact information
        wait_until_xpath(10, driver, '//*[@id=":r1j:"]').send_keys(contact_name)
        wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE ,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, contact_number)
        #description geo,eng,rus
        wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[2]/div/textarea').send_keys(description)

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
        # Folder containing your photos
        photo_folder = f'images/{scraped["id"]}/'
        photo_files = []

        # Collect all .png file paths
        for f in os.listdir(photo_folder):
            if f.endswith(".jpg"):
                photo_files.append(os.path.abspath(os.path.join(photo_folder, f)))

        # Combine file paths into a single string separated by newlines
        file_paths = "\n".join(photo_files)

        # Wait for the actual input element with type="file" to appear
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )

        # Send the file paths directly to the input element
        file_input.send_keys(file_paths)


        # ashenebis weli
        if scraped["build_year"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[12]/div/div/div'))

            match scraped["build_year"]:
                case ">2000":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[3]'))
                case "1995-2000":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[2]'))
                case "<1995":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[1]'))

        # ashenebis weli

        # parkingis tipi
        if scraped["parking_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[22]/div/div/div'))
            match scraped["parking_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[6]'))
        # parkingis tipi

        #-------- gatbobis tipi
        if scraped["heating_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div'))
            match scraped["heating_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[7]'))
                case _:
                    pass
        # -------- gatbobis tipi

        # -------- cxeli wyalis tipi
        if scraped["hot_water_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[24]/div/div/div'))

            match scraped["hot_water_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[7]'))
                case 8:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[8]'))

        # -------- cxeli wylis tipi

        #--------sveli wertilis archeva

        if scraped["bathroom_type_id"] != "null":
            list_of_bti = wait_until_xpath(10,driver, '//*[@id="1"]/div[2]/div/div[6]/div/div/div')
            driver.execute_script("arguments[0].click();", list_of_bti)
            if scraped["bathroom_type_id"] == "1":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[1]'))
            elif scraped["bathroom_type_id"] == "2":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[2]'))
            elif scraped["bathroom_type_id"] == "3":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[3]'))
            else:
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[4]'))

        #----------- sveli wertilis archeva

        #aivnebi tu dafiqsirda chaweros
        if scraped["balconies"] != None:
            wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[1]/div/label').send_keys(scraped["balconies"])
            wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys(scraped["balcony_area"])

            if scraped["balcony_area"] == None or scraped["balcony_area"] == "None":
                wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys("1")
        # aivnani

    # ----------- PARAMETREBIS GILAKEBIS MDEBAREOBEBI
        int_button = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div/div/div[1]', 20, driver)
        televizia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[2]')
        bunebrivi_airi = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[3]')
        lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[4]')
        satvirto_lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[5]')
        wyali = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[6]')
        kanalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[7]')
        eleqtroenergia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[8]')
        telefoni = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[9]')
        samzareulo_teqnika = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[10]')

        #upiratesobebi

        spa = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[1]')
        bari = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[2]')
        sport_darbazi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[3]')
        buxari = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[4]')
        mayali_grili = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[5]')
        jakuzi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[6]')
        sauna = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[7]')
        signalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[8]')
        vintilacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[9]')
        dacva = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[10]')

        #aveji da teqnika
        aveji = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[1]')
        sawoli = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[2]')
        divani = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[3]')
        magida = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[4]')
        skamebi = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[5]')
        qura = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[6]')
        gumeli = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[7]')
        kondicioneri = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[8]')
        macivari = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[9]')
        sarecxi_manqana = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[10]')
        churchlis_sarecxi = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[11]')
        # bejebi
        kari_kodit = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[1]')
        airbnb_booking = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[2]')
        sainvesticio = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[3]')
        ssmp = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[4]')



        # zeda gilakebi
        loggia = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[5]/span/div/label', 10, driver)
        veranda = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[7]/span/div/label', 10, driver)
        satavsos_tipi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[9]/span/div/label', 10, driver)
        sacurao_auzi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[1]/span/div/label', 10, driver)
        misaghebi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[3]/span/div/label', 10, driver)


    # ----------- PARAMETREBI

        time.sleep(1)
        for parameter in scraped["additions"]:
            match parameter:
                case "internet":
                    driver.execute_script("arguments[0].click();", int_button)
                case "conditioner":
                    driver.execute_script("arguments[0].click();", kondicioneri)
                case "bed":
                    driver.execute_script("arguments[0].click();", sawoli)
                case "gas":
                    driver.execute_script("arguments[0].click();", bunebrivi_airi)
                case "sofa":
                    driver.execute_script("arguments[0].click();", divani)
                case "tv":
                    driver.execute_script("arguments[0].click();", televizia)
                case "furniture":
                    driver.execute_script("arguments[0].click();", aveji)
                case "elevator":
                    driver.execute_script("arguments[0].click();", lifti)
                case "truck_elevator":
                    driver.execute_script("arguments[0].click();", satvirto_lifti)
                case "table":
                    driver.execute_script("arguments[0].click();", magida)
                case "chairs":
                    driver.execute_script("arguments[0].click();", skamebi)
                case "stove":
                    driver.execute_script("arguments[0].click();", qura)
                case "oven":
                    driver.execute_script("arguments[0].click();", gumeli)
                case "water":
                    driver.execute_script("arguments[0].click();", wyali)
                case "sewerage":
                    driver.execute_script("arguments[0].click();", kanalizacia)
                case "electricity":
                    driver.execute_script("arguments[0].click();", eleqtroenergia)
                case "telephone":
                    driver.execute_script("arguments[0].click();", telefoni)
                case "refrigerator":
                    driver.execute_script("arguments[0].click();", macivari)
                case "washing_machine":
                    driver.execute_script("arguments[0].click();", sarecxi_manqana)
                case "kitchen":
                    driver.execute_script("arguments[0].click();", samzareulo_teqnika)
                case "investment":
                    driver.execute_script("arguments[0].click();", sainvesticio)
                case "alarm":
                    driver.execute_script("arguments[0].click();", signalizacia)
                case "guard":
                    driver.execute_script("arguments[0].click();", dacva)
                case "ventilation":
                    driver.execute_script("arguments[0].click();", vintilacia)
                case "coded-door":
                    driver.execute_script("arguments[0].click();", kari_kodit)
                case "bar":
                    driver.execute_script("arguments[0].click();", bari)
                case "gym":
                    driver.execute_script("arguments[0].click();", sport_darbazi)
                case "spa":
                    driver.execute_script("arguments[0].click();", spa)
                case "grill":
                    driver.execute_script("arguments[0].click();", mayali_grili)
                case "jacuzzi":
                    driver.execute_script("arguments[0].click();", jakuzi)
                case "sauna":
                    driver.execute_script("arguments[0].click();", sauna)
                case "airbnb_booking_account":
                    driver.execute_script("arguments[0].click();", airbnb_booking)
                case "dishwasher":
                    driver.execute_script("arguments[0].click();", churchlis_sarecxi)
                case "storeroom":
                    driver.execute_script("arguments[0].scrollIntoView();", satavsos_tipi)
                    driver.execute_script("arguments[0].click();", satavsos_tipi)
                    if scraped["store_room_area"] != None:
                        sacavis_parti_entry = wait_until_xpath(xpath='//*[@id="1"]/div[3]/div/div[9]/span/div/label',
                                                               driver=driver, time=10)
                        sacavis_parti_entry.send_keys(scraped["store_room_area"])
                case "loggia":
                    driver.execute_script("arguments[0].click();", loggia)
                    if scraped["loggia_area"] != None:
                        wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[5]/span/div/label').send_keys(scraped["loggia_area"])

                case "swimming_pool":
                    driver.execute_script("arguments[0].click();", sacurao_auzi)
                case "porch":
                    driver.execute_script("arguments[0].click();", veranda)
                    if scraped["porch_area"] != None:
                        porch_area = wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[8]/div/div/label')
                        porch_area.send_keys(scraped["porch_area"])


        # case "for-parties":
        #     driver.execute_script("arguments[0].click();", for_parties)
        # case "cellar":
        #     driver.execute_script("arguments[0].click();", cellar)
        # case "fenced":
        #     driver.execute_script("arguments[0].click();", dacva)
        # case "gate":
        #     driver.execute_script("arguments[0].click();", gate)
        # case "with_a_yard":
        #     driver.execute_script("arguments[0].click();", with_a_yard)

        # case "pets-allowed":
        #     driver.execute_script("arguments[0].click();", pets_allowed)
        # case "with_buildings":
        #     driver.execute_script("arguments[0].click();", with_buildings)


        # #upload and payment
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"


        payment_part(driver)
        if driver.find_element(By.TAG_NAME, "circle"):
            ID = find_id_myhome(driver)
            info_for_database = {
                "MYHOME-ID": ID,
                "MYHOME-LINK": f"https://myhome.ge/pr/{ID}",
                "OWNER NAME": scraped["owner-name"],
                "OWNER NUMBER": scraped["owner-number"],
                "PARTI": scraped["parti"],
                "OTAXI": scraped["otax-raodenoba"],
                "BEDROOMS": scraped["sadzinebeli"],
                "CONDITION": scraped["status"],
                "PRICE": scraped["fasi"],
                "ADDRESS": scraped["misamarti"],
                "REGION": scraped["district_name"],
                "AGENTISSAXELI": scraped["agenti"],
                "TARIGI": current_time,
            }
            if to_ssge:
                try:
                    publish_ss(scraped, description, driver, info_for_database)
                except:
                    info_for_database["SS_LINK"] = "Error SS.GE-ze"
                    to_database(info_for_database)
                    driver.quit()
            else:
                info_for_database["SS_LINK"] = "No SS.GE"
                to_database(info_for_database)
                driver.quit()


    except Exception as e:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        data = f"{current_time} <||> {scraped['id']}"
        with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
            log.write(f"{data}\n")
        submit_error(scraped["id"], current_time)
        time.sleep(2)

#scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება 3 ოთახიანი ბინა ვაკეში', 'qalaqi': 'თბილისი', 'id': '17496132', 'misamarti': 'ილია ჭავჭავაძის გამზირი ', 'fasi': '570000', 'parti': '132', 'otax-raodenoba': 3, 'sadzinebeli': 2, 'sartuli': 10, 'sartuli-sul': 22, 'status': 'ახალი აშენებული', 'build_year': '>2000', 'condition': '1', 'bathroom_type_id': '2', 'balconies': '1', 'balcony_area': '900', 'hot_water_type': None, 'heating_type': None, 'parking_type': None, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['furniture', 'porch', 'telephone', 'conditioner']}
#publish(scraped, "gelashavarkakasha")


def publish_house(scraped,description, driver, to_ssge):
    try:
                    # get credentials
        with open("config.json", "r", encoding="utf-8") as cfg:
            encoded_config = json.load(cfg)["encoded_data"]
            decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

            mhemail = decoded_config["credentials"]["myhome"]["email"]
            mhpassword = decoded_config["credentials"]["myhome"]["password"]
            # ssemail = decoded_config["credentials"]["ss.ge"]["email"]
            # sspassword = decoded_config["credentials"]["ss.ge"]["password"]
            contact_name = decoded_config["contact"]["name"]
            contact_number = decoded_config["contact"]["number"]


        open_site('https://statements.tnet.ge/ka/statement/create?referrer=myhome', driver)

        wait_until_cs("button.luk-px-5", 10, driver).click()
        wait_until_id(10, driver, "Email").send_keys(mhemail)
        wait_until_id(10, driver, "Password").send_keys(mhpassword)
        wait_until_cs("button.gradient-button", 10, driver).click()

        wait_until_clickable_xpath('//*[@id="0"]/div[2]/div/div/div/div[2]/label', 30, driver).click() # tipi

        if scraped["tipi"] == "იყიდება":
            wait_until_xpath(10, driver, '//*[@id="0"]/div[3]/div/div/div/div[1]/label').click()
        wait_until_cs( "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12",10, driver).click()

        match scraped["qalaqi"]:
            case "თბილისი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[1]'))
            case "ბათუმი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[2]'))
            case "ბაკურიანი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[8]'))

        field = wait_until_xpath(10, driver, "//label[@for=':ri:']/input")
        misamarti = scraped["misamarti"]
        try:
            field.send_keys(misamarti)
            listo = wait_until_cs( 'ul.list-none',5, driver)
            first_result = wait_until_cs( "li.cursor-pointer",5, listo)
            driver.execute_script("arguments[0].click();", first_result)
        except:
            field.clear()
            field.send_keys(re.sub(r"[-#,0-9]", "", misamarti))
            listo = wait_until_cs('ul.list-none', 10, driver)
            first_result = wait_until_cs("li.cursor-pointer", 10, listo)
            driver.execute_script("arguments[0].click();", first_result)

        label_element = wait_until_xpath(30, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
        driver.execute_script("arguments[0].click();", label_element)

        if scraped["sadzinebeli"] != None and scraped["sadzinebeli"] > 0:
            element = wait_until_clickable_xpath(time=10, driver=driver, xpath='//*[@id="1"]/div[2]/div/div[4]/div/div')
            elements = element.find_elements(By.TAG_NAME, "span")
            for i in elements:
                if i.text == str(scraped["sadzinebeli"]):
                    driver.execute_script("arguments[0].click();", i)
                    break

        wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div/div/label').send_keys(scraped["sartuli-sul"])
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

        driver.execute_script("arguments[0].click();",
                              wait_until_clickable_xpath('//*[@id="2"]/div[3]/div[3]/div[2]/div[2]/div[2]', 20, driver))
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])

        #contact information

        wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[2]/div/div/label').send_keys(contact_name)
        wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE ,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, contact_number)
        #description geo,eng,rus
        wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[2]/div/textarea').send_keys(description)

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
        # Folder containing your photos
        photo_folder = f'images/{scraped["id"]}/'
        photo_files = []

        # Collect all .png file paths
        for f in os.listdir(photo_folder):
            if f.endswith(".jpg"):
                photo_files.append(os.path.abspath(os.path.join(photo_folder, f)))

        # Combine file paths into a single string separated by newlines
        file_paths = "\n".join(photo_files)

        # Wait for the actual input element with type="file" to appear
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )

        # Send the file paths directly to the input element
        file_input.send_keys(file_paths)


        # ashenebis weli
        if scraped["build_year"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[12]/div/div/div'))

            match scraped["build_year"]:
                case ">2000":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[3]'))
                case "1995-2000":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[2]'))
                case "<1995":
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[1]'))

        # ashenebis weli

        # parkingis tipi
        if scraped["parking_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[22]/div/div/div'))
            match scraped["parking_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[6]'))
        # parkingis tipi

        #-------- gatbobis tipi
        if scraped["heating_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div'))
            match scraped["heating_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[7]'))
                case _:
                    pass
        # -------- gatbobis tipi

        # -------- cxeli wyalis tipi
        if scraped["hot_water_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[24]/div/div/div'))

            match scraped["hot_water_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[7]'))
                case 8:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[8]'))

        # -------- cxeli wylis tipi

        #--------sveli wertilis archeva

        if scraped["bathroom_type_id"] != "null":
            list_of_bti = wait_until_xpath(10,driver, '//*[@id="1"]/div[2]/div/div[6]/div/div/div')
            driver.execute_script("arguments[0].click();", list_of_bti)
            if scraped["bathroom_type_id"] == "1":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[1]'))
            elif scraped["bathroom_type_id"] == "2":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[2]'))
            elif scraped["bathroom_type_id"] == "3":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[3]'))
            else:
                driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[4]'))

        #----------- sveli wertilis archeva


        #aivnebi tu dafiqsirda chaweros
        if scraped["balconies"] != None:

            wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[1]/div/label').send_keys(scraped["balconies"])
            wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys(scraped["balcony_area"])

            if scraped["balcony_area"] == None or scraped["balcony_area"] == "None":
                wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys("1")
        # aivnani

    # ----------- PARAMETREBIS GILAKEBIS MDEBAREOBEBI
        int_button = wait_until_clickable_xpath('//*[@id="1"]/div[4]/div/div/div/div[1]', 20, driver)
        televizia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[2]')
        bunebrivi_airi = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[3]')
        lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[4]')
        satvirto_lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[5]')
        wyali = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[6]')
        kanalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[7]')
        eleqtroenergia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[8]')
        telefoni = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[9]')
        samzareulo_teqnika = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[10]')

        #upiratesobebi

        spa = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[1]')
        bari = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[2]')
        sport_darbazi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[3]')
        buxari = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[4]')
        mayali_grili = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[5]')
        jakuzi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[6]')
        sauna = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[7]')
        signalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[8]')
        vintilacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[9]')
        dacva = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[10]')

        #aveji da teqnika
        aveji = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[1]')
        sawoli = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[2]')
        divani = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[3]')
        magida = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[4]')
        skamebi = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[5]')
        qura = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[6]')
        gumeli = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[7]')
        kondicioneri = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[8]')
        macivari = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[9]')
        sarecxi_manqana = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[10]')
        churchlis_sarecxi = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[11]')
        # bejebi
        kari_kodit = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[1]')
        airbnb_booking = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[2]')
        sainvesticio = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[3]')
        ssmp = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[4]')



        # zeda gilakebi
        loggia = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[5]/span/div/label', 10, driver)
        veranda = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[7]/span/div/label', 10, driver)
        satavsos_tipi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[11]/span/div/label', 10, driver)
        sacurao_auzi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[1]/span/div/label', 10, driver)
        misaghebi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[3]/span/div/label', 10, driver)

        yard = byxpath('//*[@id="1"]/div[3]/div/div[9]/span/div/label', driver)


    # ----------- PARAMETREBI

        time.sleep(1)
        for parameter in scraped["additions"]:
            match parameter:
                case "internet":
                    driver.execute_script("arguments[0].click();", int_button)
                case "conditioner":
                    driver.execute_script("arguments[0].click();", kondicioneri)
                case "bed":
                    driver.execute_script("arguments[0].click();", sawoli)
                case "gas":
                    driver.execute_script("arguments[0].click();", bunebrivi_airi)
                case "sofa":
                    driver.execute_script("arguments[0].click();", divani)
                case "tv":
                    driver.execute_script("arguments[0].click();", televizia)
                case "furniture":
                    driver.execute_script("arguments[0].click();", aveji)
                case "elevator":
                    driver.execute_script("arguments[0].click();", lifti)
                case "truck_elevator":
                    driver.execute_script("arguments[0].click();", satvirto_lifti)
                case "table":
                    driver.execute_script("arguments[0].click();", magida)
                case "chairs":
                    driver.execute_script("arguments[0].click();", skamebi)
                case "stove":
                    driver.execute_script("arguments[0].click();", qura)
                case "oven":
                    driver.execute_script("arguments[0].click();", gumeli)
                case "water":
                    driver.execute_script("arguments[0].click();", wyali)
                case "sewerage":
                    driver.execute_script("arguments[0].click();", kanalizacia)
                case "electricity":
                    driver.execute_script("arguments[0].click();", eleqtroenergia)
                case "telephone":
                    driver.execute_script("arguments[0].click();", telefoni)
                case "refrigerator":
                    driver.execute_script("arguments[0].click();", macivari)
                case "washing_machine":
                    driver.execute_script("arguments[0].click();", sarecxi_manqana)
                case "kitchen":
                    driver.execute_script("arguments[0].click();", samzareulo_teqnika)
                case "investment":
                    driver.execute_script("arguments[0].click();", sainvesticio)
                case "alarm":
                    driver.execute_script("arguments[0].click();", signalizacia)
                case "guard":
                    driver.execute_script("arguments[0].click();", dacva)
                case "ventilation":
                    driver.execute_script("arguments[0].click();", vintilacia)
                case "coded-door":
                    driver.execute_script("arguments[0].click();", kari_kodit)
                case "bar":
                    driver.execute_script("arguments[0].click();", bari)
                case "gym":
                    driver.execute_script("arguments[0].click();", sport_darbazi)
                case "spa":
                    driver.execute_script("arguments[0].click();", spa)
                case "grill":
                    driver.execute_script("arguments[0].click();", mayali_grili)
                case "jacuzzi":
                    driver.execute_script("arguments[0].click();", jakuzi)
                case "sauna":
                    driver.execute_script("arguments[0].click();", sauna)
                case "airbnb_booking_account":
                    driver.execute_script("arguments[0].click();", airbnb_booking)
                case "dishwasher":
                    driver.execute_script("arguments[0].click();", churchlis_sarecxi)
                case "storeroom":
                    driver.execute_script("arguments[0].scrollIntoView();", satavsos_tipi)
                    driver.execute_script("arguments[0].click();", satavsos_tipi)
                    if scraped["store_room_area"] != None:
                        sacavis_parti_entry = wait_until_xpath(xpath='//*[@id="1"]/div[3]/div/div[12]/div[1]/div/label',
                                                               driver=driver, time=10)
                        sacavis_parti_entry.send_keys(scraped["store_room_area"])
                case "loggia":
                    driver.execute_script("arguments[0].click();", loggia)
                    if scraped["loggia_area"] != None:
                        wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[5]/span/div/label').send_keys(scraped["loggia_area"])

                case "swimming_pool":
                    driver.execute_script("arguments[0].click();", sacurao_auzi)
                case "porch":
                    driver.execute_script("arguments[0].click();", veranda)
                    if scraped["porch_area"] != None:
                        porch_area = wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[8]/div/div/label')
                        porch_area.send_keys(scraped["porch_area"])
                case "with_a_yard":
                    driver.execute_script("arguments[0].click();", yard)
                    if scraped["yard_area"] != None or scraped["yard_area"] != "None":
                        byxpath('//*[@id="1"]/div[3]/div/div[10]/div/div/label', driver).send_keys(scraped["yard_area"])


        # case "for-parties":
        #     driver.execute_script("arguments[0].click();", for_parties)
        # case "cellar":
        #     driver.execute_script("arguments[0].click();", cellar)
        # case "fenced":
        #     driver.execute_script("arguments[0].click();", dacva)
        # case "gate":
        #     driver.execute_script("arguments[0].click();", gate)

        # case "pets-allowed":
        #     driver.execute_script("arguments[0].click();", pets_allowed)
        # case "with_buildings":
        #     driver.execute_script("arguments[0].click();", with_buildings)


        # #upload and payment
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"


        payment_part(driver)
        if driver.find_element(By.TAG_NAME, "circle"):
            ID = find_id_myhome(driver)
            info_for_database = {
                "MYHOME-ID": ID,
                "MYHOME-LINK": f"https://myhome.ge/pr/{ID}",
                "OWNER NAME": scraped["owner-name"],
                "OWNER NUMBER": scraped["owner-number"],
                "PARTI": scraped["parti"],
                "OTAXI": scraped["otax-raodenoba"],
                "BEDROOMS": scraped["sadzinebeli"],
                "CONDITION": scraped["status"],
                "PRICE": scraped["fasi"],
                "ADDRESS": scraped["misamarti"],
                "REGION": scraped["district_name"],
                "AGENTISSAXELI": scraped["agenti"],
                "TARIGI": current_time,
            }
            if to_ssge:
                try:
                    publish_ss_house(scraped, description, driver, info_for_database)
                except:
                    info_for_database["SS_LINK"] = "Error SS.GE-ze"
                    to_database(info_for_database)
                    driver.quit()
            else:
                info_for_database["SS_LINK"] = "No SS.GE"
                to_database(info_for_database)
                driver.quit()





    except Exception as e:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        data = f"{current_time} <||> {scraped['id']}"
        with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
            log.write(f"{data}\n")
        submit_error(scraped["id"], current_time)
        time.sleep(2)

#scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება 3 ოთახიანი ბინა ვაკეში', 'qalaqi': 'თბილისი', 'id': '17496132', 'misamarti': 'ილია ჭავჭავაძის გამზირი ', 'fasi': '570000', 'parti': '132', 'otax-raodenoba': 3, 'sadzinebeli': 2, 'sartuli': 10, 'sartuli-sul': 22, 'status': 'ახალი აშენებული', 'build_year': '>2000', 'condition': '1', 'bathroom_type_id': '2', 'balconies': '1', 'balcony_area': '900', 'hot_water_type': None, 'heating_type': None, 'parking_type': None, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['furniture', 'porch', 'telephone', 'conditioner']}
#publish(scraped, "gelashavarkakasha")

def publish_com_area(scraped,description, driver, to_ssge):
    try:
        with open("config.json", "r", encoding="utf-8") as cfg:
            encoded_config = json.load(cfg)["encoded_data"]
            decoded_config = json.loads(base64.b64decode(encoded_config).decode("utf-8"))

            mhemail = decoded_config["credentials"]["myhome"]["email"]
            mhpassword = decoded_config["credentials"]["myhome"]["password"]
            # ssemail = decoded_config["credentials"]["ss.ge"]["email"]
            # sspassword = decoded_config["credentials"]["ss.ge"]["password"]
            contact_name = decoded_config["contact"]["name"]
            contact_number = decoded_config["contact"]["number"]


        open_site('https://statements.tnet.ge/ka/statement/create?referrer=myhome', driver)

        wait_until_cs("button.luk-px-5", 10, driver).click()
        wait_until_id(10, driver, "Email").send_keys(mhemail)
        wait_until_id(10, driver, "Password").send_keys(mhpassword)
        wait_until_cs("button.gradient-button", 10, driver).click()

        wait_until_clickable_xpath('//*[@id="0"]/div[2]/div/div/div/div[5]/label', 30, driver).click() # tipi

        wait_until_xpath(10, driver, '//*[@id="0"]/div[3]/div/div/div/div[1]/label').click()
        wait_until_cs( "div.luk-flex.luk-justify-start.luk-items-end.luk-relative.luk-cursor-text.luk-overflow-hidden.luk-border.luk-rounded-lg.luk-w-full.luk-h-12",10, driver).click()

        match scraped["qalaqi"]:
            case "თბილისი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[1]'))
            case "ბათუმი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[2]'))
            case "ბაკურიანი":
                driver.execute_script("arguments[0].click();",
                                      wait_until_xpath(30, driver, '//*[@id="0"]/div[4]/div/div/div/div[2]/ul/li[8]'))

        field = wait_until_xpath(10, driver, "//label[@for=':ri:']/input")
        misamarti = scraped["misamarti"]
        try:
            field.send_keys(misamarti)
            listo = wait_until_cs( 'ul.list-none',5, driver)
            first_result = wait_until_cs( "li.cursor-pointer",5, listo)
            driver.execute_script("arguments[0].click();", first_result)
        except:
            field.clear()
            field.send_keys(re.sub(r"[-#,0-9]", "", misamarti))
            listo = wait_until_cs('ul.list-none', 10, driver)
            first_result = wait_until_cs("li.cursor-pointer", 10, listo)
            driver.execute_script("arguments[0].click();", first_result)

        label_element = wait_until_xpath(30, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
        driver.execute_script("arguments[0].click();", label_element)

        if scraped["sadzinebeli"] != None and scraped["sadzinebeli"] > 0:
            element = wait_until_clickable_xpath(time=10, driver=driver, xpath='//*[@id="1"]/div[2]/div/div[4]/div/div')
            elements = element.find_elements(By.TAG_NAME, "span")
            for i in elements:
                if i.text == str(scraped["sadzinebeli"]):
                    driver.execute_script("arguments[0].click();", i)
                    break

        if scraped["bathroom_type_id"] != "null":
            list_of_bti = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[6]/div/div/div')
            driver.execute_script("arguments[0].click();", list_of_bti)
            if scraped["bathroom_type_id"] == "1":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                '//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[1]'))
            elif scraped["bathroom_type_id"] == "2":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                '//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[2]'))
            elif scraped["bathroom_type_id"] == "3":
                driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                '//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[3]'))
            else:
                driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                '//*[@id="1"]/div[2]/div/div[6]/div/div/div[2]/ul/li[4]'))


        wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[1]/div/label').send_keys(scraped["sartuli"])
        wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[8]/div[2]/div/label').send_keys(scraped["sartuli-sul"])
        ###-----#_#_#__##__##__#
        # el = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[10]/div/div/div')
        # driver.execute_script("arguments[0].click();", el)
        #_#_#__#_#_#_#_#_#_

        #-- kom partis tipis archeva
        click('//*[@id="1"]/div[2]/div/div[10]/div/div/div', driver, 10)
        match True:
            case _ if "სპეციალური" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[1]', driver)
            case _ if "საოფისე" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[2]', driver)
            case _ if "სავაჭრო" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[3]', driver)
            case _ if "სასაწყობე" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[4]', driver)
            case _ if "საწარმოო" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[5]', driver)
            case _ if "კვების ობიექტი" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[6]', driver)
            case _ if "ავტოფარეხი" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[7]', driver)
            case _ if "სარდაფი" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[8]', driver)
            case _ if "ნახევარსარდაფი" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[9]', driver)
            case _ if "მთლიანი შენობა" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[10]', driver)
            case _ if "ავტოსამრეცხაო" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[11]', driver)
            case _ if "ავტოსერვისი" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[12]', driver)
            case _ if "უნივერსალური" in scraped["saxeli"]:
                click('//*[@id="1"]/div[2]/div/div[10]/div/div/div[2]/ul/li[13]', driver)

        #ashenebis weli
        click('//*[@id="1"]/div[2]/div/div[12]/div/div/div[1]', driver)
        click('//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[3]', driver)

        #mdgomareoba
        click('//*[@id="1"]/div[2]/div/div[14]/div/div/div', driver)
        click('//*[@id="1"]/div[2]/div/div[14]/div/div/div[2]/ul/li[1]', driver)


        tipi_dropdown = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div')
        driver.execute_script("arguments[0].click();", tipi_dropdown)
        arastandartuli = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[16]/div/div/div[2]/ul/li[1]')
        driver.execute_script("arguments[0].click();", arastandartuli)

        byxpath('//*[@id="1"]/div[2]/div/div[18]/div/div/label',driver).send_keys(30) # cheris simaghle

        driver.execute_script("arguments[0].click();",
                              wait_until_clickable_xpath('//*[@id="2"]/div[3]/div[3]/div[2]/div[2]/div[2]', 20, driver))
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[2]/div/div[1]/div/label').send_keys(scraped["parti"])
        wait_until_xpath(10, driver, '//*[@id="2"]/div[3]/div[3]/div[1]/div/label').send_keys(scraped["fasi"])

        #contact information

        wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[2]/div/div/label').send_keys(contact_name)
        wait_until_xpath(10, driver, '//*[@id="3"]/div[2]/div/div[5]/div/div/label').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE ,Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, contact_number)
        #description geo,eng,rus
        wait_until_xpath(10, driver, '//*[@id="4"]/div[2]/div[2]/div/textarea').send_keys(description)

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
        # Folder containing your photos
        photo_folder = f'images/{scraped["id"]}/'
        photo_files = []

        # Collect all .png file paths
        for f in os.listdir(photo_folder):
            if f.endswith(".jpg"):
                photo_files.append(os.path.abspath(os.path.join(photo_folder, f)))

        # Combine file paths into a single string separated by newlines
        file_paths = "\n".join(photo_files)

        # Wait for the actual input element with type="file" to appear
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )

        # Send the file paths directly to the input element
        file_input.send_keys(file_paths)


        # ashenebis weli
        # if scraped["build_year"] != None:
        #     driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[12]/div/div/div'))
        #
        #     match scraped["build_year"]:
        #         case ">2000":
        #             driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
        #                                                                             '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[3]'))
        #         case "1995-2000":
        #             driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
        #                                                                             '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[2]'))
        #         case "<1995":
        #             driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
        #                                                                             '//*[@id="1"]/div[2]/div/div[12]/div/div/div[2]/ul/li[1]'))

        # ashenebis weli

        # parkingis tipi
        if scraped["parking_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[22]/div/div/div'))
            match scraped["parking_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[22]/div/div/div[2]/ul/li[6]'))
        # parkingis tipi

        #-------- gatbobis tipi
        if scraped["heating_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div'))
            match scraped["heating_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[20]/div/div/div[2]/ul/li[7]'))
                case _:
                    pass
        # -------- gatbobis tipi

        # -------- cxeli wyalis tipi
        if scraped["hot_water_type"] != None:
            driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[24]/div/div/div'))

            match scraped["hot_water_type"]:
                case 1:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10,driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[1]'))
                case 2:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[2]'))
                case 3:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[3]'))
                case 4:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[4]'))
                case 5:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[5]'))
                case 6:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[6]'))
                case 7:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[7]'))
                case 8:
                    driver.execute_script("arguments[0].click();", wait_until_xpath(10, driver,
                                                                                    '//*[@id="1"]/div[2]/div/div[24]/div/div/div[2]/ul/li[8]'))

        # -------- cxeli wylis tipi

        into_view_xpath('//*[@id="1"]/div[2]/div/div[28]/div[1]/div/label', driver)

        #aivnebi tu dafiqsirda chaweros
        if scraped["balconies"] != None:
            wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[1]/div/label').send_keys(scraped["balconies"])
            if scraped["balcony_area"] == None or scraped["balcony_area"] == "None":
                wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys("1")
            else:
                wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys(
                    scraped["balcony_area"])
        # aivnani

    # ----------- PARAMETREBIS GILAKEBIS MDEBAREOBEBI
        int_button = wait_until_clickable_xpath('//*[@id="1"]/div[4]/div/div/div/div[1]', 20, driver)
        televizia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[2]')
        bunebrivi_airi = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[3]')
        lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[4]')
        satvirto_lifti = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[5]')
        wyali = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[6]')
        kanalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[7]')
        eleqtroenergia = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[8]')
        telefoni = wait_until_xpath(10, driver, '//*[@id="1"]/div[4]/div/div/div/div[9]')
        #upiratesobebi

        spa = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[1]')
        sport_darbazi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[2]')
        buxari = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[3]')
        jakuzi = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[4]')
        sauna = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[5]')
        signalizacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[6]')
        vintilacia = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[7]')
        dacva = wait_until_xpath(10, driver, '//*[@id="1"]/div[5]/div/div/div/div[8]')

        #aveji da teqnika
        aveji = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[1]')
        qura = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[2]')
        gumeli = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[3]')
        kondicioneri = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[4]')
        macivari = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[5]')
        sarecxi_manqana = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[6]')
        churchlis_sarecxi = wait_until_xpath(10, driver, '//*[@id="1"]/div[6]/div/div/div/div[7]')
        # bejebi
        kari_kodit = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[1]')
        sainvesticio = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[2]')
        ssmp = wait_until_xpath(10, driver, '//*[@id="1"]/div[7]/div/div/div/div[3]')



        # zeda gilakebi
        loggia = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[5]/span/div/label', 10, driver)
        veranda = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[7]/span/div/label', 10, driver)
        satavsos_tipi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[11]/span/div/label', 10, driver)
        sacurao_auzi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[1]/span/div/label', 10, driver)
        misaghebi = wait_until_clickable_xpath('//*[@id="1"]/div[3]/div/div[3]/span/div/label', 10, driver)

        yard = byxpath('//*[@id="1"]/div[3]/div/div[13]/span/div/label', driver)


    # ----------- PARAMETREBI

        time.sleep(1)
        for parameter in scraped["additions"]:
            match parameter:
                case "internet":
                    driver.execute_script("arguments[0].click();", int_button)
                case "conditioner":
                    driver.execute_script("arguments[0].click();", kondicioneri)
                case "gas":
                    driver.execute_script("arguments[0].click();", bunebrivi_airi)
                case "tv":
                    driver.execute_script("arguments[0].click();", televizia)
                case "furniture":
                    driver.execute_script("arguments[0].click();", aveji)
                case "elevator":
                    driver.execute_script("arguments[0].click();", lifti)
                case "truck_elevator":
                    driver.execute_script("arguments[0].click();", satvirto_lifti)
                case "stove":
                    driver.execute_script("arguments[0].click();", qura)
                case "oven":
                    driver.execute_script("arguments[0].click();", gumeli)
                case "water":
                    driver.execute_script("arguments[0].click();", wyali)
                case "sewerage":
                    driver.execute_script("arguments[0].click();", kanalizacia)
                case "electricity":
                    driver.execute_script("arguments[0].click();", eleqtroenergia)
                case "telephone":
                    driver.execute_script("arguments[0].click();", telefoni)
                case "refrigerator":
                    driver.execute_script("arguments[0].click();", macivari)
                case "washing_machine":
                    driver.execute_script("arguments[0].click();", sarecxi_manqana)
                case "investment":
                    driver.execute_script("arguments[0].click();", sainvesticio)
                case "alarm":
                    driver.execute_script("arguments[0].click();", signalizacia)
                case "guard":
                    driver.execute_script("arguments[0].click();", dacva)
                case "ventilation":
                    driver.execute_script("arguments[0].click();", vintilacia)
                case "coded-door":
                    driver.execute_script("arguments[0].click();", kari_kodit)
                case "gym":
                    driver.execute_script("arguments[0].click();", sport_darbazi)
                case "spa":
                    driver.execute_script("arguments[0].click();", spa)
                case "jacuzzi":
                    driver.execute_script("arguments[0].click();", jakuzi)
                case "sauna":
                    driver.execute_script("arguments[0].click();", sauna)
                case "dishwasher":
                    driver.execute_script("arguments[0].click();", churchlis_sarecxi)
                case "storeroom":
                    driver.execute_script("arguments[0].scrollIntoView();", satavsos_tipi)
                    driver.execute_script("arguments[0].click();", satavsos_tipi)
                    if scraped["store_room_area"] != None:
                        sacavis_parti_entry = wait_until_xpath(xpath='//*[@id="1"]/div[3]/div/div[14]/div[1]/div/label',
                                                               driver=driver, time=10)
                        sacavis_parti_entry.send_keys(scraped["store_room_area"])
                case "loggia":
                    driver.execute_script("arguments[0].click();", loggia)
                    if scraped["loggia_area"] != None:
                        wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[6]/div/div/label').send_keys(scraped["loggia_area"])

                case "swimming_pool":
                    driver.execute_script("arguments[0].click();", sacurao_auzi)
                case "porch":
                    driver.execute_script("arguments[0].click();", veranda)
                    if scraped["porch_area"] != None:
                        porch_area = wait_until_xpath(10, driver, '//*[@id="1"]/div[3]/div/div[8]/div/div/label')
                        porch_area.send_keys(scraped["porch_area"])
                case "with_a_yard":
                    driver.execute_script("arguments[0].click();", yard)
                    if scraped["yard_area"] != None or scraped["yard_area"] != "None":
                        byxpath('//*[@id="1"]/div[3]/div/div[12]/div/div/label', driver).send_keys(scraped["yard_area"])


        # #upload and payment
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"


        payment_part(driver)
        if driver.find_element(By.TAG_NAME, "circle"):
            ID = find_id_myhome(driver)
            info_for_database = {
                "MYHOME-ID": ID,
                "MYHOME-LINK": f"https://myhome.ge/pr/{ID}",
                "OWNER NAME": scraped["owner-name"],
                "OWNER NUMBER": scraped["owner-number"],
                "PARTI": scraped["parti"],
                "OTAXI": scraped["otax-raodenoba"],
                "BEDROOMS": scraped["sadzinebeli"],
                "CONDITION": scraped["status"],
                "PRICE": scraped["fasi"],
                "ADDRESS": scraped["misamarti"],
                "REGION": scraped["district_name"],
                "AGENTISSAXELI": scraped["agenti"],
                "TARIGI": current_time,
            }
            if to_ssge:
                try:
                    publish_ss_com(scraped, description, driver, info_for_database)
                except:
                    info_for_database["SS_LINK"] = "Error SS.GE-ze"
                    to_database(info_for_database)
                    driver.quit()
            else:
                info_for_database["SS_LINK"] = "No SS.GE"
                to_database(info_for_database)
                driver.quit()




    except Exception as e:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        data = f"{current_time} <||> {scraped['id']}"
        with open("logs/errors-log.txt", "a", encoding="utf-8") as log:
            log.write(f"{data}\n")
        submit_error(scraped["id"], current_time)
        time.sleep(2)

# scraped = {'tipi': 'იყიდება', 'saxeli': 'იყიდება უნივერსალური კომერციული ფართი დიდუბეში', 'qalaqi': 'თბილისი', 'id': '20178921', 'misamarti': 'კედიას ქუჩა 14ა', 'fasi': '78125', 'parti': '62.5', 'otax-raodenoba': 1, 'sadzinebeli': None, 'sartuli': 1, 'sartuli-sul': 10, 'status': '', 'build_year': '>2000', 'condition': '1', 'bathroom_type_id': '1', 'balconies': 'None', 'balcony_area': 'None', 'hot_water_type': None, 'heating_type': None, 'parking_type': None, 'porch_area': None, 'loggia_area': None, 'store_room_area': None, 'additions': ['water', 'sewerage', 'electricity'], 'yard_area': None, 'district_name': 'დიდუბე-ჩუღურეთი', 'owner-number': '577 552 405', 'owner-name': 'ოთარ', 'agenti': 'SafeHome'}
# publish_com_area(scraped, "gela", driver=cdriver())