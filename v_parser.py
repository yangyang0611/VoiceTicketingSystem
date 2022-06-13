from asyncio.windows_events import NULL
import voice_generate as voice
import sys, os, csv, re
from datetime import datetime
sys.path.append("webclawer")
from train import train, trainUtil
from railway import Railway
check_search_train_bool = False

def get_city(station):
    station_r = {
        "基隆市": ["基隆","三坑","八堵","七堵","百福","海科館","暖暖"],
        "新北市": ["五堵","汐止","汐科","板橋","浮洲","樹林","南樹林","山佳","鶯歌","福隆","貢寮","雙溪","牡丹","三貂嶺","大華","十分","望古","嶺腳","平溪","菁桐","猴硐","瑞芳","八斗子","四腳亭"],
        "臺北市": ["南港","松山","臺北","萬華"],
        "桃園市": ["桃園","內壢","中壢","埔心","楊梅","富岡","新富"],
        "新竹縣": ["北湖","湖口","新豐","竹北","竹中","六家","上員","榮華","竹東","橫山","九讚頭","合興","富貴","內灣"],
        "新竹市": ["北新竹","千甲","新莊","新竹","三姓橋","香山"],
        "苗栗縣": ["崎頂","竹南","談文","大山","後龍","龍港","白沙屯","新埔","通霄","苑裡","造橋","豐富","苗栗","南勢","銅鑼","三義"],
        "臺中市": ["日南","大甲","臺中港","清水","沙鹿","龍井","大肚","追分","泰安","后里","豐原","栗林","潭子","頭家厝","松竹","太原","精武","臺中","五權","大慶","烏日","新烏日","成功"],
        "彰化縣": ["彰化","花壇","大村","員林","永靖","社頭","田中","二水","源泉"],
        "南投縣": ["濁水","龍泉","集集","水里","車埕"],
        "雲林縣": ["林內","石榴","斗六","斗南","石龜"],
        "嘉義縣": ["大林","民雄","水上","南靖"],
        "嘉義市": ["嘉北","嘉義"],
        "臺南市": ["後壁","新營","柳營","林鳳營","隆田","拔林","善化","南科","新市","永康","大橋","臺南","保安","仁德","中洲","長榮大學","沙崙"],
        "高雄市": ["大湖","路竹","岡山","橋頭","楠梓","新左營","左營","內惟","美術館","鼓山","三塊厝","高雄","民族","科工館","正義","鳳山","後庄","九曲堂"],
        "屏東縣": ["六塊厝","屏東","歸來","麟洛","西勢","竹田","潮州","崁頂","南州","鎮安","林邊","佳冬","東海","枋寮","加祿","內獅","枋山"],
        "臺東縣": ["大武","瀧溪","金崙","太麻里","知本","康樂","臺東","山里","鹿野","瑞源","瑞和","關山","海端","池上"],
        "花蓮縣": ["富里","東竹","東里","玉里","三民","瑞穗","富源","大富","光復","萬榮","鳳林","南平","林榮新光","豐田","壽豐","平和","志學","吉安","花蓮","北埔","景美","新城","崇德","和仁","和平"],
        "宜蘭縣": ["漢本","武塔","南澳","東澳","永樂","蘇澳","蘇澳新","冬山","羅東","中里","二結","宜蘭","四城","礁溪","頂埔","頭城","外澳","龜山","大溪","大里","石城"],
    }
    for city, value in station_r.items():
        if station in value:
            return city

csv_path = os.path.join("static", "audio", "station", "TRA.csv")
with open(csv_path, newline='\n', encoding='utf-8-sig') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=','))
    all_station = [i[0] for i in rows]
# print(all_station)

csv_path = os.path.join("static", "audio", "number", "NUM.csv")
with open(csv_path, newline='\n', encoding='utf-8-sig') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=','))
    all_number = dict()
    for i in rows:
        all_number[i[1]] = i[7]
print(all_number)

number_14 = {
    "一": 1,
    "二": 2,
    "兩": 2,
    "三": 3,
    "四": 4,
}

all_car = ["自強", "區間", "莒光", "普悠瑪", "太魯閣"]
negative = ["bo", "m", "mai", "be", "bian"]
positive = ["ho", "si", "beh", "ai", "tioh", "u", "heh", "e"]

