import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        form_frame = ttk.LabelFrame(self, text="Добавить пользователя")
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="Роль:").grid(row=2, column=0, sticky="w")
        self.role_entry = ttk.Entry(form_frame, width=15)
        self.role_entry.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Email", "Role"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Имя")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Role", text="Роль")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(self, text="Удалить выбранное", command=self.delete_selected).pack(pady=5)

    def refresh_users(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = self.user_controller.get_all_users()
        for u in users:
            self.tree.insert("", "end", values=(u.id, u.username, u.email, u.role))

    def add_user(self) -> None:
        username = self.username_entry.get()
        email = self.email_entry.get()
        role = self.role_entry.get() or "developer"
        self.user_controller.add_user(username, email, role)
        self.refresh_users()

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        for item in selected:
            user_id = self.tree.item(item)["values"][0]
            self.user_controller.delete_user(user_id)
        self.refresh_users()
