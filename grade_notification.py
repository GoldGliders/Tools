#!/usr/bin/python3.8
# coding: utf-8
import csv
import logging
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from tweet import tweet


def open_with_chromedriver(url):
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        executable_path=os.getenv("CHROMEDRIVER"),
        options=options
    )
    driver.get(url)

    return driver


def login(driver, username, passwd):
    username_form = driver.find_element_by_xpath(
        '//*[@id="LoginFormSimple"]/tbody/tr[1]/td[2]/input'
    )
    passwd_form = driver.find_element_by_xpath(
        '//*[@id="LoginFormSimple"]/tbody/tr[2]/td[2]/input'
    )
    login_btn = driver.find_element_by_xpath(
        '//*[@id="LoginFormSimple"]/tbody/tr[3]/td/button[1]/span'
    )

    username_form.send_keys(username)
    passwd_form.send_keys(passwd)
    login_btn.click()


def get_grade_html(driver, url):
    driver.get(url)
    time.sleep(3)

    iframe = driver.find_element_by_xpath('//*[@id="main-frame-if"]')
    driver.switch_to.frame(iframe)
    display_on_screen_btn = driver.find_element_by_xpath(
        '//*[@id="rishuSeisekiReferListForm"]/table/tfoot/tr/td/input[1]'
    )
    display_on_screen_btn.click()
    grade_table_html = driver.page_source

    return grade_table_html


def multiple_replace(text, replacers):
    for rplcr in replacers:
        text = text.replace(*rplcr)
    return text


def make_grade_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = list()
    trs = soup.find_all("tr")
    for tr in trs[9:]:
        record = list()
        for td in tr.find_all("td"):
            text = multiple_replace(
                     td.text,
                     [("\n", ""), ("\t", ""), (" ", ""), ("\u3000", "")]
                   )
            record.append(text)
        table.append(record)
    return table


def get_old_grade(csv_name):
    with open(csv_name, "r") as csvfile:
        reader = csv.reader(csvfile)
        table = list(reader)

    return table


def comapre_grade_table(old_table, new_table):
    diff = list()
    for old, new in zip(old_table, new_table):
        if old != new:
            diff.append(new)

    return diff


def update_grade_csv(csv_name, grade_table):
    with open(csv_name, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(grade_table)


def post(diff):
    SUFFIX = "の成績出た！"
    for subject in diff:
        subject_name = subject[4]
        tweet(subject_name + SUFFIX)


if __name__ == "__main__":
    BASE_URL = "https://csweb.u-aizu.ac.jp/campusweb/campusportal.do?"
    LOGIN_URL = BASE_URL + "locale=ja_JP"
    GRADE_EXAM_URL = BASE_URL + "page=main&tabId=si"

    USERNAME = os.getenv("UoA_ID")
    PASSWORD = os.getenv("UoA_PASSWD")

    DIRECTORY = os.getenv("GRADE_NOTIFICATION_PATH")
    CSV_NAME = DIRECTORY + "UoA_grade.csv"
    LOGFILE = DIRECTORY + "grade_notification.log"

    formatter = "%(asctime)s  %(levelname)s \
                 %(name)s  %(funcName)s  %(lineno)d : %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter, filename=LOGFILE)

    try:
        logging.info("Start crawling...")
        driver = open_with_chromedriver(LOGIN_URL)
        login(driver, USERNAME, PASSWORD)
        time.sleep(3)

        html = get_grade_html(driver, GRADE_EXAM_URL)
        new_table = make_grade_table(html)
        old_table = get_old_grade(CSV_NAME)
        diff = comapre_grade_table(old_table, new_table)
        logging.info(diff)

        if diff is None or len(diff) == 0:
            logging.info("There is no update.")
        else:
            logging.info(f"There is {len(diff)} update.")
            update_grade_csv(CSV_NAME, new_table)
            post(diff)

    except NoSuchElementException as e:
        logging.warning(e)

    except Exception as e:
        logging.critical(e)

    finally:
        driver.close()
