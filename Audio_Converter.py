# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals  # 兼容python3.x版本
from PyInquirer import prompt, Separator, print_json
from rich import print  # 美化輸出
from rich import pretty
from rich.console import Console
from rich.progress import track
from pprint import pprint  # 美化輸出
from examples import custom_style_2
from decimal import *
import math
import os
import sys
import time
import subprocess


pretty.install()
console = Console()


class Convert_size:
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


def Chinese():
    try:
        # 顯示目錄下音源檔案
        def ShowList():
            os.system("cls" if os.name in ("nt", "dos") else "clear")  # 清除畫面
            console.print("{:-^70}".format("[bold cyan]當前目錄下的音樂檔案[/]"))
            try:
                Music_list = subprocess.getoutput(
                    "dir /B /O:S /A-d *.mp3 *.flac *.wav *.aac *.m4a *.wma 2> nul"
                ).split("\n")
                Music_number = 0
                for i in range(len(Music_list)):
                    Music_number += 1
                    console.print(
                        "("
                        + str(i + 1)
                        + ") "
                        + Music_list[i]
                        + "\t\t檔案大小: "
                        + str(
                            (Convert_size.convert_size(os.path.getsize(Music_list[i])))
                        )
                    )
                console.print("\n總共數量:{}個".format(Music_number))
            except:
                console.print("\n當前目錄下沒有音樂檔案!\n")
            Choice()

        # 輸入要轉換的檔案名稱或路徑
        def Choice():
            global Music_name, Music_names, Music_path
            try:
                console.print("{:-^70}".format(""))  # 分隔線
                Music_path = input("請輸入要轉換的音檔名稱(須在當前目錄下)或路徑加檔名:").strip()
                if os.path.isfile(Music_path):
                    Music_name = os.path.basename(Music_path)
                    Music_names = Music_name.split(".")[0]
                else:
                    console.print("\n[bold red]請輸入正確的檔名或路徑！[/] \n")
                    ShowList()
            except:
                console.print("例外錯誤！ \n")
                ShowList()
            console.print("\n要轉換的音檔名稱為:{}\n".format(Music_name))
            Choice_Audio()

        # 選擇要轉換的音源格式
        def Choice_Audio():
            console.print("{:-^70}".format(""))  # 分隔線
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
                os.path.dirname(Music_names),
                Music_names + "." + Music_audio["轉換後的音訊壓縮格式"],
            )
            console.print("\n轉換後的音訊檔名為:{}\n".format(Target_file))
            console.print("{:-^70}".format(""))  # 分隔線
            console.print("您選擇的是將{}轉換成{}\n".format(Music_name, Target_file))
            Ask = input("是否要開始轉換?(Y/N)")
            if Ask.lower() == "y":
                Audio_Convert()
            else:
                console.print("\n已取消轉換 請稍等...")
                ShowList()

        # 開始轉換
        def Audio_Convert():
            console.print("\n正在轉換中...\n")
            console.print("{:-^70}".format(""))  # 分隔線
            if Music_audio["轉換後的音訊壓縮格式"] == Music_name.split(".")[1]:
                console.print("\n轉換後的音訊格式與原檔案相同，請重新選擇轉換後的音訊格式!\n")
                Ask_End()
            else:
                start = time.perf_counter()
                ffmpeg()
                end = time.perf_counter()
                Times = Decimal((end - start)).quantize(
                    Decimal("0.00"), rounding=ROUND_HALF_UP
                )
            console.print("\n{:-^70}".format(""))  # 分隔線
            console.print("\n轉換完成! 處理時間為: ", Times, "秒\n", flush=True, file=sys.stderr)
            Ask_End()

        # 轉換處理主程序
        def ffmpeg():
            if Music_audio["轉換後的音訊壓縮格式"] == "mp3":
                os.system(
                    'ffmpeg -i "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["轉換後的音訊壓縮格式"] == "wav":
                os.system(
                    'ffmpeg -i "{}" -c:a pcm_s16le -f wav "{}"'.format(
                        Music_path, Target_file
                    )
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
                os.system(
                    'ffmpeg -i "{}" -c:a libvorbis "{}"'.format(Music_path, Target_file)
                )
            elif Music_audio["轉換後的音訊壓縮格式"] == "wma":
                os.system(
                    'ffmpeg -i "{}" -c:a wmav2 "{}"'.format(Music_path, Target_file)
                )
            else:
                console.print("轉換失敗!\n")

        # 轉換完成後的詢問
        def Ask_End():
            console.print("{:-^70}".format(""))  # 分隔線
            Ask2 = input("是否要繼續轉換?(Y/N):")
            if Ask2.lower() == "y":
                ShowList()
            else:
                console.print("\n轉換結束!\n")
                sys.exit()

    except Exception as e:
        console.print("\n產生異常錯誤!\n")
        console.print(e)
        console.print("\n請按任意鍵結束程序!", end=" ")
        os.system("pause >nul 2>nul")
        sys.exit()

    if __name__ == "__main__":
        ShowList()


def English():
    try:
        # Show list of music file in the current directory
        def ShowList():
            os.system("cls" if os.name in ("nt", "dos") else "clear")  # 清除畫面
            console.print(
                "{:-^70}".format("[bold cyan]Music files in the current directory[/]")
            )
            try:
                Music_list = subprocess.getoutput(
                    "dir /B /O:S /A-d *.mp3 *.flac *.wav *.aac *.m4a *.wma 2> nul"
                ).split("\n")
                Music_number = 0
                for i in range(len(Music_list)):
                    Music_number += 1
                    console.print(
                        "("
                        + str(i + 1)
                        + ") "
                        + Music_list[i]
                        + "\t\tThe size of the file: "
                        + str(
                            (Convert_size.convert_size(os.path.getsize(Music_list[i])))
                        )
                    )
                console.print(
                    "\nThe total number of music files: {}\n".format(Music_number)
                )
            except:
                console.print("\nThere is no music file in the current directory!\n")
            Choice()

        # Enter the choice of the music file to be converted
        def Choice():
            global Music_name, Music_names, Music_path
            try:
                console.print("{:-^70}".format(""))  # 分隔線
                Music_path = input(
                    "Please enter the file name or path and file name:"
                ).strip()
                if os.path.isfile(Music_path):
                    Music_name = os.path.basename(Music_path)
                    Music_names = Music_name.split(".")[0]
                else:
                    console.print(
                        "Please enter the correct file name or path and file name!\n"
                    )
                    ShowList()
            except:
                console.print("\nException Error!\n")
                ShowList()
            console.print(
                "\nThe file name of the music to be converted is:{}\n".format(
                    Music_name
                )
            )
            Choice_Audio()

        # Enter the choice of the audio format to be converted
        def Choice_Audio():
            console.print("{:-^70}".format(""))  # 分隔線
            questions = [
                {
                    "type": "list",
                    "name": "Choice_Audio",
                    "message": "Please select the audio format to be converted:",
                    "choices": ["MP3", "WAV", "AAC", "FLAC", "M4A", "OGG", "WMA"],
                    "filter": lambda val: val.lower(),
                }
            ]
            global Target_file, Music_audio
            Music_audio = prompt(questions, style=custom_style_2)
            Target_file = os.path.join(
                os.path.dirname(Music_names),
                Music_names + "." + Music_audio["Choice_Audio"],
            )
            console.print(
                "\nThe file name of the converted music is:{}\n".format(Target_file)
            )
            console.print("{:-^70}".format(""))  # 分隔線
            console.print(
                "You choose to convert the {} to {} format.\n".format(
                    Music_name, Target_file
                )
            )
            Ask = input("Are you sure to convert?(Y/N):")
            if Ask.lower() == "y":
                Audio_Convert()
            else:
                console.print("\nConversion canceled Please wait...\n")
                ShowList()

        # Convert the audio format
        def Audio_Convert():
            console.print("\nConversion started...\n")
            console.print("{:-^70}".format(""))  # 分隔線
            if Music_audio["Choice_Audio"] == Music_name.split(".")[1]:
                console.print(
                    "\nThe converted audio format is the same as the original file, please re-select the converted audio format!\n"
                )
                Ask_End()
            else:
                start = time.perf_counter()
                ffmpeg()
                end = time.perf_counter()
                Times = Decimal((end - start)).quantize(
                    Decimal("0.00"), rounding=ROUND_HALF_UP
                )
            console.print("\n{:-^70}".format(""))  # 分隔線
            console.print(
                "\nConversion completed! The time is {:.2f} seconds.\n".format(Times),
                flush=True,
                file=sys.stderr,
            )
            Ask_End()

        # Conversion processing main program
        def ffmpeg():
            if Music_audio["Choice_Audio"] == "wav":
                os.system(
                    'ffmpeg -i "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["Choice_Audio"] == "wav":
                os.system(
                    'ffmpeg -i "{}" -c:a pcm_s16le -f wav "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["Choice_Audio"] == "aac":
                os.system(
                    'ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["Choice_Audio"] == "flac":
                os.system(
                    'ffmpeg -i "{}" -c:a flac -compression_level 12 "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["Choice_Audio"] == "m4a":
                os.system(
                    'ffmpeg -i "{}" -c:a aac -strict experimental "{}"'.format(
                        Music_path, Target_file
                    )
                )
            elif Music_audio["Choice_Audio"] == "ogg":
                os.system(
                    'ffmpeg -i "{}" -c:a libvorbis "{}"'.format(Music_path, Target_file)
                )
            elif Music_audio["Choice_Audio"] == "wma":
                os.system(
                    'ffmpeg -i "{}" -c:a wmav2 "{}"'.format(Music_path, Target_file)
                )
            else:
                console.print("\nConversion failed!\n")

        # Ask whether to continue to convert
        def Ask_End():
            console.print("{:-^70}".format(""))  # 分隔線
            Ask2 = input("\nDo you want to convert another file?(Y/N):")
            if Ask2.lower() == "y":
                ShowList()
            else:
                console.print("\nConversion completed!\n")
                sys.exit()

    except Exception as e:
        console.print("\nException Error!\n")
        console.print(e)
        console.print("\nPress any key to exit...", end=" ")
        os.system("pause >nul 2>nul")
        sys.exit()

    if __name__ == "__main__":
        ShowList()


def Ask_language():
    os.system("cls" if os.name in ("nt", "dos") else "clear")  # 清除畫面
    questions = [
        {
            "type": "list",
            "name": "語言",
            "message": "請選擇你的語言版本(Please select your language version):",
            "choices": ["中文", "English"],
        }
    ]
    global language
    language = prompt(questions, style=custom_style_2)
    if language["語言"] == "中文":
        Chinese()
    elif language["語言"] == "English":
        English()


if __name__ == "__main__":
    Ask_language()
