import os
import base64
from config import *
from ui.header import Header
from ui.home_frame import HomeFrame
from ui.about_frame import AboutFrame
from ui.room_view import RoomView
from ui.room_detail_frame import RoomDetailFrame
from ui.service_frame import ServiceFrame
from ui.service_detail_frame import ServiceDetailFrame
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
        if not os.path.exists("User_Guide.pdf"):
            try:
                pdf_data = (
                    b"%PDF-1.4\n"
                    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 595 842] /Contents 4 0 R >>\nendobj\n"
                    b"4 0 obj\n<< /Length 332 >>\nstream\n"
                    b"BT\n/F1 18 Tf\n50 780 Td\n(DREAMSTAY RESORT SYSTEM - USER GUIDE) Tj\n/F1 12 Tf\n0 -40 Td\n(1. TAI TY GIA LIVE: Fetch real-time exchange rates via public REST API.) Tj\n0 -25 Td\n(2. FRONT DESK: Approve bookings, check-in, check-out, and log revenue.) Tj\n0 -25 Td\n(3. SYSTEM CRUD: Insert, Edit, Delete, and Search database items.) Tj\n0 -25 Td\n(4. TOOLBAR QUERY: Instant search entry filter in real-time.) Tj\n0 -25 Td\n(5. EXPORT/IMPORT CSV: Fully compatible with Excel UTF-8 with BOM.) Tj\n0 -25 Td\n(6. ANALYTICS: Dynamic Matplotlib charts powered by Pandas and NumPy.) Tj\nET\n"
                    b"endstream\nendobj\n"
                    b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000244 00000 n\n"
                    b"trailer\n<< /Size 5 /Root 1 0 R >>\n"
                    b"startxref\n627\n%%EOF"
                )
                with open("User_Guide.pdf", "wb") as f:
                    f.write(pdf_data)
            except Exception:
                pass

        super().__init__()
        self.title("DreamStay")
        self.geometry("1300x850")
        try:
            self.state("zoomed")
        except:
            self.attributes("-zoomed", True)
        self.update()
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
            "Dịch vụ": ServiceFrame(self.container),
            "Chi tiết dịch vụ": ServiceDetailFrame(self.container),
            "Tiện ích": UtilityFrame(self.container),
            "Chi tiết tiện ích": UtilityDetailFrame(self.container),
            "Sự kiện": EventFrame(self.container),
            "Chi tiết sự kiện": EventDetailFrame(self.container),
            "Liên hệ": ContactFrame(self.container),
            "Quản lý": MainFrame(self.container),
            "Login": LoginFrame(self.container),
            "Register": RegisterFrame(self.container),
            "Forgot": ForgotFrame(self.container),
            "Hồ sơ": ProfileFrame(self.container),
        }

        self.switch_page("Trang chủ")
        self.check_persistent_login()

    def check_persistent_login(self):
        if os.path.exists("session.txt"):
            try:
                with open("session.txt", "rb") as f:
                    encoded_data = f.read()
                    decoded_str = base64.b64decode(encoded_data).decode("utf-8")
                    data = decoded_str.split("|")
                    if len(data) == 2:
                        self.login_success(data[0], data[1], save_session=False)
            except Exception:
                pass

    def switch_page(self, name, filters=None):
        for page_name, page in self.pages.items():
            if page.winfo_ismapped():
                page.pack_forget()
                hide_func = getattr(page, "on_hide", None)
                if callable(hide_func):
                    hide_func()

        if name in self.pages:
            target_page = self.pages[name]
            target_page.pack(fill="both", expand=True)

            show_func = getattr(target_page, "on_show", None)
            if callable(show_func):
                show_func()

            load_func = getattr(target_page, "load_data", None)
            if callable(load_func):
                if name == "Phòng":
                    load_func(filters)
                else:
                    load_func()

        self.header.update_menu(self.current_user is not None, self.current_role, name)

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
        self.header.user_btn.configure(
            text="ĐĂNG NHẬP", width=90, height=32, corner_radius=6, font=FONT_BODY_BOLD
        )
        self.header.update_menu(False, None)
        self.switch_page("Trang chủ")
        messagebox.showinfo("Thông báo", "Sếp đã đăng xuất an toàn!")

    def login_success(self, name, role, save_session=True):
        self.current_user = name
        self.current_role = role

        if save_session:
            raw_str = f"{name}|{role}"
            encoded_bytes = base64.b64encode(raw_str.encode("utf-8"))
            with open("session.txt", "wb") as f:
                f.write(encoded_bytes)

        self.header.user_btn.configure(
            text="👤", width=40, corner_radius=20, font=FONT_LABEL
        )
        self.header.update_menu(True, role)
        self.switch_page("Trang chủ")

        mgmt_page = self.pages.get("Quản lý")
        update_func = getattr(mgmt_page, "update_user", None)
        if callable(update_func):
            update_func(name, role)


if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