def parse_v(result):
    print(result[:3])
    all_r = {
        "negative": False,
        "positive": False,
        "yn_measure": 0,
        "station": "",
        "num": -1,
        "time": {},
        "car": [],
        "pay": ""
    }
    for v in result[:5]:
        r = {
            "negative": False,
            "positive": False,
            "station": "",
            "num": -1,
            "time": {},
            "car": [],
            "pay": ""
        }

        pinyin_list = re.findall(r'([a-z]+)\*', v)
        if len(set(pinyin_list) & set(negative)) != 0:
            r["negative"] = True
            all_r["negative"] = True
            all_r["yn_measure"] -= 1
        elif len(set(pinyin_list) & set(positive)) != 0:
            r["positive"] = True
            all_r["positive"] = True
            all_r["yn_measure"] += 1

        # 第一個偵測到的車站
        matches = []
        for station in all_station:
            if station in v:
                matches.append(station)
        if len(matches) > 0: 
            r["station"] = matches[-1]
            if all_r["station"] == "": all_r["station"] = r["station"]

        # 第一個偵測到的數字
        matches = []
        for num_str, num in number_14.items():
            if num_str in v:
                matches.append(int(num))
        if len(matches) > 0: 
            r["num"] = matches[-1]
            if all_r["num"] == -1: all_r["num"] = r["num"]
        
        # 第一個偵測到的時間
        matchObj = re.search( r'([一二三四五六七八九十]+).*點([半]?)', v)
        if matchObj:
            hour = -1
            min = -1
            matches = []
            if matchObj.group(1) in all_number:
                matches.append(all_number[matchObj.group(1)])
            if len(matches) > 0: hour = matches[-1]

            matches = []
            if matchObj.group(2) == "":
                matches.append(0)
            else:
                matches.append(30)
            if len(matches) > 0: min = matches[-1]

            if hour != -1 and min != -1:
                r["time"] = {
                    "hour": hour,
                    "min": min,
                }
                if not all_r["time"]:
                    all_r["time"] = r["time"]

        # 聽到的所有車種
        matches = []
        for car in all_car:
            if car in v:
                matches.append(car)
        if len(matches) > 0: 
            r["car"] = matches
            all_r["car"] = list(set(all_r["car"]).union(set(r["car"])))

        # E 金融
        matches = []
        for pay in ["信用卡", "行動支付"]:
            if pay in v:
                matches.append(pay)
        if len(matches) > 0: 
            r["pay"] = matches[-1]
            if all_r["pay"] == "": all_r["pay"] = r["pay"]

        print(r)

    print(all_r)
    return all_r


