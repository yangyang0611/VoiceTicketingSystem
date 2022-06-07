from util.stt_service_client import stt
from flask import Flask, render_template, request
import os
import json
from datetime import datetime, timedelta
from dateutil.parser import parse

from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/audioUpload", methods=["POST"])
def form():
    print(request.files)
    afile = request.files.get("audio-file")
    afile.save(f"static/audio/{afile.filename}")

    result = stt(f"static/audio/{afile.filename}", "ishianTW")
    return "success", 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buy_ticket_confirm")
def buy_ticket_confirm():
    return render_template("buy_ticket_confirm.html")

# location


@app.route("/location/location")
def location():
    return render_template("location/location.html")


@app.route("/location/select_location", methods=["GET"])
def select_location():
    return render_template("location/select_location.html")


@app.route("/location/select_location", methods=["POST"])
def select_location_post():
    """
    """
    obj = request.get_json()
    print(obj)
    return {"status": "success"}


@app.route("/location/confirm_location")
def confirm_location():
    return render_template("location/confirm_location.html")

# num


@app.route("/num/num")
def num():
    return render_template("num/num.html")


@app.route("/num/select_num")
def select_num():
    return render_template("num/select_num.html")


@app.route("/num/confirm_num")
def confirm_num():
    return render_template("num/confirm_num.html")

# car


@app.route("/car/car")
def car():
    return render_template("car/car.html")


@app.route("/car/select_car_time", methods=["GET"])
def select_car_time():
    return render_template("car/select_car_time.html")


@app.route("/car/select_car_time", methods=["POST"])
def select_car_time_post():
    """
    """
    obj = request.get_json()
    print(obj)
    return {"status": "success"}


@app.route("/car/confirm_car")
def confirm_car():
    return render_template("car/confirm_car.html")


@app.route("/car/full_car")
def full_car():
    return render_template("car/full_car.html")


@app.route("/car/no_car")
def no_car():
    return render_template("car/no_car.html")

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
