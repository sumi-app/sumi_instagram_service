from time import sleep
import os


def auth_with_login_and_pass(driver):
    driver.get("https://www.instagram.com/")
    sleep(2)
    login_field = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
    login_field.send_keys(os.getenv('INSTA_LOGIN'))
    pwd_field = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
    pwd_field.send_keys(os.getenv('INSTA_PASS'))
    driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button").click()
    sleep(3)
