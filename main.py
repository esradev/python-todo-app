import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
DB_NAME = "todo.db"

def setup_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """)
    load_tasks()

def add_task():
    task = task_entry.get().strip()
    if task:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = task_listbox.get(selected_task_index)
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

def clear_all_tasks():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?"):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
        task_listbox.delete(0, tk.END)

def load_tasks():
    task_listbox.delete(0, tk.END)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task FROM tasks")
        tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, task[0])

# Create main application window
app = tk.Tk()
app.title("To-Do List")
app.geometry("400x400")

# Task input frame
input_frame = tk.Frame(app)
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30)
task_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

# Task list display
task_listbox = tk.Listbox(app, width=50, height=15)
task_listbox.pack(pady=10)

# Action buttons frame
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task)
remove_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all_tasks)
clear_button.pack(side=tk.LEFT)

# Initialize database and load tasks
setup_database()

# Start the application
app.mainloop()
