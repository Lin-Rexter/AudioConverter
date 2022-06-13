# -*- coding: utf-8 -*-
import sys
from rich.console import Console

console = Console()

class ANSI_EC:
    def __init__(self, x):
        self.x = x

    def Move_Top(self):
        sys.stdout.write("\x1B[{}A".format(self.x))

    def Move_Down(self):
        sys.stdout.write("\x1B[{}B".format(self.x))

    def Move_Right(self):
        sys.stdout.write("\x1B[{}C".format(self.x))

    def Move_Left(self):
        sys.stdout.write("\x1B[{}D".format(self.x))

    def Clear_A(self):
        sys.stderr.write("\x1B[{}K".format(self.x))

    def Clear_B(self):
        sys.stderr.write("\x1B[{}J".format(self.x))

    def Err_Flush():
        sys.stderr.flush()

    def Out_Flush():
        sys.stdout.flush()
    
    def Clear_Color():
        sys.stderr.write("\033[0m")

    def Err_Red(self):
        console.print("\n" + self.x, style="bold red")
        sys.stdout.write("\x1B[{}A".format(2))


# 自定義功能(組合功能)
class Custom:
    def Show_Err(x):
        ANSI_EC(x).Err_Red()

    def Re_Cursor_A():
        ANSI_EC(3).Move_Top()
        ANSI_EC(0).Clear_A()

    def Re_Cursor_B():
        ANSI_EC(2).Move_Top()
        ANSI_EC(0).Clear_A()
    
    def Re_Err_A():
        ANSI_EC(2).Move_Down()
        ANSI_EC(0).Clear_A()
        ANSI_EC(2).Move_Top()

    def Re_Err_B():
        ANSI_EC(2).Move_Down()
        ANSI_EC(0).Clear_B()
        ANSI_EC.Err_Flush()
        ANSI_EC(2).Move_Top()