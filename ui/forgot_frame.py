from tkinter import messagebox
from config import *
from database import db

class ForgotFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master

        self.panel = ctk.CTkFrame(self, width=450, height=600, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="Quên Mật Khẩu", font=("Segoe UI", 32, "bold"),
                     text_color="white").pack(pady=(40, 5))
        ctk.CTkLabel(self.panel, text="Nhập thông tin để thay đổi mật khẩu.", font=("Segoe UI", 13),
                     text_color=COLOR_TEXT).pack(pady=(0, 20))

        self.fields = {}
        data = [
            ("Tên đăng nhập", "username"),
            ("Mật khẩu mới", "new_pass"),
            ("Nhập lại mật khẩu mới", "confirm")
        ]

        for ph, key in data:
            is_pass = True if key in ["new_pass", "confirm"] else False
            entry = ctk.CTkEntry(self.panel, placeholder_text=ph, width=320, height=45,
                                 fg_color="#1a1a2e", border_color=COLOR_BORDER, text_color=COLOR_TEXT,
                                 show="*" if is_pass else "")
            entry.pack(pady=10)
            self.fields[key] = entry

        ctk.CTkButton(self.panel, text="CẬP NHẬT MẬT KHẨU", width=320, height=45,
                      fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"),
                      command=self.reset_password).pack(pady=(30, 10))

        def go_to_login():
            app = self.winfo_toplevel()
            func = getattr(app, "show_login", None)
            if callable(func):
                func()

        ctk.CTkButton(self.panel, text="Quay lại đăng nhập", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 12),
                      hover=False, command=go_to_login).pack(pady=10)

    def reset_password(self):
        u = self.fields["username"].get()
        p = self.fields["new_pass"].get()
        c = self.fields["confirm"].get()

        if u == "" or p == "" or c == "":
            return messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

        if p != c:
            return messagebox.showerror("Lỗi", "Mật khẩu mới không trùng khớp!")

        db.cursor.execute("SELECT * FROM users WHERE username=?", (u,))
        if not db.cursor.fetchone():
            return messagebox.showerror("Lỗi", "Tên đăng nhập không tồn tại!")

        db.cursor.execute("UPDATE users SET password=? WHERE username=?", (p, u))
        db.conn.commit()
        messagebox.showinfo("Thành công", "Mật khẩu đã được thay đổi thành công!")

        app = self.winfo_toplevel()
        func = getattr(app, "show_login", None)
        if callable(func):
            func()
        return None