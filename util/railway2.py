from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
import time, json, requests, asyncio
from tabulate import tabulate
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import service_Client as sttApi

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response
def get_media_url() :
    browser_log = driver.get_log('performance') 
    events = [process_browser_log_entry(entry) for entry in browser_log]
    result = list()
    for event in events:
        if 'Network.response' not in event['method']: continue
        if 'type' not in event['params']: continue
        if 'Media' != event['params']['type']: continue
        result.append(event['params']['response']['url'])
    return result[-1]

driver = webdriver.Chrome()
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip119/queryTime")

html = driver.find_element_by_css_selector("*").get_attribute("outerHTML")
doc = pq(html)

# 取得出發縣市
cities_startStation = {}
citiesSort_startStation = {}

# 出發站
stationSort_startStation = {}

# 取得抵達縣市
cities_endStation = {}
citiesSort_endStation = {}

# 抵達站
stationSort_endStation = {}

# 查詢結果班次
result_trans = []

# 原始頁碼
last_url = ''


def solve_recaptcha2():
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='switchToVoice']").click()
    time.sleep(3)
    _item = driver.find_element_by_xpath("//*[@id='playMusic']")
    driver.execute_script("arguments[0].click();", _item)
    time.sleep(3)
    url = get_media_url()
    print(url)

    _item = driver.find_element_by_xpath("//*[@id='voiceDiv']/div[1]/label")
    script = f"arguments[0].innerHTML=\"<a id='mydownload' href='{url}' download=''>DOWN</a>\"";
    driver.execute_script(script, _item)
    _item = driver.find_element_by_xpath("//*[@id='mydownload']")
    driver.execute_script("arguments[0].click();", _item)

    sttApi.stt('audio.mp3')

    # my_files = {'src': 'W', 'mod': 'MTK_new', 'file': open('audio.mp3', 'rb')}
    # r = requests.post('https://www.taiwanspeech.ilovetogether.com/tws-cgi/post_server.py', files = my_files)
    # print(r)
    
    # 
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(3)
    # video = driver.find_element(By.XPATH, '/html/body/video/source')
    # video_url = video.get_property('src')
    # urllib.request.urlretrieve(video_url, 'videoname.mpeg')

solve_recaptcha2()
