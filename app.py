

from glob import glob
import os
import re
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from util.stt_service_client import stt
import v_parser as p
import voice_generate as voice

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
    "date": "",
    "search_hour_min": "",
    "car_list": [],
    "select_car": {},
    "tickets": {},
    "audio_ts": ""
}

@app.route("/audioUpload", methods=["POST"])
def form():
    global session
    print(request.files)
    afile = request.files.get("audio-file")
    afile.save(f"static/audio/{afile.filename}")

    result = stt(f"static/audio/{afile.filename}", "ishianTW")
    result = str(result).split('result')[0]
    result = str(result).split(';')
    return p.redirect_admin(session, result)


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
    session["car_type"] = str(obj["car_type"]).split(',')
    session["hour"] = (obj["hour"]).zfill(2)
    session["min"] = (obj["min"]).zfill(2)
    session["date"] = obj["date"]

    if int(session["min"]) >= 30: 
        search_start_min = "30"
    else: 
        search_start_min = "00"

    session["search_hour_min"] = session["hour"].zfill(2) + ":" + str(search_start_min)

    print("search:", session["hour"], search_start_min, session["search_hour_min"], p.get_city(session["station"]), session["station"])
    print("filter:", session["hour"], session["min"],  session["car_type"])

    railway = Railway(input_endStationCity=p.get_city(session["station"]), input_endStation=session["station"], 
                      input_startTime=session["search_hour_min"], input_date=session["date"])
    railway.clickAllStep()
    print(session["car_type"])

    # 挑選前3班車
    railway.filterByTrainCategory(session["car_type"])
    first_three = railway.get_first_three()
    session["car_list"] = first_three
    # train_list = railway.get_train_list()
    session["car_list"] = trainUtil.print_train_list(first_three)
    print(session["car_list"])

    # todo : no car
    
    if(session["car_list"] == None):
        print("no car ohno")
        print(session["car_list"])
        return {"status": "no car"}
    else:
        session["audio_ts"] = voice.g_009(session["car_list"])
        return {"status": "success"} # no car

    # 挑選第一班
    # first = first_three[0]
    # trainUtil.print_train_list(first)

    # print("search:", session["hour"], search_start_min, get_city(session["station"]), session["station"])
    # print("filter:", session["hour"], session["min"], session["car_type"])

    # session["car_list"] = [
    #     {"hour": "15", "min": "38", "car": "自強", "total": "456"},
    #     {"hour": "16", "min": "40", "car": "區間", "total": "666"},
    #     {"hour": "22", "min": "00", "car": "莒光", "total": "852"},
    # ]
    


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


@app.route("/car/check_search_train")
def check_search_train():
    return str(p.check_search_train_bool), 200
    

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
    
@app.route("/car/search_car")
def search_car():
    return render_template("car/search_car.html")

# type


@app.route("/type/type")
def type():
    global session
    session["cur_page"] = 13
    return render_template("type/type.html")


@app.route("/type/type_num")
def type_num():
    global session
    session["cur_page"] = 14
    return render_template("type/type_num.html")


@app.route("/type/select_type_num", methods=["GET"])
def select_type_num():
    return render_template("type/select_type_num.html")

@app.route("/type/select_type_num", methods=["POST"])
def select_type_num_post():
    global session
    obj = request.get_json()
    print(obj)
    session["tickets"] = {
        "adult": int(obj["adult"]),
        "old": int(obj["old"]),
        "child": int(obj["child"]),
        "love": int(obj["love"]),
    }
    session["audio_ts"] = voice.g_015(session["tickets"])
    return {"status": "success"}


@app.route("/type/confirm_type")
def confirm_type():
    global session
    session["cur_page"] = 15
    return render_template("type/confirm_type.html",
        audio_url=session["audio_ts"], tickets=json.dumps(session["tickets"]))

# confirm


@app.route("/confirm/confirm_everything")
def confirm_everything():
    global session
    session["cur_page"] = 16
    session["audio_ts"] = voice.g_016(session["station"], session["select_car"], session["tickets"])
    return render_template("confirm/confirm_everything.html", audio_url=session["audio_ts"])


@app.route("/confirm/modified_before_confirm")
def modified_before_confirm():
    return render_template("confirm/modified_before_confirm.html")

# pay
# e_pay or card_pay


@app.route("/pay/payment_type_ask")
def payment_type_ask():
    global session
    session["cur_page"] = 18
    return render_template("pay/payment_type_ask.html")

# cash


@app.route("/pay/cash/cash_total")
def cash_total():
    global session
    adult = int(session["tickets"]["adult"])
    half = int(session["num"]) - adult
    session["total"] = int(int(session["select_car"]["total"]) * (adult + half*0.5))
    print(session["total"])
    session["audio_ts"] = voice.g_019(session["total"])
    return render_template("pay/cash/cash_total.html",
        audio_url=session["audio_ts"], total=session["total"])


@app.route("/pay/cash/cash_pay", methods=["GET"])
def cash_pay():
    return render_template("pay/cash/cash_pay.html")


@app.route("/pay/cash/cash_pay", methods=["POST"])
def cash_pay_post():
    global session
    obj = request.get_json()
    print(obj)
    session["change"] = int(obj["change"])
    return {"status": "success"}


@app.route("/pay/cash/cash_change")
def cash_change():
    global session
    session["audio_ts"] = voice.g_020(session["change"])
    return render_template("pay/cash/cash_change.html", audio_url=session["audio_ts"])

# e_pay


@app.route("/pay/payment_type_e")
def payment_type_e():
    global session
    session["cur_page"] = 21
    return render_template("pay/payment_type_e.html")

# card


@app.route("/pay/card/card_pay")
def card_pay():
    global session
    adult = int(session["tickets"]["adult"])
    half = int(session["num"]) - adult
    session["total"] = int(int(session["select_car"]["total"]) * (adult + half*0.5))
    print(session["total"])
    session["audio_ts"] = voice.g_022(session["total"])
    return render_template("pay/card/card_pay.html",
        audio_url=session["audio_ts"], total=session["total"])


@app.route("/pay/card/card_pay_done")
def card_pay_done():
    return render_template("pay/card/card_pay_done.html")

# e-pay


@app.route("/pay/e/e_pay")
def e_pay():
    global session
    adult = int(session["tickets"]["adult"])
    half = int(session["num"]) - adult
    session["total"] = int(int(session["select_car"]["total"]) * (adult + half*0.5))
    print(session["total"])
    session["audio_ts"] = voice.g_024(session["total"])
    return render_template("pay/e/e_pay.html",
        audio_url=session["audio_ts"], total=session["total"])


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
    # app.run(host="127.0.0.1", port="5000", debug=True)
    app.run()
