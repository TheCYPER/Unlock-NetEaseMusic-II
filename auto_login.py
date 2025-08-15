# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BE02A6F72F982CC060B0C004E8F267B7E0549DF18CFDC63C36F6D89E127876C98D82E828033BC4BADBC6879EE3ADC550BDCB21FB5F6672C7EE99FBB84BECBB9AA535D463743BEC1E5CB048160FE1CB96253F55F46B1C64460B05C8978BA711FBD57D439F0DB7D4AE0447628AB4C3128A43A9BF639282F08B9B71ACF21A934E351B7A98C32C6D72813D18CE35F0361210C640D220EA9C76E3C61D80EF3FAA75833D4EE84ADC920F88B951016EEDE46D110405C91B758171242809B5D944D8354AB18287A868628C755817836387A1D986ECB5226D3591D7008A8DFA2900BEF077B3CD4B329C9BF2115CC4BE44A432033BFCDE1B8E4EC79A52387C7CFEB7D50891B63507363620F9F04AA94D8BD57F88F69C74D06BF548DA2033826342C40F84D7A9588992B8E42AA30A94F8A03890987E05D9CAC4442160AEB31F5D5C2195DD798B11AC8AC0C1BA28DA2E2C50E2D914363BC7F22881AF1DB2FD884C72E1343141C615D38CB1C8171360009322CF9FD454F1F4BF054103FC268A36DC733A02D0911CC4276511BCA03ACB4F83A923E59914"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
