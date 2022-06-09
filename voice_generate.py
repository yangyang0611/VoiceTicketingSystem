import os, csv
import glob
import subprocess
from datetime import datetime

ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
# ffmpeg_path = "C:/Users/user/ffmpeg-5.0.1-full_build/bin/ffmpeg.exe"

subprocess.run([ffmpeg_path])
root_path = os.path.dirname(os.path.abspath(__file__))
print(root_path)

csv_path = os.path.join(root_path, "static", "audio", "station", "TRA.csv")
with open(csv_path, newline='\n', encoding='utf-8-sig') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=','))
    all_station = [i[0] for i in rows]
print(all_station)

station_dir = os.path.join(root_path, "static", "audio", "station")
syetem_dir = os.path.join(root_path, "static", "audio", "system")
ticket_dir = os.path.join(root_path, "static", "audio", "ticket")
number_dir = os.path.join(root_path, "static", "audio", "number")
car_dir = os.path.join(root_path, "static", "audio", "car")
empty_path = os.path.join(root_path, "static", "audio", "empty.wav")

def cut_start_end():
    glob_path = os.path.join(root_path, "**", "*.wav")
    for in_path in glob.glob(glob_path, recursive=True):
        out_path = os.path.join(os.path.split(in_path)[0], '_'+os.path.split(in_path)[1])
        print(in_path, out_path)
        
        subprocess.run([ffmpeg_path, "-i", in_path, "-af", "silenceremove=start_periods=1:start_threshold=-40dB:detection=peak,areverse,silenceremove=start_periods=1:start_threshold=-40dB:detection=peak,areverse", out_path])

