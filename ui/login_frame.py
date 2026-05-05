import customtkinter as ctk
from tkinter import messagebox
from config import *
from database import db


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master

        self.panel = ctk.CTkFrame(self, width=400, height=550, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="Đăng Nhập", font=("Segoe UI", 32, "bold"),
                     text_color="white").pack(pady=(40, 5))
        ctk.CTkLabel(self.panel, text="Chào mừng bạn trở lại!", font=("Segoe UI", 13),
                     text_color="#aaa").pack(pady=(0, 30))

        self.user_entry = self.create_input("Tài khoản nhân viên")
        self.pass_entry = self.create_input("Mật khẩu", is_password=True)

        self.show_pass_check = ctk.CTkCheckBox(self.panel, text="Hiện mật khẩu", font=("Segoe UI", 11),
                                               border_color=COLOR_GOLD, checkmark_color=COLOR_GOLD,
                                               text_color=COLOR_TEXT, command=self.toggle_password)
        self.show_pass_check.pack(pady=10)

        ctk.CTkButton(self.panel, text="Quên mật khẩu?", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 11),
                      hover=False, command=lambda: self.master.master.switch_page("Forgot")).pack()

        ctk.CTkButton(self.panel, text="ĐĂNG NHẬP", width=280, height=45,
                      fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"),
                      command=self.login).pack(pady=(10, 10))

        ctk.CTkButton(self.panel, text="Tạo tài khoản mới", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 12, "underline"),
                      hover=False, command=lambda: self.master.master.show_register()).pack()

    def create_input(self, placeholder, is_password=False):
        entry = ctk.CTkEntry(self.panel, placeholder_text=placeholder, width=300, height=45,
                             fg_color="#1a1a2e", border_color=COLOR_BORDER, text_color=COLOR_TEXT,
                             show="*" if is_password else "")
        entry.pack(pady=10)
        return entry

    def toggle_password(self):
        if self.show_pass_check.get():
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")

    def login(self):
        u, p = self.user_entry.get(), self.pass_entry.get()
        hashed_pw = db.hash_password(p)
        db.cursor.execute("SELECT full_name FROM users WHERE username=? AND password=?", (u, hashed_pw))
        res = db.cursor.fetchone()
        if res:
            self.master.master.show_main(res[0])
        else:
            messagebox.showerror("Từ chối", "Tài khoản hoặc mật khẩu không đúng!")