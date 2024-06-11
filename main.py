import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage
from ttkbootstrap import Style
import json
import subprocess
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
game1_path = os.path.join(script_dir, 'game_1.py')
game2_path = os.path.join(script_dir, 'game_2.py')

#main class of app
class MyToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MyToDo App")
        self.geometry("400x500")
        style = Style(theme="flatly")
        style.configure("Custom.TEntry", foreground="gray")

        #input box
        self.task_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)

        #input box placeholder
        self.task_input.insert(0, "Enter your to-do-task here ...")

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
        ttk.Button(self, text="Done", style="success.TButton",
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)
        
        #task stats display button
        ttk.Button(self, text="View Stats", style="info.TButton",
                   command=self.view_stats).pack(side=tk.BOTTOM, pady=10)
        
        #create menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        #create menu
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="☰", menu=app_menu)

        #menu items
        app_menu.add_command(label="game1", command=self.game1__init__)
        app_menu.add_command(label="game2", command=self.game2__init__)
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.quit)
        

        self.load_tasks()
    
    #func game1__init__
    def game1__init__(self):
        done_count = sum(1 for i in range(self.task_list.size()) if self.task_list.itemcget(i, "fg") == "green")
        if done_count >= 5:
            subprocess.Popen(["python",game1_path])
        else:
            messagebox.showinfo("Alert","You have to finish minimum of 5 tasks to unlock this game!")
        #when done tasks >=5 can play game 
    
    #func game2__init__
    def game2__init__(self):
        done_count = sum(1 for i in range(self.task_list.size()) if self.task_list.itemcget(i, "fg") == "green")
        if done_count >= 10:
            subprocess.Popen(["python",game2_path])
        else:
            messagebox.showinfo("Alert","You have to finish minimum of 10 tasks to unlock this game!")
        #will be added once game 2 finished
        

    #func view_stats using json file
    def view_stats(self):
        done_count = sum(1 for i in range(self.task_list.size()) if self.task_list.itemcget(i,"fg")=="green")
        total_count = self.task_list.size()
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    #func add_task
    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your to-do-task here ...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    #func mark_done from task list
    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()
    
    #func delete_task from task list
    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()
    
    #func clear_placeholder, cleared box when clicked
    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter your to-do-task here ...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    #func restore_placeholder, restore box to inital when put blank
    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your to-do-task here ...")
            self.task_input.configure(style="Custom.TEntry")

    #func load_tasks, gain saved data from tasks.json to be displayed
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass
    
    #func save_tasks, saves task into tasks.json
    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

if __name__ == '__main__':
    app = MyToDoApp()
    app.mainloop()