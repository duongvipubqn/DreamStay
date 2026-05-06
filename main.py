import customtkinter as ctk
import os
from config import *
from ui.header import Header
from ui.home_frame import HomeFrame
from ui.about_frame import AboutFrame
from ui.room_view import RoomView
from ui.room_detail_frame import RoomDetailFrame
from ui.utility_frame import UtilityFrame
from ui.utility_detail_frame import UtilityDetailFrame
from ui.event_frame import EventFrame
from ui.event_detail_frame import EventDetailFrame
from ui.contact_frame import ContactFrame
from ui.main_layout import MainFrame
from ui.login_frame import LoginFrame
from ui.register_frame import RegisterFrame
from ui.forgot_frame import ForgotFrame
from ui.profile_frame import ProfileFrame

class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DreamStay")
        self.geometry("1300x850")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color=COLOR_CREAM)

        self.current_user = None
        self.current_role = None

        self.header = Header(self, self.switch_page)
        self.header.pack(side="top", fill="x")
        self.header.update_menu(False, None)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.pages = {
            "Trang chủ": HomeFrame(self.container),
            "Giới thiệu": AboutFrame(self.container),
            "Phòng": RoomView(self.container),
            "Chi tiết phòng": RoomDetailFrame(self.container),
            "Tiện ích": UtilityFrame(self.container),
            "Chi tiết tiện ích": UtilityDetailFrame(self.container),
            "Sự kiện": EventFrame(self.container),
            "Chi tiết sự kiện": EventDetailFrame(self.container),
            "Liên hệ": ContactFrame(self.container),
            "Quản lý": MainFrame(self.container),
            "Login": LoginFrame(self.container),
            "Register": RegisterFrame(self.container),
            "Forgot": ForgotFrame(self.container),
            "Hồ sơ": ProfileFrame(self.container)
        }

        self.switch_page("Trang chủ")
        self.check_persistent_login()

    def check_persistent_login(self):
        if os.path.exists("session.txt"):
            try:
                with open("session.txt", "r", encoding="utf-8") as f:
                    data = f.read().split("|")
                    if len(data) == 2:
                        self.login_success(data[0], data[1], save_session=False)
            except:
                pass

    def switch_page(self, name, filters=None):
        for page in self.pages.values():
            page.pack_forget()

        if name in self.pages:
            self.pages[name].pack(fill="both", expand=True)
            if hasattr(self.pages[name], 'load_data'):
                if name == "Phòng":
                    self.pages[name].load_data(filters)
                else:
                    self.pages[name].load_data()

    def show_login(self):
        self.switch_page("Login")

    def show_register(self):
        self.switch_page("Register")

    def logout(self):
        from tkinter import messagebox
        if os.path.exists("session.txt"):
            os.remove("session.txt")

        self.current_user = None
        self.current_role = None
        self.header.user_btn.configure(text="ĐĂNG NHẬP", width=90, height=32, corner_radius=6,
                                       font=("Segoe UI", 12, "bold"))
        self.header.update_menu(False, None)
        self.switch_page("Trang chủ")
        messagebox.showinfo("Thông báo", "Sếp đã đăng xuất an toàn!")

    def login_success(self, name, role, save_session=True):
        self.current_user = name
        self.current_role = role

        if save_session:
            with open("session.txt", "w", encoding="utf-8") as f:
                f.write(f"{name}|{role}")

        self.header.user_btn.configure(text="👤", width=40, corner_radius=20, font=("Segoe UI", 18))
        self.header.update_menu(True, role)
        self.switch_page("Trang chủ")
        self.pages["Quản lý"].update_user(name, role)

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()