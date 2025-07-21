# gui/main_screen.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from managers.student_manager import StudentManager
from utils.helpers import validate_roll_number, validate_uk_phone


class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("750x500")
        self.manager = StudentManager()

        self.build_ui()
        self.populate_table()

    def build_ui(self):
        # ======== Form Section ========
        form_frame = tb.Frame(self.root, padding=10)
        form_frame.pack(pady=5)

        tb.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(form_frame, text="Contact").grid(row=0, column=1, padx=5, pady=5)
        tb.Label(form_frame, text="Roll Number").grid(row=0, column=2, padx=5, pady=5)

        self.name_var = tb.StringVar()
        self.contact_var = tb.StringVar()
        self.roll_var = tb.StringVar()

        tb.Entry(form_frame, textvariable=self.name_var, width=20).grid(row=1, column=0, padx=5)
        tb.Entry(form_frame, textvariable=self.contact_var, width=20).grid(row=1, column=1, padx=5)
        tb.Entry(form_frame, textvariable=self.roll_var, width=20).grid(row=1, column=2, padx=5)

        # ======== Buttons ========
        button_frame = tb.Frame(self.root)
        button_frame.pack(pady=5)

        tb.Button(button_frame, text="Add", bootstyle=PRIMARY, width=12, command=self.add_student).grid(row=0, column=0, padx=5)
        tb.Button(button_frame, text="Update", bootstyle=INFO, width=12, command=self.update_student).grid(row=0, column=1, padx=5)
        tb.Button(button_frame, text="Delete", bootstyle=DANGER, width=12, command=self.delete_student).grid(row=0, column=2, padx=5)
        tb.Button(button_frame, text="Export", bootstyle=SECONDARY, width=12, command=self.export_students).grid(row=0, column=3, padx=5)
        tb.Button(button_frame, text="Logout", bootstyle=WARNING, width=12, command=self.logout).grid(row=0, column=4, padx=5)

        # ======== Search Section ========
        search_frame = tb.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_var = tb.StringVar()
        tb.Entry(search_frame, textvariable=self.search_var, width=40).grid(row=0, column=0, padx=5)
        tb.Button(search_frame, text="Search", bootstyle=OUTLINE, command=self.search_student).grid(row=0, column=1)

        # ======== Student Table ========
        self.tree = tb.Treeview(self.root, columns=("ID", "Name", "Contact", "Roll"), show='headings', bootstyle="dark")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Roll", text="Roll Number")
        self.tree.column("ID", width=40)

        self.tree.pack(pady=10, fill=tb.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        students = self.manager.get_all_students()
        for student in students:
            self.tree.insert("", tb.END, values=student)

    def add_student(self):
        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        roll = self.roll_var.get().strip()

        if not name or not contact or not roll:
            messagebox.showwarning("Missing Fields", "Please fill all fields.")
            return
        
        if not validate_uk_phone(contact):
            messagebox.showwarning("Invalid Contact", "Please enter a valid UK phone number.")
            return
        
        if not validate_roll_number(roll):
            messagebox.showwarning("Invalid Roll Number", "Roll number must be exactly 7 digits.")
            return

        success, msg = self.manager.add_student(name, contact, roll)
        if success:
            self.populate_table()
            self.clear_fields()
        else:
            messagebox.showerror("Error", msg)

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to update.")
            return

        student_id = self.tree.item(selected)["values"][0]
        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        roll = self.roll_var.get().strip()
        
        if not name or not contact or not roll:
            messagebox.showwarning("Missing Fields", "Please fill all fields before updating.")
            return
        
        if not validate_uk_phone(contact):
            messagebox.showwarning("Invalid Contact", "Please enter a valid UK phone number.")
            return
        
        if not validate_roll_number(roll):
            messagebox.showwarning("Invalid Roll Number", "Roll number must be 7 digits.")
            return

        success, msg = self.manager.update_student(student_id, name, contact, roll)
        if success:
            self.populate_table()
            self.clear_fields()
        else:
            messagebox.showerror("Error", msg)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return

        student_id = self.tree.item(selected)["values"][0]
        confirmed = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
        if confirmed:
            self.manager.delete_student(student_id)
            self.populate_table()
            self.clear_fields()

    def search_student(self):
        keyword = self.search_var.get()
        results = self.manager.search_students(keyword)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in results:
            self.tree.insert("", tb.END, values=student)

    def export_students(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")])
        if file_path:
            success = self.manager.export_to_csv(file_path)
            if success:
                messagebox.showinfo("Exported", "Student data exported successfully.")

    def logout(self):
        self.root.destroy()

    def clear_fields(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.roll_var.set("")

    def on_row_selected(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected)["values"]
            self.name_var.set(values[1])
            self.contact_var.set(values[2])
            self.roll_var.set(values[3])
