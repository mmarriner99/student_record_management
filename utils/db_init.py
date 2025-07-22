# utils/db_init.py

import sqlite3
import os

def initialize_database():
    """Initialize database with proper text constraints for phone numbers"""
    db_path = "db/database.db"
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the students table with explicit TEXT constraint for contact
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL CHECK(length(name) >= 2 AND length(name) <= 50),
            contact TEXT NOT NULL CHECK(length(contact) >= 10 AND length(contact) <= 15),
            roll_number TEXT NOT NULL UNIQUE CHECK(length(roll_number) = 7)
        )
    ''')

    # Create indexes for better search performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_students_name ON students(name)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_students_roll ON students(roll_number)
    ''')

    conn.commit()
    
    # Check if we need to fix existing data with missing leading zeros
    cursor.execute("SELECT id, contact FROM students WHERE contact NOT LIKE '0%' AND length(contact) IN (10, 11)")
    rows_to_fix = cursor.fetchall()
    
    if rows_to_fix:
        print(f"Found {len(rows_to_fix)} phone numbers that may need leading zeros added...")
        for student_id, contact in rows_to_fix:
            # Add leading zero if the number looks like a UK number without it
            if len(contact) in [10, 11] and contact.isdigit():
                fixed_contact = '0' + contact
                cursor.execute("UPDATE students SET contact = ? WHERE id = ?", (fixed_contact, student_id))
                print(f"Fixed contact for student ID {student_id}: {contact} -> {fixed_contact}")
        
        conn.commit()
        print("Phone number fixes applied.")
    
    conn.close()
    print("Database initialized successfully.")

def backup_database():
    """Create a backup of the database"""
    import shutil
    from datetime import datetime
    
    db_path = "db/database.db"
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"db/database_backup_{timestamp}.db"
        shutil.copy2(db_path, backup_path)
        print(f"Database backed up to: {backup_path}")
        return backup_path
    return None