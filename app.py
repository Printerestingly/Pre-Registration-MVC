import os
import tkinter as tk
from tkinter import messagebox

from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from controllers.subject_controller import SubjectController
from controllers.enrollment_controller import EnrollmentController

from storage.json_db import JsonDB
from views.login_view import LoginView
from views.student_dashboard_view import StudentDashboardView
from views.admin_view import AdminView

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

db = JsonDB(DATA_DIR)

# Seed sample data if empty
if not db.exists('students'):
    from seed import seed_all
    seed_all(db)

# Controllers
auth_controller = AuthController(db)
student_controller = StudentController(db)
subject_controller = SubjectController(db)
enrollment_controller = EnrollmentController(db)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Pre-Enrollment MVC')
        self.geometry('1000x650')
        self.resizable(True, True)
        self.current_user = None  # dict for student or {'role':'admin'}
        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True)
        self.show_login()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        LoginView(self.container, on_login=self._handle_login).pack(fill='both', expand=True)

    def _handle_login(self, username, password=None):
        user = auth_controller.login(username, password)
        if not user:
            messagebox.showerror('Login failed', 'Invalid credentials or user not found')
            return
        self.current_user = user
        role = user.get('role', 'student')
        if role == 'admin':
            self.show_admin()
        else:
            self.show_student_dashboard(user['student_id'])

    def show_student_dashboard(self, student_id):
        self.clear()
        view = StudentDashboardView(
            self.container,
            student_id=student_id,
            student_controller=student_controller,
            subject_controller=subject_controller,
            enrollment_controller=enrollment_controller,
            on_logout=self._logout,
        )
        view.pack(fill='both', expand=True)

    def show_admin(self):
        self.clear()
        AdminView(
            self.container,
            student_controller=student_controller,
            subject_controller=subject_controller,
            enrollment_controller=enrollment_controller,
            on_logout=self._logout,
        ).pack(fill='both', expand=True)

    def _logout(self):
        self.current_user = None
        self.show_login()


if __name__ == '__main__':
    App().mainloop()
