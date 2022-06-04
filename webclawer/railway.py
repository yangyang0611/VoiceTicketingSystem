from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
import time
from tabulate import tabulate

driver = webdriver.Chrome()
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")

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

# ==================================================================================================================== #
# 出發站一系列動作

driver.find_element_by_xpath(
    "//*[@id='queryForm']/div/div[3]/div[1]/div[2]/label[1]").click()

print("縣市如下：")
count = 2
for city in doc("#mainline > div:nth-child(1) > ul > li:nth-child(n+2)").items():
    print(city.text())
    temp_city_id = doc("#mainline > div:nth-child(1) > ul > li:nth-child(" +
                       str(count) + ") > button").attr("data-type")
    citiesSort_startStation[city.text()] = count
    cities_startStation[city.text()] = temp_city_id
    count += 1

input_startStationCity = input("輸入出發縣市：")
time.sleep(3)

# 點選出發縣市按鈕
driver.find_element_by_xpath(
    "//*[@id='queryForm']/div/div[1]/div[2]/div[2]/button[1]").click()
time.sleep(1)

# 點選縣市
driver.find_element_by_xpath("//*[@id='mainline']/div[1]/ul/li[{0}]/button".format(
    citiesSort_startStation[input_startStationCity])).click()

print("站名：")
stationCount = 1
for station in doc("#{0} > ul > li:nth-child(n+1) > button".format(cities_startStation[input_startStationCity])).items():
    stationSort_startStation[station.text()] = stationCount
    print(station.text())
    stationCount += 1

input_startStation = input("輸入出發站：")
time.sleep(1)

# 點選出發站
driver.find_element_by_xpath("//*[@id='{0}']/ul/li[{1}]/button".format(
    cities_startStation[input_startStationCity], stationSort_startStation[input_startStation])).click()

# 出發站一系列動作--結束
# -----------============================================================================================ #

# ======================================================================================================= #
# 抵達站一些列動作--開始
print("縣市如下：")
count2 = 2
for city in doc("#mainline > div:nth-child(1) > ul > li:nth-child(n+2)").items():
    print(city.text())
    temp_city_id2 = doc("#mainline > div:nth-child(1) > ul > li:nth-child(" +
                        str(count) + ") > button").attr("data-type")
    citiesSort_endStation[city.text()] = count2
    cities_endStation[city.text()] = temp_city_id2
    count2 += 1

input_endStationCity = input("輸入抵達縣市：")
time.sleep(3)

# 點開抵達站按鈕
driver.find_element_by_xpath(
    "//*[@id='queryForm']/div/div[1]/div[4]/div[2]/button[1]").click()
time.sleep(1)

# 點選縣市
driver.find_element_by_xpath("//*[@id='mainline']/div[1]/ul/li[{0}]/button".format(
    citiesSort_startStation[input_endStationCity])).click()

# 印出站名
print("站名如下：")
endStationCount = 1
for station in doc("#{0} > ul > li:nth-child(n+1) > button".format(cities_startStation[input_endStationCity])).items():
    stationSort_endStation[station.text()] = endStationCount
    print(station.text())
    endStationCount += 1

input_endStation = input("輸入抵達站：")
time.sleep(1)

# 點選抵達站
driver.find_element_by_xpath("//*[@id='{0}']/ul/li[{1}]/button".format(
    cities_startStation[input_endStationCity], stationSort_endStation[input_endStation])).click()

# 抵達站一系列動作--結束
# =================================================================================================== #

# =================================================================================================== #
# 選擇日期時間
input_date = input("輸入日期：")
driver.execute_script(
    "document.getElementById('rideDate').value='{0}'".format(input_date))

input_startTime = input("輸入時間（起）：")
driver.execute_script(
    "document.getElementById('startTime').value='{0}'".format(input_startTime))

input_endTime = input("輸入出發時間（到）：")
driver.execute_script(
    "document.getElementById('endTime').value='{0}'".format(input_endTime))


# 選擇日期時間結束
# ================================================================================================ #

# ================================================================================================ #
# 點下查詢按鈕//*[@id="queryForm"]/div[1]/div[3]/div[3]/input
last_url = driver.current_url
driver.find_element_by_xpath(
    "//*[@id='queryForm']/div/div[3]/div[3]/input").click()
print("點選成功")
time.sleep(1)


# 等待頁面跳轉，最多30次
retry_count = 30
errorMessage = ''
while last_url == driver.current_url and retry_count > 0:
    retry_count -= 1
    if doc("#errorDiv").attr('style') != "display: none":
        errorMessage = doc("#errorDiv .mag-error").text()
        break
    time.sleep(1)

# 查詢動作結束
# ================================================================================================================== #

# ======================================================================================================== #
# 印出時刻表S

if doc("#errorDiv").attr('style') == "display: none" and errorMessage == "":
    result_html = driver.find_element_by_css_selector(
        "*").get_attribute("outerHTML")
    result_doc = pq(result_html)

    alertMessage = result_doc("#content > div.alert.alert-warning").text()
    if alertMessage != '':
        print(alertMessage)
    else:
        result_doc("#pageContent > div > table > tbody > tr.trip-column")

        for train in result_doc("#pageContent > div > table > tbody > tr.trip-column").items():
            temp_train_number = train.find("ul.train-number a").text()
            temp_departure_time = train.children("td").eq(1).text()
            temp_arrival_time = train.children("td").eq(2).text()
            temp_travel_time = train.children("td").eq(3).text()

            temp_adult_price = train.find("td").eq(6).text()
            temp_child_price = train.children("td").eq(7).text()
            temp_old_price = train.children("td").eq(8).text()

            result_trans.append(
                {'車次': temp_train_number, '出發時間': temp_departure_time, '抵達時間': temp_arrival_time, '行駛時間': temp_travel_time, '全票': temp_adult_price, '孩童票': temp_child_price, '敬老票': temp_old_price})

        print(tabulate(result_trans, headers='keys', tablefmt="grid"))

else:
    print(errorMessage)
