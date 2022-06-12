# -*- coding: utf-8 -*-
import os
from rich.console import Console

console = Console()

def Clear():
    os.system("cls" if os.name in ("nt", "dos") else "clear")


def Stop():
    console.print("\n[bold #ff7300]請按任意鍵離開...[/]")
    os.system("pause >nul 2>&1")