def redirect_admin(session, result):
    global check_search_train_bool
    v_result = parse_v(result)
    print(session)
    cur_page = session["cur_page"]
    url = ""
    if cur_page == 1: 
        # "/"
        # if v_result["yn_measure"] < 0: url = "/"
        if not v_result["positive"]: url = "/"
        else: url = "/buy_ticket_confirm"
    elif cur_page == 2: 
        # "/buy_ticket_confirm"
        # if v_result["yn_measure"] < 0: url = "/buy_ticket_confirm"
        if not v_result["positive"]: url = "/buy_ticket_confirm"
        else: url = "/location/location"
    elif cur_page == 3:
        # "/location/location"
        if v_result["station"] == "": url = "/location/location"
        else:
            session["station"] = v_result["station"]
            session["audio_ts"] = voice.g_005(session["station"])
            url = "/location/confirm_location"
    elif cur_page == 5:
        # "/location/confirm_location"
        # if v_result["yn_measure"] < 0: url = "/location/location"
        if not v_result["positive"]: url = "/location/location"
        else: url = "/num/num"
    elif cur_page == 6:
        # "/num/num"
        if v_result["num"] == -1: url = "/num/num"
        else:
            session["num"] = v_result["num"]
            session["audio_ts"] = voice.g_007(session["num"])
            url = "/num/confirm_num" 
    elif cur_page == 7:
        # "/num/confirm_num"
        # if v_result["yn_measure"] < 0: url = "/num/num"
        if not v_result["positive"]: url = "/num/num"
        else: url = "/car/car"
    elif cur_page == 8:
        # "/car/car"
        check_search_train_bool = True
        if len(v_result["car"]) != 0: session["car_type"] =  v_result["car"]
        else: session["car_type"] = ["自強","區間","莒光","普悠瑪","太魯閣"]
        
        now = datetime.now()
        if v_result["time"]:
            print(v_result["time"])
            if (now.hour > int(v_result["time"]["hour"])):
                v_result["time"]["hour"] = str(int(v_result["time"]["hour"]) + 12)
            session["hour"] = str(v_result["time"]["hour"]).zfill(2)
            session["min"] = str(v_result["time"]["min"]).zfill(2)
        else:
            hour = now.hour
            min = now.minute+30
            if min >= 60: 
                min -= 60
                hour += 1
            if hour >= 24: 
                hour -= 24
            session["hour"] = str(hour).zfill(2)
            session["min"] = str(min).zfill(2)
        session["date"] = now.strftime("%Y/%m/%d")

        if int(session["min"]) >= 30: 
            search_start_min = "30"
        else: 
            search_start_min = "00"

        session["search_hour_min"] = session["hour"].zfill(2) + ":" + str(search_start_min)

        print("search:", session["hour"], search_start_min, session["search_hour_min"], get_city(session["station"]), session["station"])
        print("filter:", session["hour"], session["min"],  session["car_type"])

        railway = Railway(input_endStationCity=get_city(session["station"]), input_date = session["date"], input_endStation=session["station"], 
                        input_startTime=session["search_hour_min"])
        railway.clickAllStep()
        print(session["car_type"])

        # 挑選前3班車
        railway.filterByTrainCategory(session["car_type"])
        first_three = railway.get_first_three()
        session["car_list"] = first_three
        # train_list = railway.get_train_list()
        session["car_list"] = trainUtil.print_train_list(first_three)
        print(session["car_list"])

        # no car
        if(session["car_list"] == None):
            url = "/car/no_car"
        else:
            session["audio_ts"] = voice.g_009(session["car_list"])
            url = "/car/recent_car" 
            
        check_search_train_bool = False
    elif cur_page == 9:
        # "/car/recent_car"
        if not v_result["positive"]: url = "/car/top_3_car"
        else: 
            session["select_car"] = session["car_list"][0]
            session["audio_ts"] = voice.g_012(session["select_car"], session["num"])
            url = "/car/confirm_car"
    elif cur_page == 11:
        # "/car/top_3_car"
        if v_result["num"] < 1 or v_result["num"] > 3:
            url = "/car/top_3_car"
        else:
            if v_result["num"] == 1:
                session["select_car"] = session["car_list"][0]
            elif v_result["num"] == 2:
                session["select_car"] = session["car_list"][1]
            elif v_result["num"] == 3:
                session["select_car"] = session["car_list"][2]
            session["audio_ts"] = voice.g_012(session["select_car"], session["num"])
            url = "/car/confirm_car"
    elif cur_page == 12:
        # "/car/confirm_car"
        if not v_result["positive"]: url = "/car/top_3_car"
        else: url = "/type/type"
    elif cur_page == 13:
        # "/type/type"
        if not v_result["positive"]: 
            session["tickets"] = {
                "adult": session["num"],
                "old": 0,
                "child": 0,
                "love": 0,
            }
            url = "/type/confirm_type"
        else: url = "/type/type_num"
    elif cur_page == 14:
        # "/type/type_num"
        # 一定買老人票
        session["tickets"] = {
            "adult": 0,
            "old": session["num"],
            "child": 0,
            "love": 0,
        }
        session["audio_ts"] = voice.g_015(session["tickets"])
        url = "/type/confirm_type"
    elif cur_page == 15:
        # "/type/confirm_type"
        if not v_result["positive"]: url = "/type/type"
        else: url = "/confirm/confirm_everything"
    elif cur_page == 16:
        # "/confirm/confirm_everything"
        # 一定沒問題
        url = "/pay/payment_type_ask"
    elif cur_page == 18:
        # "/pay/payment_type_ask"
        if not v_result["positive"]: url = "/pay/payment_type_e"
        else: url = "/pay/cash/cash_total"
    elif cur_page == 21:
        # "/pay/payment_type_e"
        if v_result["pay"] == "信用卡": url = "/pay/card/card_pay"
        elif v_result["pay"] == "行動支付": url = "/pay/e/e_pay"
        else: url = "/pay/payment_type_e"


    print(url)
    return {
        "status": "success",
        "url": url
    }

if __name__ == "__main__":
    parse_v(["ori:1.臺北二十點區間 ho* hng*", " 2.臺中自強十一點 m* hng*"])