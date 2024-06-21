import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import subprocess
import os
from datetime import datetime
from tkcalendar import DateEntry

script_dir = os.path.dirname(os.path.abspath(__file__))
game1_path = os.path.join(script_dir, 'game_1.py')
game2_path = os.path.join(script_dir, 'game_2.py')

#main class of app
class MyToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MyToDo App")
        self.geometry("600x800")
        self.iconbitmap("icon.ico")

        self.conn = sqlite3.connect("tasks.db")
        self.create_table()
        self.alter_table()

        # startup window
        startup_window = tk.Toplevel(self)
        startup_window.title("Welcome")
        startup_window.geometry("600x250")
        startup_window.iconbitmap("icon.ico")

        # Startup message
        startup_label = ttk.Label(startup_window, text="Welcome to MyToDo App!", font=("TkDefaultFont", 20))
        startup_label.pack(pady=10)

        # User notes
        side_notes = [
            "You can add tasks by typing in the input box and clicking the 'Add' button.",
            "To mark a task as done, select it from the list and click the 'Done' button.",
            "To delete a task, select it from the list and click the 'Delete' button.",
            "Click the 'View Stats' button to see task statistics.",
            "Reward yourself with some fun minigames as you finished your tasks!",
            "Note:", 
            "Once you've done 5 tasks, you can unlock the Car Game. 10 tasks, you can unlock the TeqBall Simulator"
        ]

        for note in side_notes:
            note_label = ttk.Label(startup_window, text=note)
            note_label.pack()

        #input box & placeholder
        self.task_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)
        self.task_input.insert(0, "Enter your to-do-task here ...")

        #event clear placeholder when input clicked
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        #event restore placeholder when input lose focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)
        
        #input box date & time due frame
        date_time_frame = ttk.Frame(self)
        date_time_frame.pack(pady=10)

        due_date_label = ttk.Label(date_time_frame, text="Due Date:", font=("TkDefaultFont", 14))
        due_date_label.grid(row=0, column=0, padx=10)
        due_time_label = ttk.Label(date_time_frame, text="Due Time:", font=("TkDefaultFont", 14))
        due_time_label.grid(row=0, column=1, padx=10)

        self.due_date_input = DateEntry(date_time_frame, font=("TkDefaultFont", 12), width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="dd-mm-yyyy")
        self.due_date_input.grid(row=1, column=0, padx=10)

        time_frame = ttk.Frame(date_time_frame)
        time_frame.grid(row=1, column=1, padx=10)
        
        self.hours_input = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=3, font=("TkDefaultFont", 12))
        self.hours_input.set("00")
        self.hours_input.pack(side=tk.LEFT)

        ttk.Label(time_frame, text=":", font=("TkDefaultFont", 12)).pack(side=tk.LEFT)
        
        self.minutes_input = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=3, font=("TkDefaultFont", 12))
        self.minutes_input.set("00")
        self.minutes_input.pack(side=tk.LEFT)
        
        #addingtask button
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        #listbox display added tasks
        self.task_list = tk.Listbox(self, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.BROWSE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #marking tasks as done/deleting/editing button
        ttk.Button(self, text="Done", style="success.TButton",
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Edit", style="warning.TButton",
                   command=self.edit_task).pack(side=tk.LEFT, padx=10, pady=10)
        
        #task stats display button
        ttk.Button(self, text="View Stats", style="info.TButton",
                   command=self.view_stats).pack(side=tk.RIGHT, padx=10, pady=10)
        
        #create menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        #create menu
        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="☰", menu=app_menu)

        #menu items
        app_menu.add_command(label="Race Car", command=self.game1__init__)
        app_menu.add_command(label="TeqBall Simulator", command=self.game2__init__)
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.quit)
        

        self.load_tasks()
    
    #func create_table
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                text TEXT,
                color TEXT,
                due_date TEXT,
                due_time
            )
        ''')
        self.conn.commit()

    #func alter_table
    def alter_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            PRAGMA table_info(tasks)
        ''')
        columns = [info[1] for info in cursor.fetchall()]
        if 'due_date' not in columns:
            cursor.execute('''
                ALTER TABLE tasks ADD COLUMN due_date TEXT
            ''')
        if 'due_time' not in columns:
            cursor.execute('''
                ALTER TABLE tasks ADD COLUMN due_time TEXT
            ''')
        self.conn.commit()

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
        due_date = self.due_date_input.get_date().strftime("%d-%m-%Y")
        due_time = f"{self.hours_input.get()}:{self.minutes_input.get()}"
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
            datetime.strptime(due_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date or Time", "The date format should be dd-mm-yyyy and time format should be HH:MM.")
            return
        
        if task != "Enter your to-do-task here ...":
            self.task_list.insert(tk.END, f"{task} (Due: {due_date} {due_time})")
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

    #func edit_task from task list
    def edit_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            task_index = task_index[0]
            old_task = self.task_list.get(task_index)
            old_task_text, old_due_info = old_task.rsplit(" (Due: ", 1)
            old_due_date, old_due_time = old_due_info.rsplit(" ", 1)
            old_due_time = old_due_time[:-1]
            new_task_text = simpledialog.askstring("Edit Task", "Edit your Task", initialvalue=old_task_text)
            new_due_date = simpledialog.askstring("Edit Due Date", "Edit Due Date (dd-mm-yyyy)", initialvalue=old_due_date)
            new_due_time = simpledialog.askstring("Edit Due Time", "Edit Due Time (HH:MM)", initialvalue=old_due_time)
            if new_task_text and new_due_date and new_due_time:
                try:
                    datetime.strptime(new_due_date, "%d-%m-%Y")
                    datetime.strptime(new_due_time, "%H:%M")
                except ValueError:
                    messagebox.showerror("Invalid Date or Time", "The date format should be dd-mm-yyyy and time format should be HH:MM.")
                    return
                self.task_list.delete(task_index)
                self.task_list.insert(task_index, f"{new_task_text} (Due: {new_due_date} {new_due_time})")
                self.task_list.itemconfig(task_index, fg= "orange")
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

    #func load_tasks
    def load_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT text, color, due_date, due_time FROM tasks")
        rows = cursor.fetchall()
        for row in rows:
            task_text = f"{row[0]} (Due: {row[2]} {row[3]})"
            self.task_list.insert(tk.END, task_text)
            self.task_list.itemconfig(tk.END, fg=row[1])
    
    #func save_tasks, saves task into tasks.json
    def save_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks")
        for i in range(self.task_list.size()):
            full_task = self.task_list.get(i)
            text, due_info = full_task.rsplit(" (Due: ", 1)
            due_date, due_time = due_info.split(" ", 1)
            due_time = due_time[:-1]
            color = self.task_list.itemcget(i, "fg")
            cursor.execute("INSERT INTO tasks (text, color, due_date, due_time) VALUES (?, ?, ?, ?)", (text, color, due_date, due_time))
        self.conn.commit()

if __name__ == '__main__':
    app = MyToDoApp()
    app.mainloop()