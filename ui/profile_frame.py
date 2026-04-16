import customtkinter as ctk
from config import *
from database import db


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.app = master.master  # HotelApp

        self.panel = ctk.CTkFrame(self, width=500, height=600, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="Hồ Sơ Của Bạn", font=("Georgia", 32, "bold"),
                     text_color=COLOR_NAVY).pack(pady=(40, 10))

        # Icon người dùng to đùng
        ctk.CTkLabel(self.panel, text="👤", font=("Segoe UI", 80)).pack(pady=10)

        # Thông tin sếp (Sẽ cập nhật khi load)
        self.info_label = ctk.CTkLabel(self.panel, text="Sếp: Đang tải...", font=("Segoe UI", 16, "bold"),
                                       text_color=COLOR_TEXT)
        self.info_label.pack(pady=10)

        self.email_label = ctk.CTkLabel(self.panel, text="Email: ...", font=("Segoe UI", 14), text_color=COLOR_GOLD)
        self.email_label.pack()

        # Nút Đăng xuất ngay trong hồ sơ
        ctk.CTkButton(self.panel, text="ĐĂNG XUẤT", fg_color="#e74c3c", hover_color="#c0392b",
                      text_color="white", font=("Segoe UI", 13, "bold"), width=200, height=40,
                      command=self.app.logout).pack(pady=40)

    def load_data(self):
        if self.app.current_user:
            # Truy vấn lấy thêm thông tin email từ DB
            db.cursor.execute("SELECT full_name, email FROM users WHERE full_name=?", (self.app.current_user,))
            res = db.cursor.fetchone()
            if res:
                self.info_label.configure(text=f"Sếp: {res[0].upper()}")
                self.email_label.configure(text=f"Email quản trị: {res[1]}")