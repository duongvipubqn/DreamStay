import customtkinter as ctk
from config import *
from ui.header import Header
from ui.home_frame import HomeFrame
from ui.room_view import RoomView
from ui.utility_frame import UtilityFrame
from ui.event_frame import EventFrame
from ui.contact_frame import ContactFrame
from ui.main_layout import MainFrame
from ui.login_frame import LoginFrame
from ui.register_frame import RegisterFrame
from ui.profile_frame import ProfileFrame


class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KHÁCH SẠN MỘNG MƠ")
        self.geometry("1300x850")
        self.configure(fg_color=COLOR_CREAM)

        self.current_user = None

        # Header cố định trên cùng
        self.header = Header(self, self.switch_page)
        self.header.pack(side="top", fill="x")

        # Container chứa các trang
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Khởi tạo danh sách các trang
        self.pages = {
            "Trang chủ": HomeFrame(self.container),
            "Phòng": RoomView(self.container),
            "Tiện ích": UtilityFrame(self.container),
            "Sự kiện": EventFrame(self.container),
            "Liên hệ": ContactFrame(self.container),
            "Quản lý": MainFrame(self.container),
            "Login": LoginFrame(self.container),
            "Register": RegisterFrame(self.container),
            "Hồ sơ": ProfileFrame(self.container)  # THÊM DÒNG NÀY
        }

        self.switch_page("Trang chủ")

    def switch_page(self, name):
        # Nếu nhấn vào Quản lý, kiểm tra xem đã login chưa (Ở đây tạm thời cho qua)
        # Nếu chưa login có thể sửa thành: if name == "Quản lý": name = "Login"

        for page in self.pages.values():
            page.pack_forget()

        if name in self.pages:
            self.pages[name].pack(fill="both", expand=True)
            if hasattr(self.pages[name], 'load_data'):
                self.pages[name].load_data()

    # Các hàm điều hướng trung gian
    def show_login(self):
        self.switch_page("Login")

    def show_register(self):
        self.switch_page("Register")

    def show_main(self, name):
        self.switch_page("Quản lý")
        # Cập nhật tên sếp trên sidebar của MainFrame
        self.pages["Quản lý"].update_user(name)

    def logout(self):
        from tkinter import messagebox
        self.current_user = None
        self.switch_page("Trang chủ")
        messagebox.showinfo("Thông báo", "Sếp đã đăng xuất an toàn!")

    def show_main(self, name):
        self.current_user = name  # Lưu tên sếp khi login thành công
        self.switch_page("Quản lý")
        self.pages["Quản lý"].update_user(name)

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()