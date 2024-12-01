import tkinter as tk
from tkinter import messagebox

def add_task():
    task = task_entry.get().strip()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

def clear_all_tasks():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?"):
        task_listbox.delete(0, tk.END)

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

# Start the application
app.mainloop()
