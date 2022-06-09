

import os
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from util.stt_service_client import stt

import sys
sys.path.append("webclawer")
from train import train, trainUtil
from railway import Railway

from flask import Flask, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
session = {
    "cur_page": 0,
    "station": "",
    "num": 0,
    "car_type": [],
    "hour": "",
    "min": "",
    "search_hour_min": "",
    "car_list": [],
    "select_car": {},
    "audio_ts": ""
}


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
            

import voice_generate as voice
def redirect_admin():
    global session
    print(session)
    cur_page = session["cur_page"]
    url = ""
    if cur_page == 1: 
        url = "/buy_ticket_confirm"
    elif cur_page == 2: 
        url = "/location/location"
    elif cur_page == 3:
        session["station"] = "萬華"
        session["audio_ts"] = voice.g_005(session["station"])
        url = "/location/confirm_location"
    elif cur_page == 5:
        url = "/num/num"
    elif cur_page == 6:
        session["num"] = 3
        session["audio_ts"] = voice.g_007(session["num"])
        url = "/num/confirm_num"
    elif cur_page == 7:
        url = "/car/car"
    elif cur_page == 8:
        session["car_type"] = ["自強號","區間車"]
        session["hour"] = 4
        session["min"] = 10
        if int(session["min"]) >= 30: search_start_min = 30
        else: search_start_min = 0
        print("search:", session["hour"], search_start_min, get_city(session["station"]), session["station"])
        print("filter:", session["hour"], session["min"], session["car_type"])

        session["car_list"] = [
            {"hour": "22", "min": "00", "car": "莒光號"},
            {"hour": "16", "min": "40", "car": "區間車"},
            {"hour": "12", "min": "33", "car": "自強號"},
        ]
        session["audio_ts"] = voice.g_009(session["car_list"])
        url = "/car/recent_car"
    elif cur_page == 9:
        url = "/car/top_3_car"
    elif cur_page == 11:
        session["select_car"] = {"hour": "12", "min": "33", "car": "自強號"}
        session["audio_ts"] = voice.g_012(session["select_car"], session["num"])
        url = "/car/confirm_car"
    elif cur_page == 12:
        url = "/type/type"


    print(url)
    return {
        "status": "success",
        "url": url
    }

@app.route("/audioUpload", methods=["POST"])
def form():
    print(request.files)
    afile = request.files.get("audio-file")
    afile.save(f"static/audio/{afile.filename}")

    result = stt(f"static/audio/{afile.filename}", "ishianTW")
    print(result)
    return redirect_admin()


@app.route("/")
def index():
    global session
    session["cur_page"] = 1
    return render_template("index.html")


@app.route("/buy_ticket_confirm")
def buy_ticket_confirm():
    global session
    session["cur_page"] = 2
    return render_template("buy_ticket_confirm.html")

# location


@app.route("/location/location")
def location():
    global session
    session["cur_page"] = 3
    return render_template("location/location.html")


@app.route("/location/select_location", methods=["GET"])
def select_location():
    return render_template("location/select_location.html")


@app.route("/location/select_location", methods=["POST"])
def select_location_post():
    global session
    obj = request.get_json()
    print(obj)
    session["station"] = obj["station"]
    session["audio_ts"] = voice.g_005(session["station"])
    return {"status": "success"}


@app.route("/location/confirm_location")
def confirm_location():
    global session
    session["cur_page"] = 5
    return render_template("location/confirm_location.html", 
        audio_url=session["audio_ts"], station=session["station"])

# num


@app.route("/num/num")
def num():
    global session
    session["cur_page"] = 6
    return render_template("num/num.html")


@app.route("/num/select_num", methods=["GET"])
def select_num():
    return render_template("num/select_num.html")

@app.route("/num/select_num", methods=["POST"])
def select_num_post():
    global session
    obj = request.get_json()
    print(obj)
    session["num"] = obj["num"]
    session["audio_ts"] = voice.g_007(session["num"])
    return {"status": "success"}


@app.route("/num/confirm_num")
def confirm_num():
    global session
    session["cur_page"] = 7
    return render_template("num/confirm_num.html",
        audio_url=session["audio_ts"], num=session["num"])

# car


@app.route("/car/car")
def car():
    global session
    session["cur_page"] = 8
    return render_template("car/car.html")


@app.route("/car/select_car_time", methods=["GET"])
def select_car_time():
    return render_template("car/select_car_time.html")


