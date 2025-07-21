# models/student.py

class Student:
    def __init__(self, name, contact, roll_number, student_id=None):
        self._id = student_id
        self._name = name
        self._contact = contact
        self._roll_number = roll_number

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def contact(self):
        return self._contact

    @property
    def roll_number(self):
        return self._roll_number

    def to_tuple(self):
        return (self._id, self._name, self._contact, self._roll_number)

    def to_db_tuple(self):
        return (self._name, self._contact, self._roll_number)
