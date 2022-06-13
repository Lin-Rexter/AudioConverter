# -*- coding: utf-8 -*-
from rich.console import Console

console = Console()

def Lines(Message,Symbols,Quantity):
    console.print("{:{}^{}}".format(Message,Symbols,Quantity))