from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
import time
from tabulate import tabulate
from train import train

from torch import rand_like
import os
from functools import cmp_to_key
import re

# ==================================================================================================================== #
# 出發站一系列動作
dir = os.path.dirname(os.path.realpath(__file__))

class Railway(object):
    def __init__(self, input_startStationCity='臺南市', input_startStation='臺南',
                 input_endStationCity='屏東縣', input_endStation='屏東',
                 input_date='2022/06/10', input_startTime='10:00', input_endTime='22:00'):
        self.count = 0
        self.stationCount = 0
        self.count2 = 0
        print(os.path.join(dir, "chromedriver.exe"))
        self.driver = webdriver.Chrome(os.path.join(dir, "chromedriver.exe"))
        self.url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"
        self.driver.get(
            "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")

        self.html = self.driver.find_element_by_css_selector(
            "*").get_attribute("outerHTML")
        self.doc = pq(self.html)

        # 取得出發縣市
        self.cities_startStation = {}
        self.citiesSort_startStation = {}
        self.input_startStationCity = input_startStationCity

        # 出發站
        self.stationSort_startStation = {}
        self.input_startStation = input_startStation

        # 取得抵達縣市
        self.cities_endStation = {}
        self.citiesSort_endStation = {}
        self.input_endStationCity = input_endStationCity

        # 抵達站
        self.stationSort_endStation = {}
        self.input_endStation = input_endStation

        # 時間
        self.input_date = input_date
        self.input_startTime = input_startTime
        self.input_endTime = input_endTime

        # 查詢結果班次
        self.train_list = []

        # 原始頁碼
        self.last_url = ''

    def clickStartStationCity(self):
        print("縣市如下：")
        self.count = 2
        # debug
        for city in self.doc("#mainline > div:nth-child(1) > ul > li:nth-child(n+2)").items():
            print(city.text())
            temp_city_id = self.doc("#mainline > div:nth-child(1) > ul > li:nth-child(" +
                                    str(self.count) + ") > button").attr("data-type")
            self.citiesSort_startStation[city.text()] = self.count
            self.cities_startStation[city.text()] = temp_city_id
            self.count += 1

        # 點選出發縣市按鈕
        self.driver.find_element_by_xpath(
            "//*[@id='queryForm']/div/div[1]/div[2]/div[2]/button[1]").click()
        time.sleep(0.1)

        # 點選縣市
        self.driver.find_element_by_xpath("//*[@id='mainline']/div[1]/ul/li[{0}]/button".format(
            self.citiesSort_startStation[self.input_startStationCity])).click()

    def clickStartStation(self):
        print("站名：")
        self.stationCount = 1
        for station in self.doc("#{0} > ul > li:nth-child(n+1) > button".format(self.cities_startStation[self.input_startStationCity])).items():
            self.stationSort_startStation[station.text()] = self.stationCount
            print(station.text())
            self.stationCount += 1

        # input_startStation = input("輸入出發站：")
        time.sleep(0.1)

        # 點選出發站
        self.driver.find_element_by_xpath("//*[@id='{0}']/ul/li[{1}]/button".format(
            self.cities_startStation[self.input_startStationCity], self.stationSort_startStation[self.input_startStation])).click()

# 出發站一系列動作--結束
# -----------============================================================================================ #

# ======================================================================================================= #
# 抵達站一些列動作--開始
    def clickEndStationCity(self):
        print("縣市如下：")
        self.count2 = 2
        for city in self.doc("#mainline > div:nth-child(1) > ul > li:nth-child(n+2)").items():
            print(city.text())
            temp_city_id2 = self.doc("#mainline > div:nth-child(1) > ul > li:nth-child(" +
                                     str(self.count) + ") > button").attr("data-type")
            self.citiesSort_endStation[city.text()] = self.count2
            self.cities_endStation[city.text()] = temp_city_id2
            self.count2 += 1

        # input_endStationCity = input("輸入抵達縣市：")
        time.sleep(0.3)

        # 點開抵達站按鈕
        self.driver.find_element_by_xpath(
            "//*[@id='queryForm']/div/div[1]/div[4]/div[2]/button[1]").click()
        time.sleep(0.1)

        # 點選縣市
        self.driver.find_element_by_xpath("//*[@id='mainline']/div[1]/ul/li[{0}]/button".format(
            self.citiesSort_startStation[self.input_endStationCity])).click()

    def clickEndStation(self):
        # 印出站名
        print("站名如下：")
        endStationCount = 1
        for station in self.doc("#{0} > ul > li:nth-child(n+1) > button".format(self.cities_startStation[self.input_endStationCity])).items():
            self.stationSort_endStation[station.text()] = endStationCount
            print(station.text())
            endStationCount += 1

        # input_endStation = input("輸入抵達站：")
        time.sleep(0.1)

        # 點選抵達站
        self.driver.find_element_by_xpath("//*[@id='{0}']/ul/li[{1}]/button".format(
            self.cities_startStation[self.input_endStationCity], self.stationSort_endStation[self.input_endStation])).click()

