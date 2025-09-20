from typing import Optional

class AuthController:
    def __init__(self, db):
        self.db = db


    def login(self, username: str, password: Optional[str]): 
               
        # Admin: username 'admin', password 'admin'
        if username == 'admin' and password == 'admin':
            return {'role': 'admin', 'username': 'admin'}
        
        # Student: username is 8-digit student_id starting with 69; no password for simplicity
        students = self.db.read('students')
        for s in students:
            if s['student_id'] == username:
                return {'role': 'student', 'student_id': s['student_id']}
        return None