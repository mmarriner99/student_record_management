# utils/db_init.py

import sqlite3
import os

def initialize_database():
    db_path = "db/database.db"
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the students table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()
