import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from ttkbootstrap import Style
import json
class MyToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MyToDo App")
        self.geometry("400x600")
        style = Style(theme='flatly')
        style.configure("Custon.TEntry", foreground="gray")

        #input box
        self.tas_input = ttk.Entry(self, font=(
            "TkDefaultFont",16), width=30,style="Custon.TEntry")
        self.task_input.pack(pady=10)

        #input box placeholder
        self.task_input.insert(0,"What's your task today?")
