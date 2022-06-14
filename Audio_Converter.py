# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os, sys, subprocess, time

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
from ALL_Module.Separation_Line import *
from ALL_Module.ANSI_Escape_Code import *

# rich module
pretty.install()
console = Console()

# Enlarge the window
# Window("full")

# Custom Input Validation
class Input_ask:
    def __init__(self, Message, Message_type, Error_show):
        self.Message = Message  # 提問內容
        self.Message_type = Message_type  # 提問類型
        self.Error_show = Error_show  # 是否顯示錯誤訊息
        self.Input()

    def Input(self):
        console.print(self.Message)
        self.Reply = input("=> ").strip()
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
                    self.Back_B()
                else:
                    self.ShowError()

            # 判斷輸入是否為正確檔名或路徑
            elif self.Message_type == "Check_File-Name":
                self.Err_message = "請輸入正確的檔名或路徑或音檔代號!"
                if os.path.isfile(self.Reply) or (
                    Music_list != [] and 0 < int(self.Reply) <= int(Music_number)
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
                self.Err_message = "目標目錄下已有同名、同類型檔案!       "

                if self.Reply == "":
                    self.Reply = os.getcwd()
                    Target_file = ""
                    Target_file = os.path.join(self.Reply, Target_file_name)
                if not os.path.exists(self.Reply):
                    self.Err_message = "路徑錯誤或不存在，請重新輸入正確路徑!"
                    self.ShowError()
                else:
                    Target_file = os.path.join(self.Reply, Target_file_name)

                if not os.path.exists(Target_file):
                    self.Back_B()
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
        Lines("[bold cyan]當前目錄下的音樂檔案[/]", "-", 74)
        try:
            global Music_list, Music_number
            Music_list = []
            Music_number = 0
            Music_format = ["mp3", "wav", "flac", "aac", "m4a", "wma", "ogg"]

            for file in os.listdir():
                if file.split(".")[-1] in Music_format:
                    Music_list.append(file)
                    Music_number += 1

            Music_list.sort(key=lambda x: x.split(".")[-1])

            table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
            table.add_column("號碼", style="cyan", justify="center")
            table.add_column("檔案名稱", style="cyan", justify="right")
            table.add_column("檔案大小", style="cyan", justify="center")
            for i in range(len(Music_list)):
                table.add_row(
                    "(" + str(i + 1) + ")",
                    Music_list[i],
                    str(Convert_size(os.path.getsize(Music_list[i]))),
                )
            console.print(table)

            console.print(
                "\n[bold cyan]總共數量:[bold #10b4eb]{}[/]個[/]\n".format(Music_number)
            )
        except Exception as e:
            print(e)
            console.print("\n[bold #00ffa2]當前目錄下沒有音樂檔案![/]\n")
        Choice()

    # 輸入要轉換的檔案名稱或路徑
    def Choice():
        Lines("", "-", 70)  # 分隔線

        # Music_path = 輸入的檔案路徑或是檔案名稱
        # Music_name = 去掉路徑後的檔案名稱
        # Music_extension = 檔案的副檔名
        global Music_path, Music_name, Music_extension

        Music_path = ""
        Music_name = ""
        Music_extension = ""

        Music_path = Input_ask(
            "\n請輸入[bold #ff7300]音檔名稱(須在當前目錄下)[/]或[bold #ff7300]完整路徑[/]或[bold #ff7300]以上檔案對應號碼[/]",
            "Check_File-Name",
            True,
        ).Reply
        # 判斷輸入的數值是否為代號，將數值變換為音檔名稱
        try:
            Music_name = Music_list[int(Music_path) - 1]  # 列表從0開始所以減1
            Music_path = os.path.abspath(Music_name)
        except:
            Music_name = os.path.basename(Music_path)
            Music_path = os.path.abspath(Music_path)
        Music_extension = Music_name.split(".")[1]

        console.print("\n選擇轉換的音檔為: [bold deep_sky_blue3]{}[/]\n".format(Music_name))
        Ask_Name()

    # 輸入轉換後的檔案名稱
    def Ask_Name():
        Lines("", "-", 70)  # 分隔線
        global Ask_name
        Ask_name = ""

        Ask_name = Input_ask(
            "\n請輸入轉換後的音檔名稱[bold #ff7300](按下Enter默認原檔名)[/]", "Check_File-Format", True
        ).Reply

        if Ask_name == "":
            Ask_name = Music_name.split(".")[0]

        console.print("\n轉換後的音檔名稱為: [bold deep_sky_blue3]{}[/]\n".format(Ask_name))
        Choice_Audio()

    # 選擇要轉換的音源格式
    def Choice_Audio():
        Lines("", "-", 70)  # 分隔線
        # Target_audio = 選擇的音源格式
        # Target_file_name = 轉換後的檔案完整名稱
        global Target_audio, Target_file_name
        Target_audio = ""
        Target_file_name = ""

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
        Lines("", "-", 70)  # 分隔線

        # Ask_path = 設置轉換後的檔案放置位置
        # Target_file_path = 轉換後的檔案完整路徑
        global Ask_path, Target_file_path
        Ask_path = ""
        Target_file_path = ""

        Ask_path = Input_ask(
            "\n請輸入轉換後的音檔存放位置[bold #ff7300](按下Enter默認當前位置)[/]", "Check_File-Path", True
        ).Reply
        Ask_path = os.path.abspath(Ask_path)
        Target_file_path = os.path.join(Ask_path, Target_file_name)

        console.print(
            "\n\n\n選擇轉換後的音檔存放位置為: [bold deep_sky_blue3]{}[/]\n".format(Ask_path)
        )
        Ask_Convert()

    # 詢問是否開始轉換
    def Ask_Convert():
        Lines("[bold cyan]轉換流程[/]", "-", 80)  # 分隔線

        console.print(
            "\n選擇的檔案路徑:\n[bold deep_sky_blue3]{}[/]\n".format(
                os.path.dirname(Music_path)
            )
        )
        console.print("轉換後的檔案路徑:\n[bold deep_sky_blue3]{}[/]\n".format(Ask_path))

        table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE)
        table.add_column("選擇的檔案", style="cyan", justify="center")
        table.add_column("轉換後的檔案", style="cyan", justify="center")
        table.add_row(Music_name, Target_file_name)
        console.print(table)

        Ask = Input_ask("\n[bold #ebcc36]是否要開始轉換? [Y/N] [/]", "Check_Ask", True).Reply

        if Ask == True:
            Audio_Convert()
        elif Ask == False:
            console.print("\n\n已取消轉換 請稍等...")
            Clear()
            ShowList()

    # 開始轉換
    def Audio_Convert():
        print("\n\n")
        Lines("", "-", 70)
        if Music_extension == Target_audio:
            Ask2 = Input_ask(
                "[bold #ebcc36]\n轉換後的音訊格式與原檔案相同，是否繼續轉換? [Y/N] [/]", "Check_Ask", True
            ).Reply
            if Ask2 == True:
                pass
            elif Ask2 == False:
                print("\n\n")
                Ask_End()

        try:
            print("\n")
            console.print("\n[bold red]正在轉換中...[/]\n")
            ffmpeg()
        except Exception as e:
            print(e)
            console.print("\n\n[bold red]轉換失敗![/]\n")
            sys.exit(0)

        Times = Decimal((Total_Time)).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        print("\n")
        Lines("", "-", 70)  # 分隔線

        console.print(
            "\n轉換完成! 處理時間為:[bold #10b4eb]{}秒[/][bold red] (估計時間非準確)[/]\n".format(Times)
        )
        Ask_End()

    # 轉換處理主程序
    def ffmpeg():
        global Total_Time
        Total_Time = 0

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
            start = time.perf_counter()
            subprocess.run(
                Audio_format[Target_audio].format(
                    "ffmpeg -i", Music_path, Target_file_path
                ),
                shell=True,
            )
            end = time.perf_counter()
        Total_Time = end - start

    # 轉換完成後的詢問
    def Ask_End():
        Lines("", "-", 70)  # 分隔線
        Ask3 = Input_ask(
            "\n[bold #ebcc36]是否要繼續轉換其他音檔? [Y/N] [/]", "Check_Ask", True
        ).Reply
        if Ask3 == True:
            Clear()
            ShowList()
        elif Ask3 == False:
            print("\n")
            console.print("\n[bold #81eb36]轉換結束![/]\n")
            Stop()
            sys.exit()

    if __name__ == "__main__":
        ShowList()


