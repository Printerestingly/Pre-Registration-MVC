from typing import Tuple
from models.subject import Subject

class SubjectController:
    def __init__(self, db):
        self.db = db

    def list_subjects(self):
        return self.db.read('subjects')

    def get_subject(self, subject_code: str):
        code = str(subject_code).strip()
        for s in self.db.read('subjects'):
            if str(s.get('subject_code', '')).strip() == code:
                return s
        return None



    def validate_subject(self, subject: dict) -> Tuple[bool, str]:
        if not Subject.is_valid_subject_code(subject['subject_code']):
            return False, 'Subject code not correct (8 digits and follow the conditions)'
        if int(subject['credits']) <= 0:
            return False, 'Credit must be more than 0'
        max_cap = int(subject['max_capacity'])
        if max_cap == 0:
            return False, 'Max participants must be > 0 or -1 if not limited'
        if int(subject['current_enrolled']) < 0:
            return False, 'Number of registrations must be ≥ 0'
        return True, 'OK'
