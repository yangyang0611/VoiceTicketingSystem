# 客戶端 ，用來呼叫service_Server.py
import socket
import struct
import timeit
import re
import time 

def askForService(token, data, model_name):
    # HOST, PORT 記得修改
    HOST = "140.116.245.149"
    PORT = 2802
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    model = model_name
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token + "@@@", "utf-8") + struct.pack("8s",bytes(model, encoding="utf8")) + b"L" + data
        msg = struct.pack(">I", len(msg)) + msg  # msglen
        sock.sendall(msg)
        received = str(sock.recv(1024).decode("utf-8", "ignore"))
    finally:
        sock.close()

    
    print("What we received: ", received)
    return received

#file = open(r"C:\Users\User\Downloads\hts_tw_tts\mp3-kni7tdqo", 'rb')
def api_request(file_name, model_name):

    data = open(file_name, 'rb').read() #mp3-55o3w6pl/mp3-x0p2iakm/q2r9p7h_
    token = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2NTQwODM1NDAsImlzcyI6IkpXVCIsInVzZXJfaWQiOiIyOTMiLCJzdWIiOiIiLCJhdWQiOiJ3bW1rcy5jc2llLmVkdS50dyIsImV4cCI6MTY2OTYzNTU0MCwic2NvcGVzIjoiMCIsImlhdCI6MTY1NDA4MzU0MCwiaWQiOjQzNiwidmVyIjowLjEsInNlcnZpY2VfaWQiOiIzIn0.bOezSZYxdVJmULUaVDgor-1atGraLBuc6d0h_lQoq_kLrFllsbZq5noQxdZ9W85mdXrUGFkyiBuu8LxU1_IOHrtmnTNobXdjBzzSoWFw6w5RNrNCy0xJ-wGI5nit1gcB512spzaxMQcvSQbJcT3TIiYxjWd0sNGoGRRKkPaoJbM"
    result = askForService(token, data, model_name)
    
    # 可在此做後處理
    return result

def stt(record_file, model):
    print(f"get: {record_file}")
    result = api_request(record_file, model)
    print(f"finish: {record_file}")

    return result

if __name__ == "__main__":
    # MTK_new Minnan ishianTW

    record_file = "audiotest.wav"
    start = time.time()
    result = api_request(record_file, "CTmix")
    print("Time Elapsed : ", time.time()-start)
    print(record_file)
    print("Result: ", result)
    
