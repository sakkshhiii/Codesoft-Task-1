import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Task class
class Task:
    def __init__(self, title, description, due_date, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data['title'], data['description'], data['due_date'], data['completed'])

# To-Do list manager
class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()

# GUI Application
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x400")

        self.todo = ToDoList()

        # Entry widgets
        tk.Label(root, text="Title:").grid(row=0, column=0, sticky="w", padx=5)
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(root, text="Description:").grid(row=1, column=0, sticky="w", padx=5)
        self.desc_entry = tk.Entry(root, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5)

        tk.Label(root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5)
        self.due_entry = tk.Entry(root, width=30)
        self.due_entry.grid(row=2, column=1, padx=5)

        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=3, column=0, pady=10)
        tk.Button(root, text="Mark Complete", command=self.mark_complete).grid(row=3, column=1)
        tk.Button(root, text="Delete Task", command=self.delete_task).grid(row=3, column=2)

        # Task list
        self.task_listbox = tk.Listbox(root, width=80, height=12)
        self.task_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.update_listbox()

    def add_task(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        due = self.due_entry.get().strip()

        if not title:
            messagebox.showerror("Missing Title", "Title is required.")
            return

        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
            return

        task = Task(title, desc, due)
        self.todo.add_task(task)
        self.update_listbox()

        # Clear entries
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.todo.tasks):
            status = "✓" if task.completed else "✗"
            line = f"{i + 1}. [{status}] {task.title} (Due: {task.due_date}) - {task.description}"
            self.task_listbox.insert(tk.END, line)

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo.delete_task(index)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def mark_complete(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.todo.complete_task(index)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to mark as complete.")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