@app.route("/car/select_car_time", methods=["POST"])
def select_car_time_post():
    global session
    obj = request.get_json()
    print(obj)
    session["car_type"] = obj["car_type"]
    session["hour"] = (obj["hour"]).zfill(2)
    session["min"] = (obj["min"]).zfill(2)

    if int(session["min"]) >= 30: 
        search_start_min = "30"
    else: 
        search_start_min = "00"

    session["search_hour_min"] = session["hour"].zfill(2) + ":" + str(search_start_min)

    print("search:", session["hour"], search_start_min, session["search_hour_min"], get_city(session["station"]), session["station"])
    print("filter:", session["hour"], session["min"],  session["car_type"])

    railway = Railway(input_endStationCity=get_city(session["station"]), input_endStation=session["station"], 
                      input_startTime=session["search_hour_min"])
    railway.clickAllStep()
    print(session["car_type"])
    # railway.filterByTrainCategory(session["car_type"])
    train_list = railway.get_train_list()

    # print all trains
    trainUtil.print_train_list(train_list)
    print('-----------------')
    print('first train:')

    # print first train
    trainUtil.print_first_train(train_list)

    # print("search:", session["hour"], search_start_min, get_city(session["station"]), session["station"])
    # print("filter:", session["hour"], session["min"], session["car_type"])

    session["car_list"] = [
        {"hour": "15", "min": "38", "car": "自強號"},
        {"hour": "16", "min": "40", "car": "區間車"},
        {"hour": "22", "min": "00", "car": "莒光號"},
    ]
    session["audio_ts"] = voice.g_009(session["car_list"])
    return {"status": "success"}


@app.route("/car/recent_car")
def recent_car():
    global session
    session["cur_page"] = 9
    return render_template("car/recent_car.html", 
        audio_url=session["audio_ts"], car_list=json.dumps(session["car_list"]))


@app.route("/car/full_car")
def full_car():
    return render_template("car/full_car.html")


@app.route("/car/no_car")
def no_car():
    return render_template("car/no_car.html")


@app.route("/car/top_3_car")
def top_3_car():
    global session
    session["cur_page"] = 11
    session["audio_ts"] = voice.g_011(session["car_list"])
    return render_template("car/top_3_car.html", audio_url=session["audio_ts"])

@app.route("/car/select_top_3_car_time", methods=["GET"])
def select_top_3_car_time():
    return render_template("car/select_top_3_car_time.html")

@app.route("/car/select_top_3_car_time", methods=["POST"])
def select_top_3_car_time_post():
    global session
    obj = request.get_json()
    print(obj)
    session["select_car"] = obj
    session["audio_ts"] = voice.g_012(session["select_car"], session["num"])
    return {"status": "success"}


@app.route("/car/confirm_car")
def confirm_car():
    global session
    session["cur_page"] = 12
    return render_template("car/confirm_car.html", 
        audio_url=session["audio_ts"], select_car=json.dumps(session["select_car"]))

# type


@app.route("/type/type")
def type():
    return render_template("type/type.html")


@app.route("/type/type_num")
def type_num():
    return render_template("type/type_num.html")


@app.route("/type/select_type_num")
def select_type_num():
    return render_template("type/select_type_num.html")


@app.route("/type/confirm_type")
def confirm_type():
    return render_template("type/confirm_type.html")

# confirm


@app.route("/confirm/confirm_everything")
def confirm_everything():
    return render_template("confirm/confirm_everything.html")


@app.route("/confirm/modified_before_confirm")
def modified_before_confirm():
    return render_template("confirm/modified_before_confirm.html")

# pay
# e_pay or card_pay


@app.route("/pay/payment_type_ask")
def payment_type_ask():
    return render_template("pay/payment_type_ask.html")

# cash


@app.route("/pay/cash/cash_total")
def cash_total():
    return render_template("pay/cash/cash_total.html")


@app.route("/pay/cash/cash_pay")
def cash_pay():
    return render_template("pay/cash/cash_pay.html")


@app.route("/pay/cash/cash_change")
def cash_change():
    return render_template("pay/cash/cash_change.html")

# e_pay


@app.route("/pay/payment_type_e")
def payment_type_e():
    return render_template("pay/payment_type_e.html")

# card


@app.route("/pay/card/card_pay")
def card_pay():
    return render_template("pay/card/card_pay.html")


@app.route("/pay/card/card_pay_done")
def card_pay_done():
    return render_template("pay/card/card_pay_done.html")

# e-pay


@app.route("/pay/e/e_pay")
def e_pay():
    return render_template("pay/e/e_pay.html")


@app.route("/pay/e/e_pay_done")
def e_pay_done():
    return render_template("pay/e/e_pay_done.html")

# finish


@app.route("/finish/finish")
def finish():
    return render_template("finish/finish.html")


@app.route("/finish/pls_come_again")
def pls_come_again():
    return render_template("finish/pls_come_again.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
