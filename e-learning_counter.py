import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def open_with_chromedriver(url):
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=os.getenv("CHROMEDRIVER"),
        options=options
    )
    driver.get(url)
    return driver


def login(driver):
    email_form = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/form/input[3]"
    )
    passwd_form = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/form/input[4]"
    )
    login_btn = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/form/input[5]"
    )

    email_form.send_keys(os.getenv("UoA_ID"))
    passwd_form.send_keys(os.getenv("REALLY_ENGLISH_PASSWD"))
    login_btn.click()


def go2report(driver, url):
    driver.get(url)


def get_html(driver):
    html = driver.page_source
    return html


def analyze_html(html, level):
    counter = {"listen": 0, "read": 0, "grammer": 0}
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all("tr")

    for tr in trs:
        nums = tr.find_all(class_="num")
        tds = tr.find_all("td")
        text = tr.text
        if len(nums) != 0 and nums[0].text == str(level):
            if tds[-1].text == "はい":
                if "リスニング" in text:
                    counter["listen"] += 1
                if "リーディング" in text:
                    counter["read"] += 1
                if "文法" in text:
                    counter["grammer"] += 1
    return counter


if __name__ == "__main__":
    URL = "https://u-aizu.reallyenglish.jp/login?locale=ja"
    REPORT_URL = "https://u-aizu.reallyenglish.jp/user_courses/284774/report"
    LEVEL = 4

    driver = open_with_chromedriver(URL)
    try:
        time.sleep(1)
        login(driver)
        time.sleep(1)
        go2report(driver, REPORT_URL)
        time.sleep(1)
        html = get_html(driver)
        counter = analyze_html(html, LEVEL)
        print(
            f"Level: {LEVEL}",
            counter,
            f"Total: {sum(counter.values())}"
        )
    except NoSuchElementException:
        pass
    finally:
        driver.close()
