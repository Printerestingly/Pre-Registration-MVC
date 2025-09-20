import tkinter as tk
from tkinter import ttk


class LoginView(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.on_login = on_login
        self._build()


    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        card = ttk.Frame(self, padding=24)
        card.grid(row=0, column=0, sticky='ns   ew')
        for i in range(2):
            card.columnconfigure(i, weight=1)


        ttk.Label(card, text='Login', font=('Segoe UI', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0,10))


        ttk.Label(card, text='Student ID (8 digits, starts with 69) or admin').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.username = ttk.Entry(card)
        self.username.grid(row=1, column=1, sticky='ew', padx=5, pady=5)


        ttk.Label(card, text='Password (for admin only)').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password = ttk.Entry(card, show='*')
        self.password.grid(row=2, column=1, sticky='ew', padx=5, pady=5)


        ttk.Button(card, text='Login', command=self._do_login).grid(row=3, column=0, columnspan=2, pady=10)


    def _do_login(self):
        self.on_login(self.username.get().strip(), self.password.get().strip())