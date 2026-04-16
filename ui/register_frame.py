import customtkinter as ctk
from tkinter import messagebox
from config import *
from database import db


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master

        self.panel = ctk.CTkFrame(self, width=450, height=750, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="Tạo Tài Khoản", font=("Georgia", 32, "bold"),
                     text_color=COLOR_NAVY).pack(pady=(30, 5))
        ctk.CTkLabel(self.panel, text="Đăng ký tài khoản quản lý nhân viên.", font=("Segoe UI", 13),
                     text_color=COLOR_TEXT).pack(pady=(0, 20))

        self.fields = {}
        data = [
            ("Họ và tên", "name"), ("Tên đăng nhập", "username"), ("Email", "email"),
            ("Số điện thoại", "phone"), ("Mật khẩu", "pass"), ("Nhập lại mật khẩu", "confirm")
        ]

        for ph, key in data:
            entry = ctk.CTkEntry(self.panel, placeholder_text=ph, width=320, height=45,
                                 fg_color="#f9f9f9", border_color=COLOR_BORDER, text_color=COLOR_TEXT,
                                 show="*" if key in ["pass", "confirm"] else "")
            entry.pack(pady=6)
            self.fields[key] = entry

        self.show_pass_check = ctk.CTkCheckBox(self.panel, text="Hiện mật khẩu", font=("Segoe UI", 11),
                                               border_color=COLOR_GOLD, checkmark_color=COLOR_GOLD,
                                               text_color=COLOR_TEXT, command=self.toggle_password)
        self.show_pass_check.pack(pady=10)

        ctk.CTkButton(self.panel, text="ĐĂNG KÝ NGAY", width=320, height=45,
                      fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"),
                      command=self.submit).pack(pady=(20, 10))

        ctk.CTkButton(self.panel, text="Đã có tài khoản? Đăng nhập", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 12),
                      hover=False, command=lambda: self.master.master.show_login()).pack(pady=10)

    def toggle_password(self):
        mode = "" if self.show_pass_check.get() else "*"
        self.fields["pass"].configure(show=mode)
        self.fields["confirm"].configure(show=mode)

    def submit(self):
        d = {k: v.get() for k, v in self.fields.items()}
        if "" in d.values(): return messagebox.showwarning("Lỗi", "Vui lòng nhập đủ tin!")
        if d["pass"] != d["confirm"]: return messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
        try:
            db.cursor.execute("INSERT INTO users (full_name, username, email, phone, password) VALUES (?,?,?,?,?)",
                              (d["name"], d["username"], d["email"], d["phone"], d["pass"]))
            db.conn.commit()
            messagebox.showinfo("Xong", "Tạo tài khoản thành công!")
            self.master.master.show_login()
        except:
            messagebox.showerror("Lỗi", "Username hoặc Email đã tồn tại!")