def g_005(station):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    station_index = all_station.index(station)
    station_path = os.path.join(station_dir, f"{station_index}.wav")
    print(station_path)

    system_path_1 = os.path.join(syetem_dir, f"005_1.wav")
    system_path_2 = os.path.join(syetem_dir, f"005_2.wav")
    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")

    with open("merge_list.txt", "w") as f:
        f.write(f"file '{system_path_1}'\n")
        f.write(f"file '{station_path}'\n")
        f.write(f"file '{system_path_2}'\n")

    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_007(num):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    ticket_path = os.path.join(ticket_dir, f"{num}.wav")
    print(ticket_path)

    system_path_1 = os.path.join(syetem_dir, f"007_1.wav")
    system_path_2 = os.path.join(syetem_dir, f"007_2.wav")
    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")

    with open("merge_list.txt", "w") as f:
        f.write(f"file '{system_path_1}'\n")
        f.write(f"file '{ticket_path}'\n")
        f.write(f"file '{system_path_2}'\n")

    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_009(car_list):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    first = car_list[0]
    hour = first["hour"]
    min = first["min"]
    car = first["car"]

    with open("merge_list.txt", "w") as f:

        hour_num_path = os.path.join(number_dir, f"{hour}.wav")
        hour_path = os.path.join(number_dir, "hour.wav")
        f.write(f"file '{hour_num_path}'\n")
        f.write(f"file '{hour_path}'\n")

        if (min == "00"):
            min_path = os.path.join(number_dir, "oclock.wav")
            f.write(f"file '{min_path}'\n")
        else:
            min_num_path = os.path.join(number_dir, f"{min}.wav")
            min_path = os.path.join(number_dir, "minute.wav")
            f.write(f"file '{min_num_path}'\n")
            f.write(f"file '{min_path}'\n")

        f.write(f"file '{empty_path}'\n")

        if car == "區間": 
            car_path = os.path.join(car_dir, "car1.wav")
        elif car == "莒光": 
            car_path = os.path.join(car_dir, "car2.wav")
        elif car == "自強": 
            car_path = os.path.join(car_dir, "car3.wav")
        elif car == "普悠號": 
            car_path = os.path.join(car_dir, "car4.wav")
        elif car == "太魯閣": 
            car_path = os.path.join(car_dir, "car5.wav")
        f.write(f"file '{car_path}'\n")

        f.write(f"file '{empty_path}'\n")

        system_path_2 = os.path.join(syetem_dir, f"009_2.wav")
        f.write(f"file '{system_path_2}'\n")

    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_011(car_list):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")

    with open("merge_list.txt", "w") as f:
        for i, temp in enumerate(car_list):
            hour = temp["hour"]
            min = temp["min"]
            car = temp["car"]

            system_path = os.path.join(syetem_dir, f"011_{i+1}.wav")
            f.write(f"file '{system_path}'\n")

            f.write(f"file '{empty_path}'\n")

            hour_num_path = os.path.join(number_dir, f"{hour}.wav")
            hour_path = os.path.join(number_dir, "hour.wav")
            f.write(f"file '{hour_num_path}'\n")
            f.write(f"file '{hour_path}'\n")

            if (min == "00"):
                min_path = os.path.join(number_dir, "oclock.wav")
                f.write(f"file '{min_path}'\n")
            else:
                min_num_path = os.path.join(number_dir, f"{min}.wav")
                min_path = os.path.join(number_dir, "minute.wav")
                f.write(f"file '{min_num_path}'\n")
                f.write(f"file '{min_path}'\n")

            f.write(f"file '{empty_path}'\n")

            if car == "區間": 
                car_path = os.path.join(car_dir, "car1.wav")
            elif car == "莒光": 
                car_path = os.path.join(car_dir, "car2.wav")
            elif car == "自強": 
                car_path = os.path.join(car_dir, "car3.wav")
            elif car == "普悠號": 
                car_path = os.path.join(car_dir, "car4.wav")
            elif car == "太魯閣": 
                car_path = os.path.join(car_dir, "car5.wav")
            f.write(f"file '{car_path}'\n")

        f.write(f"file '{empty_path}'\n")
        system_path = os.path.join(syetem_dir, f"011_{4}.wav")
        f.write(f"file '{system_path}'\n")

    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_012(select_car, num):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    hour = select_car["hour"]
    min = select_car["min"]
    car = select_car["car"]

    with open("merge_list.txt", "w") as f:
        system_path_1 = os.path.join(syetem_dir, f"012_1.wav")
        f.write(f"file '{system_path_1}'\n")

        hour_num_path = os.path.join(number_dir, f"{hour}.wav")
        hour_path = os.path.join(number_dir, "hour.wav")
        f.write(f"file '{hour_num_path}'\n")
        f.write(f"file '{hour_path}'\n")

        if (min == "00"):
            min_path = os.path.join(number_dir, "oclock.wav")
            f.write(f"file '{min_path}'\n")
        else:
            min_num_path = os.path.join(number_dir, f"{min}.wav")
            min_path = os.path.join(number_dir, "minute.wav")
            f.write(f"file '{min_num_path}'\n")
            f.write(f"file '{min_path}'\n")

        f.write(f"file '{empty_path}'\n")

        if car == "區間": 
            car_path = os.path.join(car_dir, "car1.wav")
        elif car == "莒光": 
            car_path = os.path.join(car_dir, "car2.wav")
        elif car == "自強": 
            car_path = os.path.join(car_dir, "car3.wav")
        elif car == "普悠號": 
            car_path = os.path.join(car_dir, "car4.wav")
        elif car == "太魯閣": 
            car_path = os.path.join(car_dir, "car5.wav")
        f.write(f"file '{car_path}'\n")

        f.write(f"file '{empty_path}'\n")

        system_path_2 = os.path.join(syetem_dir, f"012_2.wav")
        f.write(f"file '{system_path_2}'\n")

        ticket_path = os.path.join(ticket_dir, f"{num}.wav")
        f.write(f"file '{ticket_path}'\n")

        system_path_3 = os.path.join(syetem_dir, f"012_3.wav")
        f.write(f"file '{system_path_3}'\n")

    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_015(tickets):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")

    with open("merge_list.txt", "w") as f:
        system_path = os.path.join(syetem_dir, f"015.wav")
        f.write(f"file '{system_path}'\n")

        if (tickets["adult"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['adult']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "adult.wav")
            f.write(f"file '{ticket_path}'\n")
        
        if (tickets["old"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['old']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "old.wav")
            f.write(f"file '{ticket_path}'\n")

        if (tickets["child"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['child']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "child.wav")
            f.write(f"file '{ticket_path}'\n")

        if (tickets["love"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['love']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "love.wav")
            f.write(f"file '{ticket_path}'\n")


    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_016(station, select_car, tickets):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    hour = select_car["hour"]
    min = select_car["min"]
    car = select_car["car"]

    with open("merge_list.txt", "w") as f:
        system_path = os.path.join(syetem_dir, f"016_1.wav")
        f.write(f"file '{system_path}'\n")

        f.write(f"file '{empty_path}'\n")

        hour_num_path = os.path.join(number_dir, f"{hour}.wav")
        hour_path = os.path.join(number_dir, "hour.wav")
        f.write(f"file '{hour_num_path}'\n")
        f.write(f"file '{hour_path}'\n")

        if (min == "00"):
            min_path = os.path.join(number_dir, "oclock.wav")
            f.write(f"file '{min_path}'\n")
        else:
            min_num_path = os.path.join(number_dir, f"{min}.wav")
            min_path = os.path.join(number_dir, "minute.wav")
            f.write(f"file '{min_num_path}'\n")
            f.write(f"file '{min_path}'\n")

        f.write(f"file '{empty_path}'\n")

        system_path = os.path.join(syetem_dir, f"016_2.wav")
        f.write(f"file '{system_path}'\n")

        f.write(f"file '{empty_path}'\n")

        station_index = all_station.index(station)
        station_path = os.path.join(station_dir, f"{station_index}.wav")
        f.write(f"file '{station_path}'\n")

        f.write(f"file '{empty_path}'\n")

        if car == "區間": 
            car_path = os.path.join(car_dir, "car1.wav")
        elif car == "莒光": 
            car_path = os.path.join(car_dir, "car2.wav")
        elif car == "自強": 
            car_path = os.path.join(car_dir, "car3.wav")
        elif car == "普悠號": 
            car_path = os.path.join(car_dir, "car4.wav")
        elif car == "太魯閣": 
            car_path = os.path.join(car_dir, "car5.wav")
        f.write(f"file '{car_path}'\n")


        if (tickets["adult"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['adult']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "adult.wav")
            f.write(f"file '{ticket_path}'\n")
        
        if (tickets["old"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['old']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "old.wav")
            f.write(f"file '{ticket_path}'\n")

        if (tickets["child"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['child']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "child.wav")
            f.write(f"file '{ticket_path}'\n")

        if (tickets["love"] > 0):
            f.write(f"file '{empty_path}'\n")
            ticket_path = os.path.join(ticket_dir, f"{tickets['love']}.wav")
            f.write(f"file '{ticket_path}'\n")
            ticket_path = os.path.join(ticket_dir, "love.wav")
            f.write(f"file '{ticket_path}'\n")

        system_path = os.path.join(syetem_dir, f"016_3.wav")
        f.write(f"file '{system_path}'\n")


    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_019(num):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    thousand = int(num // 1000)
    num %= 1000
    hundred = int(num // 100)
    num %= 100
    num = int(num)

    with open("merge_list.txt", "w") as f:
        system_path = os.path.join(syetem_dir, "019_1.wav")
        f.write(f"file '{system_path}'\n")

        if (thousand):
            num_path = os.path.join(number_dir, f"{thousand}.wav")
            f.write(f"file '{num_path}'\n")
            num_path = os.path.join(number_dir, "thousand.wav")
            f.write(f"file '{num_path}'\n")

        if (hundred):
            num_path = os.path.join(number_dir, f"{hundred}.wav")
            f.write(f"file '{num_path}'\n")
            num_path = os.path.join(number_dir, "hundred.wav")
            f.write(f"file '{num_path}'\n")

        num_path = os.path.join(number_dir, f"{num}.wav")
        f.write(f"file '{num_path}'\n")
        num_path = os.path.join(number_dir, "dollar.wav")
        f.write(f"file '{num_path}'\n")

        f.write(f"file '{empty_path}'\n")

        system_path = os.path.join(syetem_dir, "019_2.wav")
        f.write(f"file '{system_path}'\n")

    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts

def g_020(num):
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S%f")
    thousand = int(num // 1000)
    num %= 1000
    hundred = int(num // 100)
    num %= 100
    num = int(num)

    with open("merge_list.txt", "w") as f:
        system_path = os.path.join(syetem_dir, "020.wav")
        f.write(f"file '{system_path}'\n")

        f.write(f"file '{empty_path}'\n")

        if (thousand):
            num_path = os.path.join(number_dir, f"{thousand}.wav")
            f.write(f"file '{num_path}'\n")
            num_path = os.path.join(number_dir, "thousand.wav")
            f.write(f"file '{num_path}'\n")

        if (hundred):
            num_path = os.path.join(number_dir, f"{hundred}.wav")
            f.write(f"file '{num_path}'\n")
            num_path = os.path.join(number_dir, "hundred.wav")
            f.write(f"file '{num_path}'\n")

        num_path = os.path.join(number_dir, f"{num}.wav")
        f.write(f"file '{num_path}'\n")
        num_path = os.path.join(number_dir, "dollar.wav")
        f.write(f"file '{num_path}'\n")

    system_path_out = os.path.join(syetem_dir, f"{ts}.wav")
    subprocess.run([ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts