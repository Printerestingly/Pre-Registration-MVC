from datetime import date, datetime


class Student:
    @staticmethod
    def is_valid_student_id(student_id: str) -> bool:
        return len(student_id) == 8 and student_id.isdigit() and student_id.startswith('69')


    @staticmethod
    def age(birthdate_str: str) -> int:
    # birthdate in ISO YYYY-MM-DD
        d = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        today = date.today()
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))


    @staticmethod
    def must_be_at_least_15(birthdate_str: str) -> bool:
        return Student.age(birthdate_str) >= 15