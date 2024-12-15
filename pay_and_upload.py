from for_driver import *
import time
def payment_part(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    container = wait_until_cs( "div.fixed.bottom-0.left-0.right-0.z-20.flex",10, driver)
    buttons = container.find_elements(By.TAG_NAME, "button")
    upload_button = buttons[1]
    try:
        upload_button.click()
    except:
        driver.execute_script("arguments[0].click();", upload_button)

    payment_choice = wait_until_clickable_xpath(
        '//*[@id="root"]/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", payment_choice)
    time.sleep(5)
    balance_choice = wait_until_clickable_xpath(
        '//*[@id="root"]/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/label', 30, driver)
    driver.execute_script("arguments[0].click();", balance_choice)
    pay_button = wait_until_clickable_xpath('//*[@id="root"]/div[2]/div/div[1]/div[2]/div/div/div/div[3]/button', 30,
                                            driver)
    driver.execute_script("arguments[0].click();", pay_button)
    success = wait_until_xpath(300, driver, "//h1[contains(text(), 'გადახდა წარმატებით განხორციელდა')]")

    if success:
        return True
    else:
        return False