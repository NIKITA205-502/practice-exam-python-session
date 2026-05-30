import tkinter as tk
from tkinter import ttk, messagebox

class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Добавить задачу")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="Приоритет (1-3):").grid(row=2, column=0, sticky="w")
        self.priority_entry = ttk.Entry(form_frame, width=5)
        self.priority_entry.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)

        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=5)
        ttk.Label(search_frame, text="Поиск:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Искать", command=self.refresh_tasks).pack(side="left")

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Status", "Priority"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Status", text="Статус")
        self.tree.heading("Priority", text="Приоритет")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

    def refresh_tasks(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = self.search_entry.get()
        if query:
            tasks = self.task_controller.search_tasks(query)
        else:
            tasks = self.task_controller.get_all_tasks()
        for t in tasks:
            self.tree.insert("", "end", values=(t.id, t.title, t.status, t.priority))

    def add_task(self) -> None:
        title = self.title_entry.get()
        description = self.desc_entry.get()
        try:
            priority = int(self.priority_entry.get())
        except ValueError:
            priority = 2
        from datetime import datetime, timedelta
        due_date = datetime.now() + timedelta(days=7)
        projects = self.project_controller.get_all_projects()
        project_id = projects[0].id if projects else 1
        users = self.user_controller.get_all_users()
        user_id = users[0].id if users else 1
        self.task_controller.add_task(title, description, priority, due_date, project_id, user_id)
        self.refresh_tasks()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        for item in selected:
            task_id = self.tree.item(item)["values"][0]
            self.task_controller.delete_task(task_id)
        self.refresh_tasks()
