# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals  # 兼容python3.x版本
from PyInquirer import prompt, Separator, print_json
from rich import print  # 美化輸出
from pprint import pprint  # 美化輸出
from examples import custom_style_2
from decimal import *
import math
import os
import sys
import time
import subprocess


# 檔案大小轉換
# 參考網址: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


# 顯示目錄下音源檔案
def ShowList():
    os.system("cls" if os.name in ("nt", "dos") else "clear")  # 清除畫面
    print("{:-^60}".format("當前目錄下的音源檔案"))
    try:
        Music_list = subprocess.getoutput(
            "dir /B /O:S /A-d *.mp3 *.flac *.wav *.aac *.m4a *.wma 2> nul"
        ).split("\n")
        Music_number = 0
        for i in range(len(Music_list)):
            Music_number += 1
            print(
                "("
                + str(i + 1)
                + ") "
                + Music_list[i]
                + "\t\t檔案大小: "
                + str(convert_size(os.path.getsize(Music_list[i])))
            )
        print("\n總共數量:{}個".format(Music_number))
    except:
        print("\n目前目錄下沒有音源檔案!")
    Choice()


# 輸入要轉換的檔案名稱或路徑
def Choice():
    global Music_name, Music_names, Music_path
    try:
        print("{:-^70}".format(""))  # 分隔線
        Music_path = input("請輸入要轉換的音檔名稱(須在當前目錄下)或路徑加檔名:").strip()
        if os.path.isfile(Music_path):
            Music_name = os.path.basename(Music_path)
            Music_names = Music_name.split(".")[0]
        else:
            os.system("cls" if os.name in ("nt", "dos") else "clear")
            print("請輸入正確的MP3檔名或路徑！ \n")
            Choice()
    except:
        ShowList()
        print("請輸入正確的MP3檔名或路徑！ \n")
        Choice()
    print("\n要轉換的音檔名稱為:{}".format(Music_name))
    audio_Convert()


def audio_Convert():
    print("{:-^70}".format(""))  # 分隔線
    questions = [
        {
            "type": "list",
            "name": "轉換後的音訊壓縮格式",
            "message": "請選擇轉換後的音訊格式:",
            "choices": ["MP3", "WAV", "AAC", "FLAC", "M4A", "OGG", "WMA"],
            "filter": lambda val: val.lower(),
        }
    ]
    global Target_file, Music_audio
    Music_audio = prompt(questions, style=custom_style_2)
    Target_file = os.path.join(
        os.path.dirname(Music_names), Music_names + "." + Music_audio["轉換後的音訊壓縮格式"]
    )
    print("\n轉換後的音訊檔名為:{}".format(Target_file))
    print("{:-^70}".format(""))  # 分隔線
    print("您選擇的是將{}轉換成{}\n".format(Music_name, Target_file))
    Ask = input("是否要開始轉換?(Y/N)")
    if Ask.lower() == "y":
        Audio_Convert()
    else:
        print("\n已取消轉換 請稍等...")
        time.sleep(2)
        ShowList()


def Audio_Convert():
    print("\n正在轉換中...")
    print("{:-^70}".format(""))  # 分隔線
    start = time.perf_counter()
    ffmpeg()
    end = time.perf_counter()
    Times = Decimal((end - start)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    print("{:-^70}".format(""))  # 分隔線
    print("\n轉換完成! 處理時間為: ", Times, "秒", flush=True, file=sys.stderr)
    Ask2 = input("是否要繼續轉換?(Y/N):")
    if Ask2.lower() == "y":
        ShowList()
    else:
        print("\n結束轉換程序!")
        os.system("pause")


def ffmpeg():
    if Music_audio["轉換後的音訊壓縮格式"] == Music_name.split(".")[1]:
        print("\n轉換後的音訊格式與原檔案相同，請重新選擇轉換後的音訊格式!")
    elif Music_audio["轉換後的音訊壓縮格式"] == "mp3":
        os.system(
            'ffmpeg -i "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"'.format(
                Music_path, Target_file
            )
        )
    elif Music_audio["轉換後的音訊壓縮格式"] == "wav":
        os.system(
            'ffmpeg -i "{}" -c:a pcm_s16le -f wav "{}"'.format(Music_path, Target_file)
        )
    elif Music_audio["轉換後的音訊壓縮格式"] == "aac":
        os.system(
            'ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(
                Music_path, Target_file
            )
        )
    elif Music_audio["轉換後的音訊壓縮格式"] == "flac":
        os.system(
            'ffmpeg -i "{}" -c:a flac -compression_level 12 "{}"'.format(
                Music_path, Target_file
            )
        )
    elif Music_audio["轉換後的音訊壓縮格式"] == "m4a":
        os.system(
            'ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(
                Music_path, Target_file
            )
        )
    elif Music_audio["轉換後的音訊壓縮格式"] == "ogg":
        os.system('ffmpeg -i "{}" -c:a libvorbis "{}"'.format(Music_path, Target_file))
    elif Music_audio["轉換後的音訊壓縮格式"] == "wma":
        os.system('ffmpeg -i "{}" -c:a wmav2 "{}"'.format(Music_path, Target_file))
    else:
        os.system("ffmpeg -i {} {}".format(Music_path, Target_file))


if __name__ == "__main__":
    ShowList()
