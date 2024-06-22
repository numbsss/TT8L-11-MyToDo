import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import subprocess
import os
from datetime import datetime, timedelta
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

        # app theme
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("TCombobox", font=("Helvetica", 12))

        self.create_widgets()

        self.load_tasks()
        self.check_reminders()
    
    #func create_widget
    def create_widgets(self):
        # startup window
        startup_window = tk.Toplevel(self)
        startup_window.title("Welcome")
        startup_window.geometry("600x250")
        startup_window.iconbitmap("icon.ico")

        # Startup message
        startup_label = ttk.Label(startup_window, text="Welcome to MyToDo App!", font=("Helvetica", 20))
        startup_label.pack(pady=10)

        # User notes
        side_notes = [
            "You can add tasks by typing in the input box and clicking the 'Add' button.",
            "To mark a task as done, select it from the list and click the 'Done' button.",
            "To delete a task, select it from the list and click the 'Delete' button.",
            "Click the 'View Stats' button to see task statistics.",
            "Reward yourself with some fun minigames as you finished your tasks!",
            "Note:", 
            "Once you've done 1 task, you can unlock the Car Game. 3 tasks, you can unlock the TeqBall Simulator"
        ]

        for note in side_notes:
            note_label = ttk.Label(startup_window, text=note)
            note_label.pack()

        #main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        #input box & placeholder
        self.task_input = ttk.Entry(main_frame, font=(
            "Helvetica", 16), width=30)
        self.task_input.pack(pady=10)
        self.task_input.insert(0, "Enter your to-do-task here ...")

        #event clear placeholder when input clicked
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        #event restore placeholder when input lose focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)
        
        #input box date & time due frame
        date_time_frame = ttk.Frame(main_frame)
        date_time_frame.pack(pady=10)

        due_date_label = ttk.Label(date_time_frame, text="Due Date:", font=("Helvetica", 14))
        due_date_label.grid(row=0, column=0, padx=10)
        due_time_label = ttk.Label(date_time_frame, text="Due Time:", font=("Helvetica", 14))
        due_time_label.grid(row=0, column=1, padx=10)

        self.due_date_input = DateEntry(date_time_frame, font=("Helvetica", 12), width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="dd-mm-yyyy")
        self.due_date_input.grid(row=1, column=0, padx=10)

        time_frame = ttk.Frame(date_time_frame)
        time_frame.grid(row=1, column=1, padx=10)
        
        self.hours_input = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=3, font=("Helvetica", 12))
        self.hours_input.set("00")
        self.hours_input.pack(side=tk.LEFT)

        ttk.Label(time_frame, text=":", font=("Helvetica", 12)).pack(side=tk.LEFT)
        
        self.minutes_input = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=3, font=("Helvetica", 12))
        self.minutes_input.set("00")
        self.minutes_input.pack(side=tk.LEFT)
        
        #addingtask button
        ttk.Button(main_frame, text="Add", command=self.add_task).pack(pady=5)

        #listbox display added tasks
        self.task_list = tk.Listbox(main_frame, font=(
            "Helvetica", 16), height=10, selectmode=tk.BROWSE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        #marking tasks as done/deleting/editing/view stats button
        ttk.Button(button_frame, text="Done", style="success.TButton",
                    command=self.mark_done).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Delete", style="danger.TButton",
                    command=self.delete_task).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Edit", style="warning.TButton",
                    command=self.edit_task).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="View Stats", style="info.TButton",
                    command=self.view_stats).pack(side=tk.RIGHT, padx=10)
        
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
    
    #func create_table
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                text TEXT,
                color TEXT,
                due_date TEXT,
                due_time TEXT
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
        if done_count >= 1:
            subprocess.Popen(["python", game1_path])
        else:
            messagebox.showinfo("Alert", "You have to finish minimum of 1 task to unlock this game!")
        #when done tasks >=5 can play game 
    
    #func game2__init__
    def game2__init__(self):
        done_count = sum(1 for i in range(self.task_list.size()) if self.task_list.itemcget(i, "fg") == "green")
        if done_count >= 3:
            subprocess.Popen(["python", game2_path])
        else:
            messagebox.showinfo("Alert", "You have to finish minimum of 3 tasks to unlock this game!")
        #will be added once game 2 finished
        
    #func view_stats
    def view_stats(self):
        done_count = sum(1 for i in range(self.task_list.size()) if self.task_list.itemcget(i, "fg") == "green")
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
            full_task = self.task_list.get(task_index)
            try:
                old_task_text, old_due_info = full_task.rsplit(" (Due: ", 1)
                old_due_date, old_due_time = old_due_info.rsplit(" ", 1)
                old_due_time = old_due_time[:-1]
            except:
                old_task_text = full_task
                old_due_date = datetime.now().strftimetime("%d-%m-%Y")
                old_due_time = "00:00"

            new_task_text = simpledialog.askstring("Edit Task", "Edit your Task", initialvalue=old_task_text)
            
            edit_due_date_popup = tk.Toplevel(self)
            edit_due_date_popup.title("Set your new Due Date")
            edit_due_date_popup.geometry("300x200")

            due_date_label = ttk.Label(edit_due_date_popup, text="Due Date:", font=("TkDefaultFont", 12))
            due_date_label.pack(pady=5)
            new_due_date = DateEntry(edit_due_date_popup, font=("TkDefaultFont", 12), date_pattern="dd-mm-yyyy")
            new_due_date.set_date(datetime.strptime(old_due_date, "%d-%m-%Y"))
            new_due_date.pack(pady=5)

            due_time_label = ttk.Label(edit_due_date_popup, text="Due Time:", font=("TkDefaultFont", 12))
            due_time_label.pack(pady=5)

            new_due_time_frame = ttk.Frame(edit_due_date_popup)
            new_due_time_frame.pack(pady=5)

            new_hours_input = ttk.Combobox(new_due_time_frame, values=[f"{i:02d}" for i in range(24)], width=3, font=("TkDefaultFont", 12))
            new_hours_input.set(old_due_time.split(":")[0])
            new_hours_input.pack(side=tk.LEFT)

            ttk.Label(new_due_time_frame, text=":", font=("TkDefaultFont", 12)).pack(side=tk.LEFT)

            new_minutes_input = ttk.Combobox(new_due_time_frame, values=[f"{i:02d}" for i in range(60)], width=3, font=("TkDefaultFont", 12))
            new_minutes_input.set(old_due_time.split(":")[1] if len(old_due_time.split(":")) > 1 else "00")
            new_minutes_input.pack(side=tk.LEFT)

            #func save_edit
            def save_edit():
                new_due_date_val = new_due_date.get_date().strftime("%d-%m-%Y")
                new_due_time_val = f"{new_hours_input.get()}:{new_minutes_input.get()}"
                try:
                    datetime.strptime(new_due_date_val, "%d-%m-%Y")
                    datetime.strptime(new_due_time_val, "%H:%M")
                except ValueError:
                    messagebox.showerror("Invalid Date or Time", "The date format should be dd-mm-yyyy and time format should be HH:MM.")
                    return
                if new_task_text and new_due_date_val and new_due_time_val:
                    self.task_list.delete(task_index)
                    self.task_list.insert(task_index, f"{new_task_text} (Due: {new_due_date_val} {new_due_time_val})")
                    self.task_list.itemconfig(task_index, fg="orange")
                    self.save_tasks()
                edit_due_date_popup.destroy()

            save_button = ttk.Button(edit_due_date_popup, text="Save", command=save_edit)
            save_button.pack(pady=10)
    
    #func clear_placeholder, cleared box when clicked
    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter your to-do-task here ...":
            self.task_input.delete(0, tk.END)
            self.task_input.config(foreground='black')

    #func restore_placeholder, restore box to inital when put blank
    def restore_placeholder(self, event):
        if not self.task_input.get():
            self.task_input.insert(0, "Enter your to-do-task here ...")
            self.task_input.config(foreground='grey')

    #func load_tasks
    def load_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT text, color, due_date, due_time FROM tasks")
        tasks = cursor.fetchall()
        for task in tasks:
            task_text, color, due_date, due_time = task
            self.task_list.insert(tk.END, f"{task_text} (Due: {due_date} {due_time})")
            self.task_list.itemconfig(tk.END, fg=color)
    
    #func save_tasks, saves task into tasks.json
    def save_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks")
        for i in range(self.task_list.size()):
            full_task = self.task_list.get(i)
            try:
                text, due_info = full_task.rsplit(" (Due: ", 1)
                due_date, due_time = due_info.split(" ", 1)
                due_time = due_time[:-1]
            except ValueError:
                text = full_task
                due_date = datetime.now().strftime("%d-%m-%Y")
                due_time = "00:00"
            color = self.task_list.itemcget(i, "fg")
            cursor.execute("INSERT INTO tasks (text, color, due_date, due_time) VALUES (?, ?, ?, ?)", (text, color, due_date, due_time))
        self.conn.commit()
    
    #func check_reminders, remind upcoming current tasks when app launched
    def check_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT text, color, due_date, due_time FROM tasks WHERE color = 'orange'")
        rows = cursor.fetchall()
        for row in rows:
            due_datetime_str = f"{row[2]} {row[3]}"
            due_datetime = datetime.strptime(due_datetime_str, "%d-%m-%Y %H:%M")
            now = datetime.now()
            time_difference = due_datetime - now
            
            if time_difference.total_seconds() < 0:
                message = f"Task '{row[0]}' is past due!"
            else:
                days_until_due = time_difference.days
                hours_until_due = time_difference.seconds // 3600
                minutes_until_due = (time_difference.seconds % 3600) // 60
                
                if days_until_due == 0:
                    if hours_until_due > 0 or minutes_until_due > 0:
                        message = f"Task '{row[0]}' is due in {hours_until_due} hours and {minutes_until_due} minutes!"
                    else:
                        message = f"Task '{row[0]}' is due very soon!"
                elif days_until_due == 1:
                    message = f"Task '{row[0]}' is due in 1 day!"
                else:
                    message = f"Task '{row[0]}' is due in {days_until_due} days and {hours_until_due} hours!"
            
            messagebox.showinfo("Task Reminder", message)

        self.after(3600000, self.check_reminders)

if __name__ == '__main__':
    app = MyToDoApp()
    app.mainloop()