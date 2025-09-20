from typing import Tuple
from models.student import Student

class StudentController:
    def __init__(self, db):
        self.db = db

    def get_student(self, student_id: str):
        sid = str(student_id).strip()
        for s in self.db.read('students'):
            if str(s.get('student_id', '')).strip() == sid:
                return s
        return None


    def list_students(self):
        return self.db.read('students')

    def validate_student(self, student: dict) -> Tuple[bool, str]:
        if not Student.is_valid_student_id(student['student_id']):
            return False, 'Student code not correct'
        if not Student.must_be_at_least_15(student['birthdate']):
            return False, 'Student must be at least 15 years old'
        return True, 'OK'
