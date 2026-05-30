# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("800x600")

        self.task_controller = book_controller
        self.project_controller = reader_controller
        self.user_controller = loan_controller

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        task_view = TaskView(notebook, self.task_controller, self.project_controller, self.user_controller)
        notebook.add(task_view, text="Задачи")

        project_view = ProjectView(notebook, self.project_controller)
        notebook.add(project_view, text="Проекты")

        user_view = UserView(notebook, self.user_controller)
        notebook.add(user_view, text="Пользователи")
