import tkinter as tk
from tkinter import ttk, messagebox


class SubjectDetailView(tk.Frame):
    def __init__(self, master, subject_code, subject_controller, enrollment_controller, student_id, on_registered):
        super().__init__(master, padx=12, pady=12)
        self.subject_controller = subject_controller
        self.enrollment_controller = enrollment_controller
        self.student_id = student_id
        self.on_registered = on_registered
        self.subject = (
            subject_code if isinstance(subject_code, dict)
            else self.subject_controller.get_subject(str(subject_code).strip())
        )        
        self._build()


    def _build(self):
        if not self.subject:
            ttk.Label(self, text='Subject not found').pack()
            return
        s = self.subject
        info = (
            f"ID: {s['subject_code']}\n"
            f"Name: {s['name']}\n"
            f"Credits: {s['credits']}\n"
            f"Instructor: {s['teacher']}\n"
            f"Prerequisite subject: {s.get('prerequisite_code') or '-'}\n"
            f"Max participants: {s['max_capacity']}\n"
            f"Registered: {s['current_enrolled']}\n"
        )
        ttk.Label(self, text='Subject details', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0,10))
        ttk.Label(self, text=info, justify='left').pack(anchor='w')
        ttk.Button(self, text='Register', command=self._register).pack(anchor='w', pady=10)


    def _register(self):
        ok, msg = self.enrollment_controller.register(self.student_id, self.subject['subject_code'])
        if ok:
            messagebox.showinfo('Success', msg)
            self.on_registered()
        else:
            messagebox.showerror('Cannot be registered', msg)