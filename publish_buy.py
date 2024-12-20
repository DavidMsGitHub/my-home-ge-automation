from for_driver import *
from pay_and_upload import payment_part
import os
from datetime import datetime
import time


def publish(link,scraped,description=""):
    try:
        # get credentials
        with open("config.json", "r", encoding="utf-8") as cfg:
            json_string = json.load(cfg)
            mhemail = json_string["credentials"]["email"]
            mhpassword = json_string["credentials"]["password"]
            contact_name = json_string["contact"]["name"]
            contact_number = json_string["contact"]["number"]

        driver = cdriver()

        driver.get("https://statements.tnet.ge/ka/statement/create?referrer=myhome")

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

        wait_until_xpath(10, driver, "//label[@for=':ri:']/input").send_keys(scraped["misamarti"])
        listo = wait_until_cs( 'ul.list-none',10, driver)
        first_result = wait_until_cs( "li.cursor-pointer",10, listo)
        driver.execute_script("arguments[0].click();", first_result)

        label_element = wait_until_xpath(30, driver, f"//label[.//span[text()='{scraped['otax-raodenoba']}']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
        driver.execute_script("arguments[0].click();", label_element)

        if scraped["sadzinebeli"] > 0:
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
            if f.endswith(".png"):
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
            wait_until_xpath(10,driver,'//*[@id="1"]/div[2]/div/div[28]/div[2]/div/label').send_keys(scraped["balcony_area"])
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
                        sacavis_parti_entry = wait_until_xpath(xpath='//*[@id="1"]/div[2]/div/div[38]/div[1]/div/label',
                                                               driver=driver, time=10)
                        sacavis_parti_entry.send_keys(scraped["store_room_area"])

                case "loggia":
                    driver.execute_script("arguments[0].click();", loggia)
                    loggia = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[34]/div/div/label')
                    loggia.send_keys(scraped["loggia_area"])
                case "swimming_pool":
                    driver.execute_script("arguments[0].click();", sacurao_auzi)
                case "porch":
                    driver.execute_script("arguments[0].click();", veranda)
                    if scraped["porch_area"] != None:
                        porch_area = wait_until_xpath(10, driver, '//*[@id="1"]/div[2]/div/div[36]/div/div/label')
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


        if payment_part(driver):
            driver.quit()
    except:
        now = datetime.now()
        current_time = f"[{now.strftime('%b %d')} {now.hour}:{now.strftime('%M')}]"
        with open("logs/errors-log.txt", "a") as log:
            log.write(f"{current_time} <||> {scraped["id"]}\n")

