import os
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.webdriver.chrome.webdriver import WebDriver

from auth_manager.auth_manager import auth_with_login_and_pass


def get_chrome_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    chrome_driver_binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver: WebDriver = None

    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if chrome_driver_binary_location == None:  # running in test env
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
    else:  # running in server env
        options.binary_location = chrome_driver_binary_location

        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=options)

    return driver


def send_message_to_account(login, bot_msg):
    # chrome_options = Options()
    # # Add for opening screen
    # # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('log-level=2')
    # driver = webdriver.Chrome(ChromeDriverManager().install(), 0, chrome_options)

    driver = get_chrome_driver()

    auth_with_login_and_pass(driver)

    driver.get(f"https://www.instagram.com/{login}")

    sleep(5)

    try:
        follow_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button")
        if follow_button and follow_button.text == 'Подписаться':
            follow_button.click()
    except:
        print('Follow exception')

    sleep(5)

    message_open_button = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button")
    message_open_button.click()

    sleep(5)

    try:
        close_modal_button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]")
        if close_modal_button:
            close_modal_button.click()
    except:
        print('Close banner exception')

    text_field = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
    text_field.send_keys(bot_msg)

    send_msg_button = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button")
    send_msg_button.click()
