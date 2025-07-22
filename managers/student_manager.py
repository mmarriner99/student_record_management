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
            # Ensure contact is stored as string with leading zero
            contact = self._normalize_phone_number(contact)
            
            student = Student(name, contact, roll)
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if roll number already exists
            cursor.execute("SELECT id FROM students WHERE roll_number = ?", (roll,))
            if cursor.fetchone():
                conn.close()
                return False, "Roll number already exists"
            
            cursor.execute("INSERT INTO students (name, contact, roll_number) VALUES (?, ?, ?)",
                           student.to_db_tuple())
            conn.commit()
            conn.close()
            return True, "Student added successfully"
        except sqlite3.IntegrityError:
            return False, "Roll number must be unique"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def update_student(self, student_id, name, contact, roll):
        try:
            # Ensure contact is stored as string with leading zero
            contact = self._normalize_phone_number(contact)
            
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if roll number exists for a different student
            cursor.execute("SELECT id FROM students WHERE roll_number = ? AND id != ?", (roll, student_id))
            if cursor.fetchone():
                conn.close()
                return False, "Roll number already exists for another student"
            
            cursor.execute("""
                UPDATE students SET name = ?, contact = ?, roll_number = ?
                WHERE id = ?
            """, (name, contact, roll, student_id))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Student not found"
                
            conn.commit()
            conn.close()
            return True, "Student updated successfully"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def delete_student(self, student_id):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Student not found"
                
            conn.commit()
            conn.close()
            return True, "Student deleted successfully"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def get_all_students(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY name")
            rows = cursor.fetchall()
            conn.close()
            
            # Ensure phone numbers are properly formatted
            formatted_rows = []
            for row in rows:
                student_id, name, contact, roll = row
                contact = self._normalize_phone_number(str(contact))
                formatted_rows.append((student_id, name, contact, roll))
            
            return formatted_rows
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []

    def search_students(self, keyword):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM students
                WHERE name LIKE ? OR contact LIKE ? OR roll_number LIKE ?
                ORDER BY name
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            rows = cursor.fetchall()
            conn.close()
            
            # Ensure phone numbers are properly formatted
            formatted_rows = []
            for row in rows:
                student_id, name, contact, roll = row
                contact = self._normalize_phone_number(str(contact))
                formatted_rows.append((student_id, name, contact, roll))
            
            return formatted_rows
        except Exception as e:
            print(f"Error searching students: {e}")
            return []

    def export_to_csv(self, filepath):
        try:
            students = self.get_all_students()
            with open(filepath, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Contact", "Roll Number"])
                writer.writerows(students)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False

    def get_student_by_id(self, student_id):
        """Get a single student by ID"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                student_id, name, contact, roll = row
                contact = self._normalize_phone_number(str(contact))
                return (student_id, name, contact, roll)
            return None
        except Exception as e:
            print(f"Error fetching student: {e}")
            return None

    def _normalize_phone_number(self, phone):
        """Ensure phone number starts with 0 and is properly formatted"""
        phone = str(phone).strip()
        
        # Remove any non-digit characters except leading +
        if phone.startswith('+44'):
            # Convert +44 format to UK format
            phone = phone.replace('+44', '0', 1)
            phone = ''.join(filter(str.isdigit, phone))
        else:
            phone = ''.join(filter(str.isdigit, phone))
        
        # Ensure it starts with 0 if it's a UK number
        if phone and not phone.startswith('0') and len(phone) in [10, 11]:
            phone = '0' + phone
        
        return phone

    def validate_unique_roll(self, roll_number, exclude_id=None):
        """Check if roll number is unique"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            if exclude_id:
                cursor.execute("SELECT id FROM students WHERE roll_number = ? AND id != ?", 
                             (roll_number, exclude_id))
            else:
                cursor.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number,))
            
            result = cursor.fetchone()
            conn.close()
            return result is None
        except Exception as e:
            print(f"Error validating roll number: {e}")
            return False