import tkinter as tk
from tkinter import ttk, messagebox


from views.subject_detail_view import SubjectDetailView


class StudentDashboardView(tk.Frame):
    def __init__(self, master, student_id, student_controller, subject_controller, enrollment_controller, on_logout):
        super().__init__(master)
        self.student_id = student_id
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
        top.columnconfigure(1, weight=1)


        self.lbl_title = ttk.Label(top, text='Profile', font=('Segoe UI', 14, 'bold'))
        self.lbl_title.grid(row=0, column=0, sticky='w')
        ttk.Button(top, text='Sign out', command=self.on_logout).grid(row=0, column=2, sticky='e')


        mid = ttk.Frame(self, padding=10)
        mid.grid(row=1, column=0, sticky='nsew')
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(1, weight=1)


        self.info = ttk.Label(mid, text='')
        self.info.grid(row=0, column=0, sticky='w', pady=(0,10))


        # Tabs: Available subjects / My enrollments
        self.tabs = ttk.Notebook(mid)
        self.tabs.grid(row=1, column=0, sticky='nsew')


        self.frame_available = ttk.Frame(self.tabs)
        self.frame_my = ttk.Frame(self.tabs)
        self.tabs.add(self.frame_available, text='Subjects not yet registered')
        self.tabs.add(self.frame_my, text='Registered subjects')


        # Available list
        self.tree_avail = ttk.Treeview(self.frame_available, columns=('code','name','credits','teacher','max','cur'), show='headings', height=12)
        for col, text in [('code','Code'),('name','Name'),('credits','Credits'),('teacher','Instructor'),('max','Max participants'),('cur','Registered')]:
            self.tree_avail.heading(col, text=text)
            self.tree_avail.column(col, width=120, anchor='center')
        self.tree_avail.pack(fill='both', expand=True, padx=10, pady=10)


        btns = ttk.Frame(self.frame_available)
        btns.pack(fill='x', padx=10, pady=(0,10))
        ttk.Button(btns, text='Details', command=self._open_detail).pack(side='left')
        ttk.Button(btns, text='Register', command=self._register_selected).pack(side='left', padx=6)


        # My enrollments
        self.tree_my = ttk.Treeview(self.frame_my, columns=('code','name','status','grade'), show='headings', height=12)
        for col, text in [('code','Code'),('name','Name'),('status','Status'),('grade','Grade')]:
            self.tree_my.heading(col, text=text)
            self.tree_my.column(col, width=160, anchor='center')
        self.tree_my.pack(fill='both', expand=True, padx=10, pady=10)

    def refresh(self):
        # ----- โหลดโปรไฟล์ -----
        student = self.student_controller.get_student(self.student_id)
        if not student:
            messagebox.showerror('Error', 'Student not found')
            return
        self.info.config(
            text=f"ID: {student['student_id']} | Name: {student['prefix']}{student['first_name']} {student['last_name']} | Age: {student['birthdate']}"
        )

        # ----- โหลดข้อมูลหลัก -----
        subjects = self.subject_controller.list_subjects()
        # แผนที่รหัสวิชา -> object (ใช้เปิดรายละเอียด/สมัคร)
        self._subject_map = {str(s.get('subject_code', '')).strip(): s for s in subjects}

        my_enroll = self.enrollment_controller.list_student_enrollments(self.student_id)
        my_codes = {str(e.get('subject_code', '')).strip() for e in my_enroll}

        # ----- วิชาที่ยังไม่ได้ลงทะเบียน -----
        for iid in self.tree_avail.get_children():
            self.tree_avail.delete(iid)

        for s in subjects:
            code = str(s.get('subject_code', '')).strip()
            if code in my_codes:
                continue
            # ใช้ code เป็น iid เพื่อกันเลขศูนย์หาย
            self.tree_avail.insert(
                '', 'end',
                iid=code,
                values=(code, s.get('name', ''), s.get('credits', ''), s.get('teacher', ''),
                        s.get('max_capacity', ''), s.get('current_enrolled', ''))
            )

        # ----- วิชาที่ลงทะเบียนแล้ว -----
        for iid in self.tree_my.get_children():
            self.tree_my.delete(iid)

        code_to_name = {str(s.get('subject_code', '')).strip(): s.get('name', '') for s in subjects}
        for e in my_enroll:
            code = str(e.get('subject_code', '')).strip()
            name = code_to_name.get(code, '-')
            self.tree_my.insert('', 'end',
                                values=(code, name, e.get('status', ''), e.get('grade') or '-'))



    def _get_selected_code(self):
        sel = self.tree_avail.selection()
        if not sel:
            return None
        return sel[0]  # <<< ได้เป็น subject_code จริง ๆ (string พร้อมศูนย์นำหน้า)


    def _open_detail(self):
        code = self._get_selected_code()
        if not code:
            messagebox.showinfo('Select', 'Please select subject')
            return
        subj = self._subject_map.get(code)
        if not subj:
            messagebox.showerror('Error', 'Subject not found')
            return
        win = tk.Toplevel(self)
        win.title('Details')
        SubjectDetailView(
            win,
            subject_code=subj,  # ส่ง object ตรง ๆ ก็ได้
            subject_controller=self.subject_controller,
            enrollment_controller=self.enrollment_controller,
            student_id=self.student_id,
            on_registered=lambda: (self.refresh(), win.destroy())
        ).pack(fill='both', expand=True)

    def _register_selected(self):
        code = self._get_selected_code()
        if not code:
            messagebox.showinfo('Select', 'Please select subject')
            return
        ok, msg = self.enrollment_controller.register(self.student_id, code)  # code เป็น string ถูกต้องแล้ว
        if ok:
            messagebox.showinfo('Success', msg)
            self.refresh()
        else:
            messagebox.showerror('Cannot register', msg)
   