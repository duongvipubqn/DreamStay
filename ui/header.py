import customtkinter as ctk
from config import *
import colorsys


class Header(ctk.CTkFrame):
    def __init__(self, master, switch_func):
        super().__init__(master, fg_color=COLOR_NAVY, height=70, corner_radius=0)
        self.pack_propagate(False)
        self.switch_func = switch_func
        self.app = master
        self.hue = 0

        self.brand_container = ctk.CTkFrame(self, fg_color="transparent")
        self.brand_container.pack(side="left", padx=30)

        self.letters = []
        for char in "DreamStay":
            lbl = ctk.CTkLabel(self.brand_container, text=char,
                               font=("Edwardian Script ITC", 50))
            lbl.pack(side="left", padx=0)
            self.letters.append(lbl)

        self.user_btn = ctk.CTkButton(self, text="ĐĂNG NHẬP", width=90, height=32, corner_radius=6,
                                      fg_color="white", text_color=COLOR_NAVY,
                                      hover_color=COLOR_GOLD, font=("Segoe UI", 12, "bold"),
                                      command=self.handle_user_click)
        self.user_btn.pack(side="right", padx=30)

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=20)

        self.update_menu(False)
        self.animate_rainbow()

    def animate_rainbow(self):
        self.hue += 0.005
        if self.hue > 1.0: self.hue = 0

        for i, lbl in enumerate(self.letters):
            char_hue = (self.hue + (i * 0.05)) % 1.0

            rgb = colorsys.hsv_to_rgb(char_hue, 0.4, 1.0)
            color_hex = '#%02x%02x%02x' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

            lbl.configure(text_color=color_hex)

        self.after(30, self.animate_rainbow)

    def update_menu(self, is_logged_in):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        menus = ["Trang chủ", "Phòng", "Tiện ích", "Sự kiện", "Liên hệ"]
        if is_logged_in:
            menus.append("Quản lý")

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