import tkinter as tk
from tkinter import ttk, messagebox

class AdminView(tk.Frame):
    def __init__(self, master, student_controller, subject_controller, enrollment_controller, on_logout):
        super().__init__(master)
        self.student_controller = student_controller
        self.subject_controller = subject_controller
        self.enrollment_controller = enrollment_controller
        self.on_logout = on_logout
        self._build()
        self.refresh()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = ttk.Frame(self, padding=10)
        top.grid(row=0, column=0, sticky='ew')
        ttk.Label(top, text='Registration and grade management ', font=('Segoe UI', 14, 'bold')).pack(side='left')
        ttk.Button(top, text='Sign out', command=self.on_logout).pack(side='right')

        body = ttk.Frame(self, padding=10)
        body.grid(row=1, column=0, sticky='nsew')
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(body, columns=('id','student','subject','status','grade'), show='headings')
        for col, text in [('id','ID'),('student','StudentID'),('subject','SubjectCode'),('status','Status'),('grade','Grade')]:
            self.tree.heading(col, text=text)
        self.tree.column(col, width=150, anchor='center')
        self.tree.grid(row=0, column=0, sticky='nsew')

        form = ttk.Frame(body)
        form.grid(row=1, column=0, sticky='ew', pady=10)
        ttk.Label(form, text='StudentID').grid(row=0, column=0)
        self.e_student = ttk.Entry(form, width=12)
        self.e_student.grid(row=0, column=1)
        ttk.Label(form, text='SubjectCode').grid(row=0, column=2)
        self.e_subject = ttk.Entry(form, width=12)
        self.e_subject.grid(row=0, column=3)
        ttk.Label(form, text='Grade (Example A,B+,B,...)').grid(row=0, column=4)
        self.e_grade = ttk.Entry(form, width=10)
        self.e_grade.grid(row=0, column=5)
        ttk.Button(form, text='Set Grade', command=self._set_grade).grid(row=0, column=6, padx=8)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in self.enrollment_controller.list_all_enrollments():
            self.tree.insert('', 'end', values=(e['id'], e['student_id'], e['subject_code'], e['status'], e.get('grade') or '-'))


    def _set_grade(self):
        s_id = self.e_student.get().strip()
        sub = self.e_subject.get().strip()
        grade = self.e_grade.get().strip() or None
        if not s_id or not sub:
            messagebox.showinfo('Fill in information', 'Fill in your StudentID and SubjectCode')
            return
        ok = self.enrollment_controller.set_grade(s_id, sub, grade)
        if ok:
            messagebox.showinfo('Success', 'Grades updates')
            self.refresh()
        else:
            messagebox.showerror('Error', 'No matching registration found.')