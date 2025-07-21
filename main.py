# main.py

import tkinter as tk
from gui.login_screen import LoginScreen
from utils.db_init import initialize_database

def main():
    # Ensure the database and tables are set up
    initialize_database()

    # Launch the login screen
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
