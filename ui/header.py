import customtkinter as ctk
from config import *

class Header(ctk.CTkFrame):
    def __init__(self, master, switch_func):
        super().__init__(master, fg_color=COLOR_NAVY, height=70, corner_radius=0)
        self.pack_propagate(False)
        self.switch_func = switch_func
        self.app = master # HotelApp

        # Logo bên trái
        ctk.CTkLabel(self, text="KháchSạnMộngMơ", font=("Georgia", 20, "bold"),
                     text_color=COLOR_GOLD).pack(side="left", padx=30)

        # Nút Avatar bên phải (Click để chuyển trang)
        self.user_btn = ctk.CTkButton(self, text="👤", width=40, height=40, corner_radius=20,
                                      fg_color=COLOR_WHITE, text_color=COLOR_NAVY,
                                      hover_color=COLOR_GOLD, font=("Segoe UI", 16),
                                      command=self.handle_user_click) # Đổi sang lệnh click
        self.user_btn.pack(side="right", padx=30)

        # Menu điều hướng
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=20)

        menus = ["Trang chủ", "Phòng", "Tiện ích", "Sự kiện", "Liên hệ", "Quản lý"]
        for menu in menus:
            btn = ctk.CTkButton(self.menu_frame, text=menu, font=("Segoe UI", 13, "bold"),
                                fg_color="transparent", text_color="#ccc",
                                hover_color=COLOR_GOLD, width=100,
                                command=lambda m=menu: self.switch_func(m))
            btn.pack(side="left", padx=5)

    def handle_user_click(self):
        if self.app.current_user is None:
            # Nếu chưa đăng nhập -> Sang trang Login
            self.app.show_login()
        else:
            # Nếu đã đăng nhập -> Sang trang Hồ sơ
            self.app.switch_page("Hồ sơ")