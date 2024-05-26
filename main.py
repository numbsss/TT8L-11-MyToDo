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
        self.task_input = ttk.Entry(self, font=(
            "TkDefaultFont",16), width=30,style="Custon.TEntry")
        self.task_input.pack(pady=10)

        #input box placeholder
        self.task_input.insert(0,"Enter your to-do here ...")

        #event clear placeholder when input clicked
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        #event restore placeholder when input lose focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        #addingtask button
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        #listbox display added tasks
        self.task_list = tk.Listbox(self, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #marking tasks as done/deleting button
        ttk.Button(self,text="Done", style="success.TButton",
                   command=self.mark_done).pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)
        
        #task stats display button
        ttk.Button(self, text="View Stats", style="info.TButton",
                   command=self.view_stats).pack(side=tk.BOTTOM, pady=10)
        
        self.load_tasks()

    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")
    
    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your to-do here ...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()