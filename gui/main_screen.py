# gui/main_screen.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from managers.student_manager import StudentManager
from utils.helpers import validate_roll_number, validate_uk_phone, validate_student_name, format_uk_phone

class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("750x500")
        self.manager = StudentManager()
        self.selected_student_id = None

        self.build_ui()
        self.populate_table()

    def build_ui(self):
        # ======== Form Section ========
        form_frame = tb.Frame(self.root, padding=10)
        form_frame.pack(pady=5)

        tb.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tb.Label(form_frame, text="Contact").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tb.Label(form_frame, text="Roll Number").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.name_var = tb.StringVar()
        self.contact_var = tb.StringVar()
        self.roll_var = tb.StringVar()

        # Add validation traces to format phone number as user types
        self.contact_var.trace('w', self.on_contact_change)

        tb.Entry(form_frame, textvariable=self.name_var, width=20).grid(row=1, column=0, padx=5)
        tb.Entry(form_frame, textvariable=self.contact_var, width=20).grid(row=1, column=1, padx=5)
        tb.Entry(form_frame, textvariable=self.roll_var, width=20).grid(row=1, column=2, padx=5)

        # ======== Buttons ========
        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=5)

        tb.Button(button_frame, text="Add", bootstyle=PRIMARY, width=12, command=self.add_student).grid(row=0, column=0, padx=5)
        tb.Button(button_frame, text="Update", bootstyle=INFO, width=12, command=self.update_student).grid(row=0, column=1, padx=5)
        tb.Button(button_frame, text="Delete", bootstyle=DANGER, width=12, command=self.delete_student).grid(row=0, column=2, padx=5)
        tb.Button(button_frame, text="Clear", bootstyle=SECONDARY, width=12, command=self.clear_fields).grid(row=0, column=3, padx=5)
        tb.Button(button_frame, text="Export", bootstyle=WARNING, width=12, command=self.export_students).grid(row=0, column=4, padx=5)
        tb.Button(button_frame, text="Logout", bootstyle=DANGER, width=12, command=self.logout).grid(row=0, column=5, padx=5)

        # ======== Search Section ========
        search_frame = tb.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_var = tb.StringVar()
        search_entry = tb.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=0, padx=5)
        
        tb.Button(search_frame, text="Search", bootstyle=OUTLINE, command=self.search_student).grid(row=0, column=1, padx=5)
        tb.Button(search_frame, text="Show All", bootstyle="secondary-outline", command=self.populate_table).grid(row=0, column=2, padx=5)

        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: self.search_student())

        # ======== Student Table ========
        self.tree = tb.Treeview(self.root, columns=("ID", "Name", "Contact", "Roll"), show='headings', bootstyle="dark")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Roll", text="Roll Number")
        self.tree.column("ID", width=40)
        self.tree.column("Name", width=200)
        self.tree.column("Contact", width=150)
        self.tree.column("Roll", width=100)

        self.tree.pack(pady=10, fill=tb.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        # Add status bar
        self.status_var = tb.StringVar()
        self.status_var.set("Ready")
        status_bar = tb.Label(self.root, textvariable=self.status_var, relief=tb.SUNKEN, anchor=tb.W)
        status_bar.pack(side=tb.BOTTOM, fill=tb.X)

    def on_contact_change(self, *args):
        """Format phone number as user types"""
        try:
            current = self.contact_var.get()
            # Don't format while user is typing if it's getting longer
            # This prevents interference with user input
            pass
        except:
            pass

    def populate_table(self):
        """Populate table with all students"""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = self.manager.get_all_students()
        for student in students:
            self.tree.insert("", tb.END, values=student)
        
        # Update status
        self.status_var.set(f"Showing {len(students)} student(s)")

    def add_student(self):
        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        roll = self.roll_var.get().strip()

        # Enhanced validation
        if not self.validate_input(name, contact, roll):
            return

        success, msg = self.manager.add_student(name, contact, roll)
        if success:
            self.populate_table()
            self.clear_fields()
            self.status_var.set("Student added successfully")
            messagebox.showinfo("Success", msg)
        else:
            self.status_var.set("Failed to add student")
            messagebox.showerror("Error", msg)

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("No Selection", "Please select a student to update.")
            return

        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        roll = self.roll_var.get().strip()
        
        # Enhanced validation
        if not self.validate_input(name, contact, roll, is_update=True):
            return

        success, msg = self.manager.update_student(self.selected_student_id, name, contact, roll)
        if success:
            self.populate_table()
            self.clear_fields()
            self.status_var.set("Student updated successfully")
            messagebox.showinfo("Success", msg)
        else:
            self.status_var.set("Failed to update student")
            messagebox.showerror("Error", msg)

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return

        # Get student name for confirmation
        selected = self.tree.selection()
        if selected:
            student_name = self.tree.item(selected)["values"][1]
            confirmed = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete student '{student_name}'?\n\nThis action cannot be undone."
            )
            if confirmed:
                success, msg = self.manager.delete_student(self.selected_student_id)
                if success:
                    self.populate_table()
                    self.clear_fields()
                    self.status_var.set("Student deleted successfully")
                    messagebox.showinfo("Success", msg)
                else:
                    self.status_var.set("Failed to delete student")
                    messagebox.showerror("Error", msg)

    def search_student(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.populate_table()
            return

        results = self.manager.search_students(keyword)

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in results:
            self.tree.insert("", tb.END, values=student)
        
        # Update status
        self.status_var.set(f"Found {len(results)} result(s) for '{keyword}'")

    def export_students(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Student Data"
        )
        if file_path:
            success = self.manager.export_to_csv(file_path)
            if success:
                self.status_var.set(f"Data exported to {file_path}")
                messagebox.showinfo("Export Complete", f"Student data exported successfully to:\n{file_path}")
            else:
                self.status_var.set("Export failed")
                messagebox.showerror("Export Failed", "Failed to export student data.")

    def validate_input(self, name, contact, roll, is_update=False):
        """Enhanced input validation with better error messages"""
        if not name or not contact or not roll:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return False
        
        # Validate name
        if not validate_student_name(name):
            messagebox.showwarning(
                "Invalid Name", 
                "Name must be 2-50 characters long and contain only letters, spaces, hyphens, and apostrophes."
            )
            return False
        
        # Format and validate phone number
        formatted_contact = format_uk_phone(contact)
        if not validate_uk_phone(formatted_contact):
            messagebox.showwarning(
                "Invalid Contact", 
                "Please enter a valid UK phone number.\n\nExamples:\n• Mobile: 07123456789\n• Landline: 02012345678 or 01234567890"
            )
            return False
        
        # Update the contact field with formatted number
        self.contact_var.set(formatted_contact)
        
        # Validate roll number
        if not validate_roll_number(roll):
            messagebox.showwarning(
                "Invalid Roll Number", 
                "Roll number must be exactly 7 digits.\n\nExample: 1234567"
            )
            return False

        # Check roll number uniqueness
        exclude_id = self.selected_student_id if is_update else None
        if not self.manager.validate_unique_roll(roll, exclude_id):
            messagebox.showwarning(
                "Duplicate Roll Number", 
                "This roll number is already assigned to another student."
            )
            return False

        return True

    def logout(self):
        confirmed = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirmed:
            self.root.destroy()

    def clear_fields(self):
        """Clear all form fields and reset selection"""
        self.name_var.set("")
        self.contact_var.set("")
        self.roll_var.set("")
        self.selected_student_id = None
        
        # Clear tree selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.status_var.set("Form cleared")

    def on_row_selected(self, event):
        """Handle row selection with proper phone number formatting"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected)["values"]
            if len(values) >= 4:
                self.selected_student_id = values[0]
                self.name_var.set(values[1])
                
                # Ensure contact number is properly formatted with leading zero
                contact = str(values[2])
                formatted_contact = format_uk_phone(contact)
                self.contact_var.set(formatted_contact)
                
                self.roll_var.set(values[3])
                self.status_var.set(f"Selected student: {values[1]}")
        else:
            self.selected_student_id = None