# 抵達站一系列動作--結束
# =================================================================================================== #


# =================================================================================================== #
# 選擇日期時間

    def clickDateAndTime(self):
        # input_date = input("輸入日期：")
        self.driver.execute_script(
            "document.getElementById('rideDate').value='{0}'".format(self.input_date))

        # input_startTime = input("輸入時間（起）：")
        self.driver.execute_script(
            "document.getElementById('startTime').value='{0}'".format(self.input_startTime))

        # input_endTime = input("輸入出發時間（到）：")
        self.driver.execute_script(
            "document.getElementById('endTime').value='{0}'".format(self.input_endTime))

        self.driver.find_element_by_xpath(
            "//*[@id='queryForm']/div/div[3]/div[1]/div[2]/label[1]").click()


# 選擇日期時間結束
# ================================================================================================ #

# ================================================================================================ #
# 點下查詢按鈕//*[@id="queryForm"]/div[1]/div[3]/div[3]/input

    def clickSearch(self):
        self.last_url = self.driver.current_url
        self.driver.find_element_by_xpath(
            "//*[@id='queryForm']/div/div[3]/div[3]/input").click()
        print("點選成功")
        time.sleep(0.1)

        # 等待頁面跳轉，最多30次
        retry_count = 30
        errorMessage = ''
        while self.last_url == self.driver.current_url and retry_count > 0:
            retry_count -= 1
            if self.doc("#errorDiv").attr('style') != "display: none":
                errorMessage = self.doc("#errorDiv .mag-error").text()
                break
            time.sleep(0.1)

        if self.doc("#errorDiv").attr('style') == "display: none" and errorMessage == "":
            result_html = self.driver.find_element_by_css_selector(
                "*").get_attribute("outerHTML")
            result_doc = pq(result_html)

            alertMessage = result_doc(
                "#content > div.alert.alert-warning").text()
            if alertMessage != '':
                print(alertMessage)
            else:
                result_doc(
                    "#pageContent > div > table > tbody > tr.trip-column")

                for result in result_doc("#pageContent > div > table > tbody > tr.trip-column").items():
                    train_number_str = result.find("ul.train-number a").text()
                    departure_time_str = result.children("td").eq(1).text()
                    arrival_time_str = result.children("td").eq(2).text()
                    travel_time_str = result.children("td").eq(3).text()
                    adult_price_str = result.find("td").eq(6).text()
                    child_price_str = result.children("td").eq(7).text()
                    old_price_str = result.children("td").eq(8).text()

                    self.train_list.append(train(train_number_str, departure_time_str, arrival_time_str, travel_time_str, adult_price_str,
                                                 child_price_str, old_price_str))

                    # result_trans.append(
                    #    {'車次': temp_train_number, '出發時間': temp_departure_time, '抵達時間': temp_arrival_time, '行駛時間': temp_travel_time, '全票': temp_adult_price, '孩童票': temp_child_price, '敬老票': temp_old_price})

                # print(tabulate(result_trans, headers='keys', tablefmt="grid"))

        # else:
        #    print(errorMessage)

# 查詢動作結束
# ================================================================================================================== #

    def clickAllStep(self):
        self.clickStartStationCity()
        self.clickStartStation()
        self.clickEndStationCity()
        self.clickEndStation()
        self.clickDateAndTime()
        self.clickSearch()
# ======================================================================================================== #
# 印出時刻表S

    def filterByTrainCategory(self, category):
        return_list = []
        for t in self.train_list:
             for c in category:
                if (c == t.category):
                    return_list.append(t)
                    break
        self.train_list = return_list
    
    def get_first_three(self):
        first_three = self.train_list[0:3]
        return sorted(first_three, key=cmp_to_key(mulTime))
        
    def sort_train_list(self):
        print('sort_train_list')
        self.train_list = sorted(self.train_list, key=cmp_to_key(mulTime))
    
    def get_train_list(self):
        return self.train_list
    
def mulTime(t1, t2):
    t1_time = re.split(':', t1.arrival_time)
    t1_sec = int(t1_time[0])*60 + int(t1_time[1])
    t2_time = re.split(':', t2.arrival_time)
    t2_sec = int(t2_time[0])*60 + int(t2_time[1])
    diff = t1_sec - t2_sec
    if (diff == 0):
        return 0
    elif (diff > 0):
        return 1
    else:
        return -1