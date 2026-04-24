import customtkinter as ctk
from config import *

class Header(ctk.CTkFrame):
    def __init__(self, master, switch_func):
        super().__init__(master, fg_color=COLOR_NAVY, height=70, corner_radius=0)
        self.pack_propagate(False)
        self.switch_func = switch_func
        self.app = master

        ctk.CTkLabel(self, text="KháchSạnMộngMơ", font=("Segoe UI", 20, "bold"),
                     text_color=COLOR_GOLD).pack(side="left", padx=30)

        self.user_btn = ctk.CTkButton(self, text="ĐĂNG NHẬP", width=90, height=32, corner_radius=6,
                                      fg_color="white", text_color=COLOR_NAVY,
                                      hover_color=COLOR_GOLD, font=("Segoe UI", 12, "bold"),
                                      command=self.handle_user_click)
        self.user_btn.pack(side="right", padx=30)

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=20)

        menus = ["Trang chủ", "Phòng", "Tiện ích", "Sự kiện", "Liên hệ", "Quản lý"]
        for menu in menus:
            btn = ctk.CTkButton(self.menu_frame, text=menu, font=("Segoe UI", 13, "bold"),
                                fg_color="transparent", text_color="white",
                                hover_color=COLOR_GOLD, width=100,
                                command=lambda m=menu: self.switch_func(m))
            btn.pack(side="left", padx=5)

    def handle_user_click(self):
        if self.app.current_user is None:
            self.app.show_login()
        else:
            self.app.switch_page("Hồ sơ")