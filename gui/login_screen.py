# gui/login_screen.py

import tkinter as tk
from tkinter import messagebox
from gui.main_screen import MainScreen

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Login")
        self.root.geometry("300x180")

        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.authenticate)
        self.login_button.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Basic credentials (can be changed or moved to file later)
        if username == "admin" and password == "password":
            self.root.destroy()
            new_root = tk.Tk()
            MainScreen(new_root)
            new_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
