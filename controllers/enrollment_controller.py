from datetime import datetime
from typing import Optional, Tuple
from models.enrollment import CapacityPolicy


class EnrollmentController:
    def __init__(self, db):
        self.db = db

    # อ่าน enrollments ของนักเรียนคนหนึ่ง
    def list_student_enrollments(self, student_id: str):
        return [e for e in self.db.read('enrollments') if e['student_id'] == student_id]

    # อ่าน enrollments ทั้งหมด (ถูกเรียกจาก AdminView.refresh)
    def list_all_enrollments(self):
        return self.db.read('enrollments')

    def get_completed_subject_codes(self, student_id: str):
        return [
            e['subject_code']
            for e in self.list_student_enrollments(student_id)
            if e.get('status') == 'completed' and e.get('grade')
        ]

    def is_already_enrolled(self, student_id: str, subject_code: str) -> bool:
        for e in self.list_student_enrollments(student_id):
            if e['subject_code'] == subject_code and e['status'] in ('enrolled', 'completed'):
                return True
        return False

    def can_register(self, student: dict, subject: dict) -> Tuple[bool, str]:
        # อายุ ≥ 15
        from models.student import Student
        if not Student.must_be_at_least_15(student['birthdate']):
            return False, 'Student must be at least 15 years old'

        # ความจุ
        max_cap = int(subject['max_capacity'])
        cur = int(subject['current_enrolled'])

        if max_cap != -1:
            if not CapacityPolicy.can_register_with_cap(cur, max_cap):
                return False, 'Subject reached maximum participants'
        else:
            if not CapacityPolicy.can_register_unlimited():
                return False, 'Cannot register'

        # พรีเรค
        prereq = subject.get('prerequisite_code')
        if prereq:
            if prereq not in self.get_completed_subject_codes(student['student_id']):
                return False, f'Must pass prerequisite ({prereq}) before registering'

        # ลงซ้ำ
        if self.is_already_enrolled(student['student_id'], subject['subject_code']):
            return False, 'You have already registered'

        return True, 'OK'

    def register(self, student_id: str, subject_code: str) -> Tuple[bool, str]:
        sid  = str(student_id).strip()
        code = str(subject_code).strip()

        students = self.db.read('students')
        subjects = self.db.read('subjects')
        student = next((s for s in students  if str(s.get('student_id','')).strip() == sid), None)
        subject = next((s for s in subjects  if str(s.get('subject_code','')).strip() == code), None)
        if not student or not subject:
            return False, 'Subject or Student not found'

        ok, reason = self.can_register(student, subject)
        if not ok:
            return False, reason

        enrollments = self.db.read('enrollments')
        new_id = (max([e['id'] for e in enrollments], default=0) + 1)
        enrollments.append({
            'id': new_id,
            'student_id': str(student_id).strip(),
            'subject_code': str(subject_code).strip(),
            'status': 'enrolled',
            'grade': None,
            'created_at': datetime.utcnow().isoformat()
        })
        self.db.write('enrollments', enrollments)

        subjects = self.db.read('subjects')
        for s in subjects:
            if str(s.get('subject_code', '')).strip() == str(subject_code).strip():
                s['current_enrolled'] = int(s['current_enrolled']) + 1
                break
        self.db.write('subjects', subjects)

        return True, 'Registration complete'


    def set_grade(self, student_id: str, subject_code: str, grade: Optional[str]):
        enrollments = self.db.read('enrollments')
        changed = False
        for e in enrollments:
            if e['student_id'] == student_id and e['subject_code'] == subject_code:
                e['grade'] = grade
                e['status'] = 'completed' if grade else 'enrolled'
                changed = True
        if changed:
            self.db.write('enrollments', enrollments)
        return changed

