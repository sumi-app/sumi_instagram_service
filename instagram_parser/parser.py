import json
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from auth_manager.auth_manager import auth_with_login_and_pass


def parse_accounts(tag):
    url = f"https://www.instagram.com/explore/tags/{tag}/"
    chrome_options = Options()
    # Add for opening screen
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=2')
    driver = webdriver.Chrome(ChromeDriverManager().install(), 0, chrome_options)

    auth_with_login_and_pass(driver)
    sleep(10)
    driver.get(url)

    # scroll(driver)
    sleep(10)
    favorite_posts_row = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div")
    favorites_posts = favorite_posts_row.find_elements_by_class_name("kIKUG")

    links = []

    for favorite_post in favorites_posts:
        l = str(favorite_post.find_element_by_xpath('a').get_attribute('href'))
        links.append(l)

    for link in links:
        driver.get(f"{link}")
        sleep(6)
        driver.find_element_by_class_name("e1e1d").click()
        sleep(6)
        followers_count = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute('title')
        nik = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/h2").text
        description = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/span").text
        name = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/h1").text

        print(followers_count, nik, description, name)

        count_replaced = followers_count.replace(' ', '')
        # type(count_replaced)
        # print(count_replaced)
        json_data = json.dumps({
            "name": str(name),
            "login": str(nik),
            "description": str(description),
            "count": int(count_replaced),
            "social_network": 3,
        }, ensure_ascii=False)
        json_data.encode('unicode_escape')
        print(json_data)
        headers = {'Content-Type': 'text/text; charset=utf-8'}
        r = requests.post("http://localhost:8080/api/blogger", data=json_data.encode("utf-8"), headers=headers)
        print(r.status_code, r.reason)


# def scroll(driver):
#     end_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[3]/div[3]")
#     driver.execute_script("arguments[0].scrollIntoView(true);", end_post)
#     for i in range(20):
#         try:
#             end_post = driver.find_element_by_xpath(f"/html/body/div[1]/section/main/article/div[2]/div/div[{i + 1}]")
#             driver.execute_script("arguments[0].scrollIntoView(true);", end_post)
#             print('Move down')
#         except:
#             print('Scroll exception')


if __name__ == '__main__':
    load_dotenv()
    parse_accounts('самара')

# def parse_account_data(login):

# api_url = f"https://www.instagram.com/{login}/?__a=1"
# r = requests.get(api_url)
# result = r.content
# print(result)
# return result
