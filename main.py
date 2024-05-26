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

        