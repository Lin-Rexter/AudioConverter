# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os, sys, subprocess, time
from tokenize import Special

# PyInquirer module
from PyInquirer import prompt
from examples import custom_style_1

# Rich module
from rich import print, pretty, box
from rich.console import Console
from rich.table import Table

# 時間運算
from decimal import *

# Custom module
from ALL_Module.OS import *
from ALL_Module.Convert_size import *
from ALL_Module.ANSI_Escape_Code import *

# import curses

# rich module
pretty.install()
console = Console()


# Custom Input Validation
class Input_ask:
    def __init__(self, Message, Message_type, Error_show):
        self.Message = Message  # 提問內容
        self.Message_type = Message_type  # 提問類型
        self.Error_show = Error_show  # 是否顯示錯誤訊息
        self.Input()

    def Input(self):
        console.print(self.Message + ": ", end="")
        self.Reply = input().strip()
        self.Check()

    # 判斷輸入是否錯誤
    def Check(self):
        try:
            # 用於判斷Y或N
            if self.Message_type == "Check_Ask":
                self.Err_message = "請輸入Y或N"  # 錯誤訊息

                Valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
                self.Reply = self.Reply.lower()

                if self.Reply in Valid:
                    self.Reply = Valid[self.Reply]
                    self.Back_A()
                else:
                    self.ShowError()

            # 判斷輸入是否為正確檔名或路徑
            elif self.Message_type == "Check_File-Name":
                self.Err_message = "請輸入正確的檔名或路徑或音檔代號!"
                if Music_list != [] and (
                    os.path.exists(self.Reply)
                    or 0 < int(self.Reply) <= (int(Music_number))
                ):
                    self.Back_B()
                else:
                    self.ShowError()

            # 判斷輸入檔名是否包含非法字元
            elif self.Message_type == "Check_File-Format":
                self.Err_message = '檔名不能有 \ / : * ? " < > | 的特殊符號!'

                Special_char = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]

                if self.Reply not in Special_char:
                    self.Back_B()
                else:
                    self.ShowError()

            # 判斷檔案路徑是否正確並判斷是否有相同檔案
            elif self.Message_type == "Check_File-Path":
                self.Err_message = "目標目錄下已有同名、同類型檔案!"

                if self.Reply == "":
                    self.Reply = os.getcwd()
                    path = self.Reply + "\\" + Target_file_name
                    if not os.path.exists(path):
                        self.Back_A()
                    else:
                        self.ShowError()
                elif not os.path.exists(self.Reply):
                    self.Err_message = "路徑錯誤或不存在，請重新輸入正確路徑!"
                    self.ShowError()
                else:
                    path = self.Reply + "\\" + Target_file_name
                    if not os.path.exists(path):
                        self.Back_A()
                    else:
                        self.ShowError()

            # 未定義提問類型，顯示錯誤
            else:
                self.Err_message = "未設定或正確的提問類型參數!"
                self.ShowError()

        except Exception:
            self.ShowError()

    # 顯示錯誤訊息
    def ShowError(self):
        # 判斷參數設定是否需要顯示錯誤訊息
        if self.Error_show == True:
            Custom.Show_Err(self.Err_message)
            self.Cursor_Return_A()
        elif self.Error_show == False:
            self.Cursor_Return_B()

    # 光標回歸輸入行，清除舊輸入文字(用於有錯誤訊息的情況)
    def Cursor_Return_A(self):
        Custom.Re_Cursor_A()
        self.Input()

    # 光標回歸輸入行，清除舊輸入文字(用於無錯誤訊息的情況)
    def Cursor_Return_B(self):
        Custom.Re_Cursor_B()
        self.Input()

    # 輸入正確，回到進度
    def Back_A(self):
        Custom.Re_Err_A()  # 收回錯誤訊息
        return self.Reply

    # 輸入正確，回到進度
    def Back_B(self):
        Custom.Re_Err_B()  # 收回錯誤訊息
        return self.Reply


