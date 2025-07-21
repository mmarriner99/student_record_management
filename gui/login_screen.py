# gui/login_screen.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from gui.main_screen import MainScreen

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Student Management")
        self.root.geometry("300x200")

        self.username_var = tb.StringVar()
        self.password_var = tb.StringVar()

        tb.Label(root, text="Username").pack(pady=(20, 5))
        tb.Entry(root, textvariable=self.username_var, width=25).pack()

        tb.Label(root, text="Password").pack(pady=5)
        tb.Entry(root, textvariable=self.password_var, width=25, show="*").pack()

        tb.Button(root, text="Login", bootstyle=PRIMARY, command=self.authenticate).pack(pady=15)

    def authenticate(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "admin" and password == "password":
            self.root.destroy()
            new_root = tb.Window(themename="darkly")
            MainScreen(new_root)
            new_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
