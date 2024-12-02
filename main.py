import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Database setup
DB_NAME = "todo.db"


def setup_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)
    add_completed_column()  # Ensure the 'completed' column exists
    load_tasks()


def add_completed_column():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")  # Get the columns in the table
        columns = [column[1] for column in cursor.fetchall()]
        if 'completed' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")
            print("Completed column added successfully.")


def add_task():
    task = task_entry.get().strip()
    if task:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
            task_id = cursor.lastrowid  # Get the ID of the newly inserted task
        task_listbox.insert(tk.END, task)
        task_ids.append(task_id)  # Add the new task ID to the list
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def add_task_from_input(event=None):
    task = task_entry.get().strip()  # Get the text from the input field
    if task:  # Ensure the input is not empty
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))  # Add task to database
            task_id = cursor.lastrowid  # Get the ID of the newly inserted task
            conn.commit()

        # Update the listbox with the new task
        task_listbox.insert(tk.END, task)
        task_ids.append(task_id)  # Add the new task ID to the list
        task_entry.delete(0, tk.END)  # Clear the input field
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_ids[selected_task_index[0]]
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        task_listbox.delete(selected_task_index)
        task_ids.pop(selected_task_index[0])
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")


def clear_all_tasks():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?"):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
        task_listbox.delete(0, tk.END)
        task_ids.clear()


def load_tasks():
    task_listbox.delete(0, tk.END)
    task_ids.clear()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, completed FROM tasks")
        tasks = cursor.fetchall()
    for task_id, task, completed in tasks:
        task_ids.append(task_id)
        display_task = f"[✔] {task}" if completed else task
        task_listbox.insert(tk.END, display_task)


def mark_as_completed():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_ids[selected_task_index[0]]
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        task = task_listbox.get(selected_task_index)
        # Check if the task is already marked as completed
        if "[✔]" in task:
            return

        task_listbox.delete(selected_task_index)
        task_listbox.insert(selected_task_index, f"[✔] {task}")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")


def mark_as_incomplete():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_ids[selected_task_index[0]]
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (task_id,))

        # Check if the task is already marked as incomplete
        task = task_listbox.get(selected_task_index)
        if "[✔]" not in task:
            return

        # Get the current task and update it
        task_listbox.delete(selected_task_index)
        task_listbox.insert(selected_task_index, task.replace("[✔] ", ""))
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as incomplete.")


def edit_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_id = task_ids[selected_task_index[0]]
        current_task = task_listbox.get(selected_task_index).replace("[✔] ", "").strip()

        # Prompt for new task name
        new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task)
        if new_task and new_task.strip():
            new_task = new_task.strip()
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index, f"[✔] {new_task}" if "[✔]" in current_task else new_task)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")


# Create main application window
app = tk.Tk()
app.title("To-Do List")
app.geometry("600x500")
app.config(bg="#f4f4f9")  # Set background color

task_ids = []

# Task input frame
input_frame = tk.Frame(app, bg="#f4f4f9")
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30, font=("Arial", 14), bd=2, relief="solid", highlightthickness=2,
                      highlightbackground="#0078d4")
task_entry.pack(side=tk.LEFT, padx=10)

add_button = tk.Button(input_frame, text="Add Task", command=add_task, bg="#0078d4", fg="white",
                       font=("Arial", 12, "bold"), relief="flat", width=12)
add_button.pack(side=tk.LEFT, padx=5)

# Binding the Enter key to the task-adding function
task_entry.bind("<Return>", add_task_from_input)


# Task list display
task_listbox = tk.Listbox(app, width=50, height=15, font=("Arial", 12), bd=0, bg="#fff", selectbackground="#6ba5ff",
                          selectforeground="black")
task_listbox.pack(pady=10)

# Action buttons frame
button_frame = tk.Frame(app, bg="#f4f4f9")
button_frame.pack(pady=10)

edit_button = tk.Button(button_frame, text="Edit", command=edit_task, bg="#f0ad4e", fg="white", font=("Arial", 12), relief="flat", width=12)
edit_button.pack(side=tk.LEFT, padx=5)

mark_button = tk.Button(button_frame, text="Completed", command=mark_as_completed, bg="#5bc0de", fg="white", font=("Arial", 12), relief="flat", width=12)
mark_button.pack(side=tk.LEFT, padx=5)

unmark_button = tk.Button(button_frame, text="Incomplete", command=mark_as_incomplete, bg="#d9534f", fg="white", font=("Arial", 12), relief="flat", width=12)
unmark_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(button_frame, text="Remove", command=remove_task, bg="#d9534f", fg="white", font=("Arial", 12), relief="flat", width=12)
remove_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all_tasks, bg="#d9534f", fg="white", font=("Arial", 12), relief="flat", width=12)
clear_button.pack(side=tk.LEFT, padx=5)


# Initialize database and load tasks
setup_database()

# Start the application
app.mainloop()
