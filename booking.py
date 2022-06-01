from multiprocessing import Condition
import requests
import time
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from tabulate import tabulate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
import sys
import re

driver = webdriver.Chrome()
driver.get("https://www.google.com/recaptcha/api2/demo")


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)

# html = driver.find_element_by_css_selector("*").get_attribute("outerHTML")
# doc = pq(html)

# input_ticket_num = input("輸入車票數量：")
# input_ticket_num_int = int(input_ticket_num)

# # 選擇票數
# driver.execute_script(
#     "document.getElementById('normalQty').value='{0}'".format(input_ticket_num_int))

# if input_ticket_num_int > 1:
#     for x in range(input_ticket_num_int):
#         driver.find_element_by_xpath(
#             "//*[@id='queryForm']/div[1]/div[2]/div[1]/div[2]/button[2]").click()


# 驗證碼
try:
    delay()
    frames = driver.find_elements_by_tag_name("iframe")
     recaptcha_control_frame = None
      recaptcha_challenge_frame = None
       for index, frame in enumerate(frames):
            if re.search('reCAPTCHA', frame.get_attribute("title")):
                recaptcha_control_frame = frame

            if re.search('recaptcha challenge', frame.get_attribute("title")):
                recaptcha_challenge_frame = frame
        if not (recaptcha_control_frame and recaptcha_challenge_frame):
            print("[ERR] Unable to find recaptcha. Abort solver.")
            sys.exit()
        # switch to recaptcha frame
        delay()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_control_frame)
        # click on checkbox to activate recaptcha
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()

        # switch to recaptcha audio control frame
        delay()
        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_challenge_frame)

# data-sitekey = "6LdHYnAcAAAAAI26IgbIFgC-gJr-zKcQqP1ineoz"
