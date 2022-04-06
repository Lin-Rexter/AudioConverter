# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from pprint import pprint
from re import M
from PyInquirer import prompt, Separator,print_json
from examples import custom_style_2
from decimal import *
import os
import sys
import time
import subprocess

def FileSize(size):
    units=('B','KB','MB','GB','TB','PB')
    for i in range(len(units)-1,-1,-1):
        if size>=2*(1024**i):
            return str(round(size/(1024**i),3))+units[i]


def Choice():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    while True:
        print('=======================================================================')
        print('當前目錄下的音源檔案:')
        try:
            Music_list = subprocess.getoutput('dir /B /O:S /A-d *.mp3 *.flac *.wav *.aac *.m4a *.wma').split('\n')
            if len(Music_list) == 0 or Music_list == ['']:
                print('\n目前目錄下沒有音源檔案!')
            else:
                Music_number=0
                for i in range(len(Music_list)):
                    Music_number += 1
                    print('('+str(i + 1) + ') ' + Music_list[i] + ' \t檔案大小:' + str(FileSize(os.path.getsize(Music_list[i]))))
                print('\n音檔總共數量:{}個'.format(Music_number))
        except:
            print('\n目前目錄下沒有音源檔案!')
        print('=======================================================================')
        global Music_name,Music_names,Music_path
        Music_path = input("請輸入要轉換的音檔名稱(須在當前目錄下)或路徑加檔名:").strip()
        if os.path.isfile(Music_path):
            Music_name = os.path.basename(Music_path)
            Music_names = Music_name.split(".")[0]
            break;
        else:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            print("請輸入正確的MP3檔名或路徑！ \n")
    print("\n要轉換的音檔名稱為:{}".format(Music_name))
    print('=======================================================================')
    questions = [
        {
            'type': 'list',
            'name': '轉換後的音訊壓縮格式',
            'message': '請選擇轉換後的音訊格式:',
            'choices': ['MP3','WAV','AAC','FLAC','M4A','OGG','WMA'],
            'filter': lambda val: val.lower()
        }
    ]
    global Target_file,Music_audio
    Music_audio = prompt(questions, style=custom_style_2)
    Target_file = os.path.join(os.path.dirname(Music_names), Music_names + '.' + Music_audio['轉換後的音訊壓縮格式'])
    print('\n轉換後的音訊檔名為:{}'.format(Target_file))
    print('=======================================================================')
    print('您選擇的是將{}轉換成{}\n'.format(Music_name,Target_file))
    Ask = input("是否要開始轉換?(Y/N)")
    if Ask.lower() == 'y':
        End_Convert()
    else:
        print('\n已取消轉換 請稍等...')
        time.sleep(2)
        Choice()


def audio_Convert():
    if Music_audio['轉換後的音訊壓縮格式'] == Music_name.split(".")[1]:
        print('\n轉換後的音訊格式與原檔案相同，請重新選擇轉換後的音訊格式!')
    elif Music_audio['轉換後的音訊壓縮格式'] == 'mp3':
        os.system('ffmpeg -i "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'wav':
        os.system('ffmpeg -i "{}" -c:a pcm_s16le -f wav "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'aac':
        os.system('ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'flac':
        os.system('ffmpeg -i "{}" -c:a flac -compression_level 12 "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'm4a':
        os.system('ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'ogg':
        os.system('ffmpeg -i "{}" -c:a libvorbis "{}"'.format(Music_path,Target_file))
    elif Music_audio['轉換後的音訊壓縮格式'] == 'wma':
        os.system('ffmpeg -i "{}" -c:a wmav2 "{}"'.format(Music_path,Target_file)) 
    else:
        os.system('ffmpeg -i {} {}'.format(Music_path,Target_file))


def End_Convert():
    print('\n正在轉換中...')
    print('=======================================================================')
    start = time.perf_counter()
    audio_Convert()
    end = time.perf_counter()
    Times= Decimal((end - start)).quantize(Decimal('0.00'),rounding=ROUND_HALF_UP)
    print('=======================================================================')
    print("\n轉換完成! 處理時間為: ", Times, "秒", flush = True, file = sys.stderr)
    Ask2 = input("是否要繼續轉換?(Y/N):")
    if Ask2.lower() == 'y':
        Choice()
    else:
        print('\n結束轉換程序!')


if __name__ == "__main__":
    Choice()