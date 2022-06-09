import os, csv
import glob
import subprocess
from datetime import datetime

subprocess.run(["C:/ffmpeg/bin/ffmpeg.exe"])
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

def cut_start_end():
    glob_path = os.path.join(root_path, "**", "*.wav")
    for in_path in glob.glob(glob_path, recursive=True):
        out_path = os.path.join(os.path.split(in_path)[0], '_'+os.path.split(in_path)[1])
        print(in_path, out_path)
        
        subprocess.run(["C:/ffmpeg/bin/ffmpeg.exe", "-i", in_path, "-af", "silenceremove=start_periods=1:start_threshold=-40dB:detection=peak,areverse,silenceremove=start_periods=1:start_threshold=-40dB:detection=peak,areverse", out_path])

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

    subprocess.run(["C:/ffmpeg/bin/ffmpeg.exe", "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
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

    subprocess.run(["C:/ffmpeg/bin/ffmpeg.exe", "-y", "-f", "concat", "-safe", "0", "-i", "merge_list.txt", "-c:v", "copy", system_path_out])
    return ts