# 語言版本-中文
def Chinese():

    Clear()
    # 顯示目錄下音源檔案
    def ShowList():
        console.print("{:-^74}".format("[bold cyan]當前目錄下的音樂檔案[/]"))
        try:
            global Music_list, Music_number
            Music_number = 0

            Music_list = subprocess.getoutput(
                "dir /B /O:S /A-d *.mp3 *.flac *.wav *.aac *.m4a *.wma *.ogg 2> nul"
            ).split()

            # 顯示當前音檔清單
            table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
            table.add_column("數量", style="cyan", justify="center")
            table.add_column("檔案名稱", style="cyan", justify="center")
            table.add_column("檔案大小", style="cyan", justify="center")
            for i in range(len(Music_list)):
                Music_number += 1
                table.add_row(
                    "(" + str(i + 1) + ")",
                    Music_list[i],
                    str(Convert_size(os.path.getsize(Music_list[i]))),
                )
            console.print(table)

            console.print("\n[bold cyan]總共數量:{}個[/]\n".format(Music_number))
        except Exception:
            console.print("\n[bold #00ffa2]當前目錄下沒有音樂檔案![/]\n")
        Choice()

    # 輸入要轉換的檔案名稱或路徑
    def Choice():
        # 分隔線
        console.print("{:-^70}".format(""))
        # Music_path = 輸入的檔案路徑或是檔案名稱
        # Music_name = 去掉路徑後的檔案名稱
        # Music_extension = 檔案的副檔名
        global Music_path, Music_name, Music_extension

        Music_path = Input_ask(
            "\n請輸入[bold #ff7300]音檔名稱(須在當前目錄下)[/]或[bold #ff7300]完整路徑[/]或[bold #ff7300]以上檔案對應號碼[/]",
            "Check_File-Name",
            True,
        ).Reply

        # 判斷輸入的數值是否為代號，將數值變換為音檔名稱
        try:
            Music_name = Music_list[int(Music_path) - 1]  # 列表從0開始所以減1
            Music_path = Music_name
        except:
            Music_name = os.path.basename(Music_path)
        Music_extension = Music_name.split(".")[1]

        console.print("\n選擇轉換的音檔為: [bold deep_sky_blue3]{}[/]\n".format(Music_name))
        Ask_Name()

    # 輸入轉換後的檔案名稱
    def Ask_Name():
        console.print("{:-^70}".format(""))  # 分隔線
        global Ask_name

        Ask_name = Input_ask(
            "\n請輸入轉換後的音檔名稱[bold #ff7300](按下Enter默認原檔名)[/]", "Check_File-Format", True
        ).Reply

        if Ask_name == "":
            Ask_name = Music_name.split(".")[0]

        console.print("\n轉換後的音檔名稱為: [bold deep_sky_blue3]{}[/]\n".format(Ask_name))
        Choice_Audio()

    # 選擇要轉換的音源格式
    def Choice_Audio():
        console.print("{:-^70}\n".format(""))  # 分隔線
        # Target_audio = 選擇的音源格式
        # Target_file_name = 轉換後的檔案完整名稱
        global Target_audio, Target_file_name

        questions = [
            {
                "type": "list",
                "name": "轉換後的音訊壓縮格式",
                "message": "請選擇轉換後的音訊格式:",
                "choices": ["MP3", "WAV", "AAC", "FLAC", "M4A", "OGG", "WMA"],
                "filter": lambda val: val.lower(),
            }
        ]
        Target_audio = prompt(questions, style=custom_style_1)
        Target_audio = Target_audio.get("轉換後的音訊壓縮格式")
        Target_file_name = Ask_name + "." + Target_audio

        console.print(
            "\n轉換後的音檔為: [bold deep_sky_blue3]{}[/]\n".format(Target_file_name)
        )
        Ask_Path()

    # 輸入轉換後的檔案路徑
    def Ask_Path():
        console.print("{:-^70}".format(""))  # 分隔線
        # Ask_path = 設置轉換後的檔案放置位置
        # Target_file_path = 轉換後的檔案完整路徑
        global Ask_path, Target_file_path

        Ask_path = Input_ask(
            "\n請輸入轉換後的音檔存放位置[bold #ff7300](按下Enter默認當前位置)[/]", "Check_File-Path", True
        ).Reply

        Target_file_path = Ask_path + "/" + Target_file_name

        console.print(
            "\n選擇轉換後的音檔存放位置為: [bold deep_sky_blue3]{}[/]\n".format(Target_file_path)
        )
        Ask_Convert()

    # 詢問是否開始轉換
    def Ask_Convert():
        console.print("{:-^70}".format(""))  # 分隔線
        console.print(
            "\n轉換流程: [bold deep_sky_blue3]{}[/] [bold red]=>[/] [bold deep_sky_blue3]{}[/] \n".format(
                Music_path, Target_file_path
            )
        )

        Ask = Input_ask("[bold #ebcc36]是否要開始轉換? [Y/N] [/]", "Check_Ask", True).Reply

        if Ask == True:
            Audio_Convert()
        elif Ask == False:
            console.print("\n已取消轉換 請稍等...")
            Clear()
            ShowList()

    # 開始轉換
    def Audio_Convert():
        console.print("\n{:-^70}".format(""))
        if Music_extension == Target_audio:
            Ask2 = Input_ask(
                "[bold #ebcc36]\n轉換後的音訊格式與原檔案相同，是否繼續轉換? [Y/N] [/]", "Check_Ask", True
            ).Reply
            if Ask2 == True:
                print("\n")
                pass
            elif Ask2 == False:
                Ask_End()

        try:
            console.print("\n[bold red]正在轉換中...[/]\n")
            start = time.perf_counter()
            ffmpeg()
            end = time.perf_counter()
        except Exception as e:
            print(e)
            console.print("\n[bold red]轉換失敗![/]\n")
            sys.exit(0)

        Times = Decimal((end - start)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        console.print("\n{:-^70}".format(""))  # 分隔線
        console.print(
            "\n轉換完成! 處理時間為:[bold #10b4eb]{}秒[/][bold red] (估計時間非準確)[/]\n".format(Times)
        )
        Ask_End()

    # 轉換處理主程序
    def ffmpeg():
        Audio_format = {
            "mp3": '{} "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"',
            "wav": '{} "{}" -c:a pcm_s16le -f wav "{}"',
            "aac": '{} "{}" -c:a aac -strict experimental "{}"',
            "flac": '{} "{}" -c:a flac -compression_level 12 "{}"',
            "m4a": '{} "{}" -c:a aac -strict experimental "{}"',
            "ogg": '{} "{}" -c:a libvorbis "{}"',
            "wma": '{} "{}" -c:a wmav2 "{}"',
        }
        if Target_audio in Audio_format:
            os.system(
                Audio_format[Target_audio].format(
                    "ffmpeg -i", Music_path, Target_file_path
                )
            )

    # 轉換完成後的詢問
    def Ask_End():
        console.print("{:-^70}".format(""))  # 分隔線
        Ask3 = Input_ask("\n[bold #ebcc36]是否要繼續轉換? [Y/N] [/]", "Check_Ask", True).Reply
        if Ask3 == True:
            Clear()
            ShowList()
        elif Ask3 == False:
            console.print("\n\n[bold #81eb36]轉換結束![/]\n")
            Stop()
            sys.exit()

    if __name__ == "__main__":
        ShowList()


# 語言版本-English(尚未更新!!)
def English():
    Clear()
    # Show list of music file in the current directory
    def ShowList():
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
                    + str((Convert_size(os.path.getsize(Music_list[i]))))
                )
            console.print(
                "\n[bold cyan]The total number of music files: {}[/]\n".format(
                    Music_number
                )
            )
        except:
            console.print(
                "\n[bold #00ffa2]There is no music file in the current directory![/]\n"
            )
        Choice()

    # Enter the choice of the music file to be converted
    def Choice():
        global Music_name, Music_names, Music_path
        console.print("{:-^70}".format(""))  # 分隔線
        Music_path = input("Please enter the file name or path and file name:").strip()
        if os.path.isfile(Music_path):
            Music_name = os.path.basename(Music_path)
            Music_names = Music_name.split(".")[0]
        else:
            Clear()
            console.print(
                "[bold red]Please enter the correct file name or path and file name![/]\n"
            )
            ShowList()
        console.print(
            "\nThe file name of the music to be converted is:{}\n".format(Music_name)
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
        Music_audio = prompt(questions, style=custom_style_1)
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
        Audio_format = {
            "mp3": '{} "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"',
            "wav": '{} "{}" -c:a pcm_s16le -f wav "{}"',
            "aac": '{} "{}" -c:a aac -strict experimental "{}"',
            "flac": '{} "{}" -c:a flac -compression_level 12 "{}"',
            "m4a": '{} "{}" -c:a aac -strict experimental "{}"',
            "ogg": '{} "{}" -c:a libvorbis "{}"',
            "wma": '{} "{}" -c:a wmav2 "{}"',
        }
        if Target_audio in Audio_format:
            os.system(
                Audio_format[Target_audio].format("ffmpeg -i", Music_path, Target_file)
            )

    # Ask whether to continue to convert
    def Ask_End():
        console.print("{:-^70}".format(""))  # 分隔線
        Ask2 = input("\nDo you want to convert another file?(Y/N):")
        if Ask2.lower() == "y":
            ShowList()
        else:
            console.print("\n\nConversion completed!\n")
            sys.exit()

    if __name__ == "__main__":
        try:
            ShowList()
        except BaseException as e:
            console.print("\n\n[bold #52c5ff]Operation cancelled![/]\n")
            sys.exit(0)


def Ask_language():
    Clear()
    questions = [
        {
            "type": "list",
            "name": "語言",
            "message": "請選擇你的語言版本(Please select your language version):",
            "choices": ["中文", "English"],
        }
    ]
    language = prompt(questions, style=custom_style_1).get("語言")
    if language == "中文":
        try:
            Chinese()
        except KeyboardInterrupt:
            console.print("\n\n\n[bold red]已中斷程序![/]\n")
            sys.exit(0)
        except Exception as e:
            print(e)
            console.print("\n\n[bold red]發生錯誤![/]\n")
            sys.exit(0)
    elif language == "English":
        try:
            English()
        except KeyboardInterrupt:
            console.print("\n\n\n[bold red]Cenceled![/]\n")
            sys.exit(0)
        except Exception as e:
            print(e)
            console.print("\n\n[bold red]Error![/]\n")
            sys.exit(0)


if __name__ == "__main__":
    try:
        Ask_language()
    except Exception:
        console.print("\n\n[bold red]已中斷程序! Operation cancelled![/]\n")
        sys.exit()