# 語言版本-English
def English():

    Clear()
    # Show list of audio file in current directory
    def ShowList():
        Lines("[bold cyan]The list of audio files in current directory[/]", "-", 84)

        try:
            global Music_list, Music_number
            Music_list = []
            Music_number = 0
            Music_format = ["mp3", "wav", "flac", "aac", "m4a", "wma", "ogg"]

            for file in os.listdir():
                if file.split(".")[-1] in Music_format:
                    Music_list.append(file)
                    Music_number += 1

            Music_list.sort(key=lambda x: x.split(".")[-1])

            table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
            table.add_column("Number", style="cyan", justify="center")
            table.add_column("File Name", style="cyan", justify="center")
            table.add_column("File Size", style="cyan", justify="center")
            for i in range(len(Music_list)):
                table.add_row(
                    "(" + str(i + 1) + ")",
                    Music_list[i],
                    str(Convert_size(os.path.getsize(Music_list[i]))),
                )
            console.print(table)

            console.print(
                "\n[bold cyan]Total number of music files:[/] [bold #10b4eb]{}[/]\n".format(
                    Music_number
                )
            )
        except:
            console.print(
                "\n[bold #00ffa2]There is no audio file in the current directory![/]\n"
            )
        Choice()

    # Enter the number of audio file to convert
    def Choice():
        Lines("", "-", 70)
        # Music_path = audio file path
        # Music_name = audio file name
        # Music_extension = audio file extension
        global Music_path, Music_name, Music_extension
        Music_path = ""
        Music_name = ""
        Music_extension = ""

        Music_path = Input_ask(
            "\n[bold #ebcc36]Please enter the number of audio file to convert[/]",
            "Check_File-Name",
            True,
        ).Reply

        try:
            Music_name = Music_list[
                int(Music_path) - 1
            ]  # Because the index of the list starts from 0, so we need to minus 1
            Music_path = os.path.abspath(Music_name)
        except:
            Music_name = os.path.basename(Music_path)
            Music_path = os.path.abspath(Music_path)
        Music_extension = Music_name.split(".")[1]

        console.print(
            "\nThe audio file of choice: [bold deep_sky_blue3]{}[/]\n".format(
                Music_name
            )
        )
        Ask_Name()

    # Enter the converted file name
    def Ask_Name():
        Lines("", "-", 70)
        global Ask_name
        Ask_name = ""

        Ask_name = Input_ask(
            "\nPlease enter the name of the converted audio file [bold #ff7300](Press Enter to use the original file name)[/]",
            "Check_File-Format",
            True,
        ).Reply

        if Ask_name == "":
            Ask_name = Music_name.split(".")[0]

        console.print(
            "\nThe name of the converted audio file: [bold deep_sky_blue3]{}[/]\n".format(
                Ask_name
            )
        )
        Choice_Audio()

    # Choose the audio format
    def Choice_Audio():
        Lines("", "-", 70)

        # Target_audio = Select audio format
        # Target_file_name = Full name of the file after conversion
        global Target_audio, Target_file_name
        Target_audio = ""
        Target_file_name = ""

        questions = [
            {
                "type": "list",
                "name": "Choice_Audio",
                "message": "Please select the converted audio format:",
                "choices": ["MP3", "WAV", "AAC", "FLAC", "M4A", "OGG", "WMA"],
                "filter": lambda val: val.lower(),
            }
        ]
        Target_audio = prompt(questions, style=custom_style_1)
        Target_audio = Target_audio.get("Choice_Audio")
        Target_file_name = Ask_name + "." + Target_audio

        console.print(
            "\nThe converted audio file: [bold deep_sky_blue3]{}[/]\n".format(
                Target_file_name
            )
        )
        Ask_Path()

    # Enter the path of the converted file
    def Ask_Path():
        Lines("", "-", 70)

        # Ask_path = The audio file location after conversion
        # Target_file_path = The full path of the converted file
        global Ask_path, Target_file_path
        Ask_path = ""
        Target_file_path = ""

        Ask_path = Input_ask(
            "\nPlease enter the location of the converted audio file [bold #ff7300](Press Enter to use the current position)[/]",
            "Check_File-Path",
            True,
        ).Reply
        Ask_path = os.path.abspath(Ask_path)
        Target_file_path = os.path.join(Ask_path, Target_file_name)

        console.print(
            "\n\n\nThe location of the converted audio file: [bold deep_sky_blue3]{}[/]\n".format(
                Ask_path
            )
        )
        Ask_Convert()

    # Ask whether to start the conversion
    def Ask_Convert():
        Lines("[bold cyan]Conversion Process[/]", "-", 84)

        console.print(
            "\nThe choose file path:\n[bold deep_sky_blue3]{}[/]\n".format(
                os.path.dirname(Music_path)
            )
        )
        console.print(
            "The Converted file path:\n[bold deep_sky_blue3]{}[/]\n".format(Ask_path)
        )

        table = Table(show_header=True, header_style="bold green", box=box.DOUBLE_EDGE)
        table.add_column("The choose file", style="cyan", justify="center")
        table.add_column("The converted file", style="cyan", justify="center")
        table.add_row(Music_name, Target_file_name)
        console.print(table)

        Ask = Input_ask(
            "\n[bold #ebcc36]Do you want to convert the file?[/]", "Check_Ask", True
        ).Reply
        if Ask == True:
            Audio_Convert()
        elif Ask == False:
            console.print("\n\n[bold #00ffa2]The conversion is cancelled![/]\n")
            Clear()
            ShowList()

    # Start the conversion
    def Audio_Convert():
        print("\n\n")
        Lines("", "-", 70)
        if Music_extension == Target_audio:
            Ask2 = Input_ask(
                "[bold #ebcc36]\nThe file is the same format as the target format,Do you want to convert it [Y/N] [/]",
                "Check_Ask",
                True,
            ).Reply
            if Ask2 == True:
                pass
            elif Ask2 == False:
                print("\n\n")
                Ask_End()

        try:
            print("\n")
            console.print("\n[bold red]Converting...[/]\n")
            ffmpeg()
        except Exception as e:
            print(e)
            console.print("\n\n[bold red]Conversion failed![/]\n")
            sys.exit(0)

        Times = Decimal((Total_Time)).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        print("\n")
        Lines("", "-", 70)

        console.print(
            "\nConversion completed! Processing time is:[bold #10b4eb]{} seconds[/][bold red] (Estimated time is not accurate)[/]\n".format(
                Times
            )
        )
        Ask_End()

    # Conversion processing main program
    def ffmpeg():
        global Total_Time
        Total_Time = 0

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
            start = time.perf_counter()
            os.system(
                Audio_format[Target_audio].format(
                    "ffmpeg -i", Music_path, Target_file_path
                )
            )
            end = time.perf_counter()
        Total_Time = end - start

    # Ask whether to continue to convert
    def Ask_End():
        Lines("", "-", 70)
        Ask3 = Input_ask(
            "\n[bold #ebcc36]Do you want to convert another file? [Y/N] [/]",
            "Check_Ask",
            True,
        ).Reply
        if Ask3 == True:
            Clear()
            ShowList()
        elif Ask3 == False:
            print("\n")
            console.print("\n[bold #81eb36]Conversion completed![/]\n")
            Stop()
            sys.exit()

    if __name__ == "__main__":
        ShowList()


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
            Custom.Re_Err_B()
            print("\n\n")
            console.print("\n[bold red]已中斷程序![/]\n")
            sys.exit(0)
        except Exception as e:
            print(e)
            print("\n")
            console.print("\n[bold red]發生錯誤![/]\n")
            sys.exit(0)
    elif language == "English":
        try:
            English()
        except KeyboardInterrupt:
            Custom.Re_Err_B()
            print("\n\n")
            console.print("\n[bold red]Program has been interrupted by user![/]\n")
            sys.exit(0)
        except Exception as e:
            print(e)
            print("\n")
            console.print("\n[bold red]Error![/]\n")
            sys.exit(0)


if __name__ == "__main__":
    try:
        Ask_language()
    except Exception:
        console.print("\n\n[bold red]已中斷程序! Operation cancelled![/]\n")
        sys.exit()
