import os
import sys
import urllib
import pydub
import speech_recognition as sr
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
from datetime import datetime
import requests
import json
import stem.process
from stem import Signal
from stem.control import Controller

# custom patch libraries


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)


def create_tor_proxy(socks_port, control_port):
    TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
    try:
        tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(socks_port),
                'ControlPort': str(control_port),
                'MaxCircuitDirtiness': '300',
            },
            init_msg_handler=lambda line: print(line) if re.search(
                'Bootstrapped', line) else False,
            tor_cmd=TOR_PATH
        )
        print("[INFO] Tor connection created.")
    except:
        tor_process = None
        print("[INFO] Using existing tor connection.")

    return tor_process


def renew_ip(control_port):
    print("[INFO] Renewing TOR ip address.")
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        controller.close()
    print("[INFO] IP address has been renewed! Better luck next try~")


if __name__ == "__main__":
    SOCKS_PORT = 41293
    CONTROL_PORT = 41294
    USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
                       ]
    activate_tor = False
    tor_process = None
    user_agent = random.choice(USER_AGENT_LIST)
    if activate_tor:
        print('[INFO] TOR has been activated. Using this option will change your IP address every 60 secs.')
        print('[INFO] Depending on your luck you might still see: Your Computer or Network May Be Sending Automated Queries.')
        tor_process = create_tor_proxy(SOCKS_PORT, CONTROL_PORT)
        PROXIES = {
            "http": f"socks5://127.0.0.1:{SOCKS_PORT}",
            "https": f"socks5://127.0.0.1:{SOCKS_PORT}"
        }
        response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
    else:
        response = requests.get("http://ip-api.com/json/")
    result = json.loads(response.content)
    print('[INFO] IP Address [%s]: %s %s' % (datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"), result["query"], result["country"]))

    # download latest chromedriver, please ensure that your chrome is up to date
    driver = webdriver.Chrome()
    driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query")

    # main program
    # auto locate recaptcha frames
    try:
        delay()
        frames = driver.find_elements_by_tag_name("iframe")
        recaptcha_control_frame = None
        recaptcha_challenge_frame = None
        for index, frame in enumerate(frames):
            if re.search('reCAPTCHA', frame.get_attribute("title")):
                recaptcha_control_frame = frame

            if re.search('reCAPTCHA 驗證問題將在兩分鐘後失效', frame.get_attribute("title")):
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

    except:
        # if ip is blocked.. renew tor ip
        print("[INFO] IP address has been blocked for recaptcha.")
        if activate_tor:
            renew_ip(CONTROL_PORT)
        sys.exit()
