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
    browser.add_cookie({"name": "MUSIC_U", "value": "0024E8D70C19D56E8C0B076E1B05860FD4152DB6D4EC849EDD5C3BB95102607092E5FD1F9DB41239B2389CBD1F41E1C77D2468881BE8C892D22924DFFF91A07CB89C0A02C5AEA07F2A2D044BC1B780E40DFD34656022A773965A69783221F373157EEB34BA1F7EA2F6117A828E6775095A7FA2A50DC38DFBBE9DF5166D47DF826911F5E9741D4309CDD41542239028E233235436E4D88DE6326A44C443B8F3B5314154DF23A1E64852B3AC2FD508E143BAB5EC6BF1585560D3211777C842102DE5D3040A363B06B2C9D0FCF5AAB4266931AA9460877EF0168FA3B1A53C5CBADDC196B9B6FD8CAA8F8F9B74259034E0C05AD5A20C6F93BA3EC2E1A8A63378CA78BC56B3597948B5DA84D83DF039C697085E681BDFF73E3D72132D41DE76C829E85BB21BD0CA86FAD28A810525EE0ED91A438FAF492254BBD3D64A53616362D1379C10BECC95D90733133651067301A45C3A77903CA15DAEC53B41572C25B319D1B2D4F31530B2CFA8098EB45634C549AC0DBCF054D8BB818CDFA58B8434BF465EB933C7F6809AC92E04040F9E87EC1D3133"})
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
