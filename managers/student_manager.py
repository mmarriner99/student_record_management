# managers/student_manager.py

import sqlite3
import csv
from models.student import Student

class StudentManager:
    def __init__(self, db_path="db/database.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def add_student(self, name, contact, roll):
        try:
            student = Student(name, contact, roll)
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, contact, roll_number) VALUES (?, ?, ?)",
                           student.to_db_tuple())
            conn.commit()
            conn.close()
            return True, "Student added"
        except sqlite3.IntegrityError:
            return False, "Roll number must be unique"
        except Exception as e:
            return False, str(e)

    def update_student(self, student_id, name, contact, roll):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students SET name = ?, contact = ?, roll_number = ?
                WHERE id = ?
            """, (name, contact, roll, student_id))
            conn.commit()
            conn.close()
            return True, "Student updated"
        except Exception as e:
            return False, str(e)

    def delete_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

    def get_all_students(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def search_students(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR contact LIKE ? OR roll_number LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def export_to_csv(self, filepath):
        try:
            students = self.get_all_students()
            with open(filepath, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Contact", "Roll Number"])
                writer.writerows(students)
            return True
        except Exception as e:
            print("Export error:", e)
            return False
