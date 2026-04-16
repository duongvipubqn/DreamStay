import customtkinter as ctk
from config import *


class ContactFrame(ctk.CTkFrame):  # Đảm bảo tên Class đúng như này
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Liên Hệ Với Chúng Tôi", font=("Georgia", 32, "bold"), text_color=COLOR_NAVY).pack(
            pady=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=100)

        # Cột trái: Form
        self.left = ctk.CTkFrame(self.container, fg_color=COLOR_WHITE, corner_radius=10, border_width=1,
                                 border_color=COLOR_BORDER)
        self.left.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.left, text="Gửi Tin Nhắn", font=("Segoe UI", 20, "bold"), text_color=COLOR_NAVY).pack(pady=20)
        ctk.CTkEntry(self.left, placeholder_text="Họ và tên", width=300, height=40).pack(pady=10)
        ctk.CTkEntry(self.left, placeholder_text="Email", width=300, height=40).pack(pady=10)

        # Dùng CTkTextbox cho nội dung tin nhắn
        self.msg_box = ctk.CTkTextbox(self.left, width=300, height=120, border_width=1, border_color=COLOR_BORDER)
        self.msg_box.pack(pady=10)

        ctk.CTkButton(self.left, text="GỬI TIN NHẮN", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"), width=300, height=40).pack(pady=20)

        # Cột phải: Thông tin
        self.right = ctk.CTkFrame(self.container, fg_color="transparent")
        self.right.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        info = [
            ("📍 Địa chỉ:", "123 Đại lộ Thượng Lưu, TP. Biển"),
            ("📞 Điện thoại:", "(+84) 123 456 789"),
            ("✉️ Email:", "info@khachsanmongmo.vn"),
            ("🕒 Giờ mở cửa:", "6:00 AM - 9:00 PM")
        ]

        for head, txt in info:
            f = ctk.CTkFrame(self.right, fg_color="transparent")
            f.pack(fill="x", pady=10)
            ctk.CTkLabel(f, text=head, font=("Segoe UI", 14, "bold"), text_color=COLOR_GOLD).pack(anchor="w")
            ctk.CTkLabel(f, text=txt, font=("Segoe UI", 14), text_color=COLOR_TEXT).pack(anchor="w")

    def load_data(self): pass