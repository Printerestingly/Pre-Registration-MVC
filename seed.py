from datetime import date, timedelta
import random

def seed_all(db):
    students = []
    base_birth = date.today().replace(year=date.today().year - 16) # ~16yo
    for i in range(10):
        sid = f"69{str(i+1).zfill(6)}" # 69000001 ... 69000010
        students.append({
            'student_id': sid,
            'prefix': 'Mr. ' if i % 2 == 0 else 'Ms. ',
            'first_name': f'Name{i+1}',
            'last_name': f'Lastname{i+1}',
            'birthdate': (base_birth - timedelta(days=30*i)).isoformat(),
            'current_school': 'High School ABC',
            'email': f'student{i+1}@school.test'
        })
    db.write('students', students)

    subjects = []
    teachers = ['Dr. Brown','Ms. Green','Mr. White','Dr. Black','Mrs. Pink']

    # 6 courses starting with 0550xxxxx (faculty)
    for i in range(6):
        code = f"0550{random.randint(1,9)}{str(i+1).zfill(2)}" # e.g. 05501501
        subjects.append({
            'subject_code': code,
            'name': f'Faculty Course {i+1}',
            'credits': 3,
            'teacher': random.choice(teachers),
            'prerequisite_code': None,
            'max_capacity': 20 if i % 2 == 0 else -1,
            'current_enrolled': 0
        })

    # 4 general courses starting with 9069xxxx
    for i in range(4):
        code = f"9069{str(100+i)}" # e.g. 9069100x -> ensure 8 digits
        code = code[:8] # just in case
        subjects.append({
            'subject_code': code,
            'name': f'GenEd Course {i+1}',
            'credits': 2,
            'teacher': random.choice(teachers),
            'prerequisite_code': None,
            'max_capacity': 10,
            'current_enrolled': 0
        })

    # Add one course with prerequisite = first faculty course
    prereq_code = subjects[0]['subject_code']
    subjects.append({
        'subject_code': '90691234',
        'name': 'Advanced GenEd (needs prereq)',
        'credits': 2,
        'teacher': 'Dr. Silver',
        'prerequisite_code': prereq_code,
        'max_capacity': 5,
        'current_enrolled': 0
    })

    db.write('subjects', subjects)

    # Empty enrollments
    db.write('enrollments', [])