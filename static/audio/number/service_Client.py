# !/usr/bin/env python
# _*_coding:utf-8_*_

# 給任何使用這支程式的人：這支程式是新版台語台羅語音合成的API的client端。具體上會發送最下方變數data的台羅
# 給伺服器，並接收一個回傳的wav檔，output.wav
# 接受之台羅為教育部羅馬拼音，非教會羅馬拼音，請注意。
# 接受格式為UTF-8台羅，不是帶數字的。即請用類似"phái-sè"而非"phai2-se3"這種
# 不同port可以有不同格式，詳見下面的[注意]

#客戶端 ，用來呼叫service_Server.py
import os
import socket
import sys
import struct
import time
### Don't touch
def askForService(token,data,model,name):
    # HOST, PORT 記得修改
    global HOST
    global PORT
    ts = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = ""
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token+"@@@" + data + "@@@" + model, "utf-8")
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)
        

        with open(f'{name}.wav','wb') as f:
            while True:
                # print("True, wait for 15sec")
                # time.sleep(15)
                
                l = sock.recv(8192)
                # print('Received')
                if not l: break
                f.write(l)
    finally:
        sock.close()
    return ts
### Don't touch

def process(token,data,model,name):
    # 可在此做預處理
    start = time.time()
    # 送出
    ts = askForService(token,data,model,name)
    # 可在此做後處理
    print(time.time()-start)
    return ts

def tts(model, data, name):
    global HOST
    global PORT
    ######### 注意：以下數字，10008為原版，10010套用實驗室變調版，10012則是接受中文輸入，即多套一個中文轉台羅
    ### ***10008以及10010接受台羅，10012接受中文
    HOST, PORT = "140.116.245.146", 10012
    token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTc3NDYwNzQsImlhdCI6MTY0MDA2NjA3NCwic3ViIjoiIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJpc3MiOiJKV1QiLCJ1c2VyX2lkIjoiMjk3IiwibmJmIjoxNjQwMDY2MDc0LCJ2ZXIiOjAuMSwic2VydmljZV9pZCI6IjI0IiwiaWQiOjQyMywic2NvcGVzIjoiMCJ9.hagrNms65H0rwT7KxYySRpPy7IlvwafP3RAyyhVoThPGAeZwzfsHmCQcR2yEDzW1u32jRT01FoKdUtGFLUi1EuXwbsTyCaH5ylFLVjh81Swev-MM7ks4rka9GJq-0TKyU8qW1t_NiyNurZKLRfbFFFdy7Uy78RjqJgS4TQ6E8L4"
    # 男生聲音: model = "M12_sandhi" / 女生聲音: model = "F14_sandhi"
    
    # data = "lîm--sian--sinn ê tsa-bóo-kiánn、 tíng-kò-gue̍h tsò--lâng āu--ji̍t 、tio̍h beh kè--lâng"
    ts = process(token, data, model, name)
    return ts

def digit(num):
    if num == 1: return "tsit4"
    elif num == 2: return "nng3"
    elif num == 3: return "sann7"
    elif num == 4: return "si2"
    elif num == 5: return "goo3"
    elif num == 6: return "lak4"
    elif num == 7: return "tshit8"
    elif num == 8: return "peh2"
    elif num == 9: return "kau2"
    else: return ""
    
def convert(num):
    temp = ""
    if num // 10 != 0:
        if num // 10 == 1:
            temp = "tsap4"
        elif num // 10 == 2:
            temp = "ji3 tsap4"
        else:
            temp = digit(num//10) + " " + "tsap4"
        num %= 10
        
        if num == 1: temp += " " + "i1"
        elif num == 2: temp += " " + "ji7"
        else: temp += " " + f"{digit(num)}"

    
    else:
        temp = digit(num)
    
    return temp
   
def number():
    for i in range(1, 100):
        if i == 63 or i == 73 or i == 76 or i == 78: continue
        str_num = convert(i)
        print(str_num)
        tts("M12", str_num, i)
        
if __name__ == "__main__":

    for i in range(1, 100):
        str_num = convert(i)
        print(str_num)
        tts("M12", str_num, i)
        

    
    