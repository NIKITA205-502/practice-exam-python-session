import tkinter as tk
from tkinter import ttk, messagebox

class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Добавить проект")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_project).grid(row=2, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Название")
        self.tree.heading("Status", text="Статус")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

    def refresh_projects(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        projects = self.project_controller.get_all_projects()
        for p in projects:
            self.tree.insert("", "end", values=(p.id, p.name, p.status))

    def add_project(self) -> None:
        name = self.name_entry.get()
        description = self.desc_entry.get()
        from datetime import datetime, timedelta
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=30)
        self.project_controller.add_project(name, description, start_date, end_date)
        self.refresh_projects()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        for item in selected:
            project_id = self.tree.item(item)["values"][0]
            self.project_controller.delete_project(project_id)
        self.refresh_projects()
