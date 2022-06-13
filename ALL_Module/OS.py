# -*- coding: utf-8 -*-
import os
from rich.console import Console

console = Console()

def Clear():
    os.system("cls" if os.name in ("nt", "dos") else "clear")


def Stop():
    console.print("\n[bold #ff7300]請按任意鍵離開...[/]")
    os.system("pause >nul 2>&1")

def Window(mode):
    if mode == "full":
        os.system("mode con cols=135 lines=45")
    elif mode == "medium":
        os.system("mode con cols=100 lines=30")
    elif mode == "small":
        os.system("mode con cols=80 lines=25")
