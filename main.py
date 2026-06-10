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
        if not os.path.exists("user_guide.pdf"):
            try:
                pdf_data = (
                    b"%PDF-1.4\n"
                    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 595 842] /Contents 4 0 R >>\nendobj\n"
                    b"4 0 obj\n<< /Length 936 >>\nstream\n"
                    b"BT\n"
                    b"/F1 14 Tf\n"
                    b"50 780 Td\n"
                    b"(TRUONG DAI HOC HA LONG - KHOA CONG NGHE THONG TIN) Tj\n"
                    b"0 -25 Td\n"
                    b"(DREAMSTAY RESORT SYSTEM - TAI LIEU HUONG DAN SU DUNG) Tj\n"
                    b"/F1 10 Tf\n"
                    b"0 -30 Td\n"
                    b"(Mon hoc: Lap trinh Python | GVHD: ThS. Pham Nguyen Hong) Tj\n"
                    b"0 -15 Td\n"
                    b"(Nhom sinh vien thuc hien: Tran Duc Duong (Nhom truong) & Bui Thi Thuy Hoa) Tj\n"
                    b"0 -35 Td\n"
                    b"(1. TAI TY GIA LIVE: Lay ty gia thoi gian thuc tu REST API truc tuyen.) Tj\n"
                    b"0 -25 Td\n"
                    b"(2. LE TAN & DON HANG: Phe duyet dat phong, check-in, check-out va giao do an.) Tj\n"
                    b"0 -25 Td\n"
                    b"(3. QUAN TRI DU LIEU (CRUD): Them, sua, xoa da dong, va tim kiem thoi gian thuc.) Tj\n"
                    b"0 -25 Td\n"
                    b"(4. TUONG THICH EXCEL: Nhap/Xuat file CSV ma hoa UTF-8 with BOM khong loi font.) Tj\n"
                    b"0 -25 Td\n"
                    b"(5. THONG KE CO SO DU LIEU: Doanh thu khu vuc va bieu do hinh quat Matplotlib.) Tj\n"
                    b"0 -25 Td\n"
                    b"(6. EASTER EGGS: Phim tat am nhac an gia tri va hoan doi trang thai.) Tj\n"
                    b"0 -40 Td\n"
                    b"(Luu y: Vui long dat file user_guide.pdf ban scan goc vao thu muc de xem ban day du.) Tj\n"
                    b"ET\n"
                    b"endstream\n"
                    b"endobj\n"
                    b"xref\n"
                    b"0 5\n"
                    b"0000000000 65535 f\n"
                    b"0000000009 00000 n\n"
                    b"0000000059 00000 n\n"
                    b"0000000114 00000 n\n"
                    b"0000000289 00000 n\n"
                    b"trailer\n"
                    b"<< /Size 5 /Root 1 0 R >>\n"
                    b"startxref\n"
                    b"1278\n"
                    b"%%EOF"
                )
                with open("user_guide.pdf", "wb") as f:
                    f.write(pdf_data)
            except Exception:
                pass

        super().__init__()
        self.title("DreamStay")
        self.geometry("1300x850")
        self.minsize(1200, 750)
        try:
            self.state("zoomed")
        except:
            self.attributes("-zoomed", True)
        self.update()

        window_width = self.winfo_width()
        if window_width < 500:
            window_width = self.winfo_screenwidth()

        scale_factor = window_width / 1920.0
        scale_factor = max(0.7, min(scale_factor, 1.4))

        ctk.set_widget_scaling(scale_factor)
        ctk.set_window_scaling(scale_factor)

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
            "Phòng nghỉ": RoomView(self.container),
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

        self.chat_win = None
        self.chat_btn = ctk.CTkButton(
            self,
            text="💬 Dreamer",
            width=110,
            height=45,
            corner_radius=22,
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_BODY_BOLD,
            command=self.toggle_chat,
        )
        self.chat_btn.place(relx=0.97, rely=0.93, anchor="se")

        self.bind_all("<Control-BackSpace>", self.global_ctrl_backspace)
        self.bind_all("<Button-1>", self.global_click_unfocus, add="+")

    def check_persistent_login(self):
        if os.path.exists("session.txt"):
            try:
                with open("session.txt", "r", encoding="utf-8") as f:
                    encoded_data = f.read()
                decoded_str = xor_decrypt(encoded_data, "DreamStaySessionSalt2026")
                data = decoded_str.split("|")
                if len(data) == 3:
                    self.login_success(data[0], data[1], data[2], save_session=False)
            except Exception:
                pass

    def login_success(self, username, name, role, save_session=True):
        self.current_username = username
        self.current_user = name
        self.current_role = role

        from database import db

        db.log_action(username, "LOGIN", "users", username)

        if save_session:
            raw_str = f"{username}|{name}|{role}"
            encoded_b64 = xor_crypt(raw_str, "DreamStaySessionSalt2026")
            with open("session.txt", "w", encoding="utf-8") as f:
                f.write(encoded_b64)

        self.header.update_user_avatar(username)
        self.header.update_menu(True, role)
        self.switch_page("Trang chủ")

        mgmt_page = self.pages.get("Quản lý")
        update_func = getattr(mgmt_page, "update_user", None)
        if callable(update_func):
            update_func(name, role)

    def show_login(self):
        self.switch_page("Login")

    def show_register(self):
        self.switch_page("Register")

    def logout(self):
        from tkinter import messagebox

        if os.path.exists("session.txt"):
            os.remove("session.txt")

        pronoun = get_pronoun(self)

        self.current_user = None
        self.current_role = None
        self.header.update_user_avatar(None)
        self.header.update_menu(False, None)
        self.switch_page("Trang chủ")
        messagebox.showinfo("Thông báo", f"{pronoun.capitalize()} đã đăng xuất an toàn!")

    def switch_page(self, name):
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
                load_func()

        self.header.update_menu(self.current_user is not None, self.current_role, name)

    def toggle_chat(self):
        if self.chat_win is None or not self.chat_win.winfo_exists():
            from ui.chat_window import ChatWindow

            self.chat_win = ChatWindow(self)
        else:
            self.chat_win.deiconify()
            self.chat_win.lift()

    def global_click_unfocus(self, event):
        widget = event.widget
        try:
            class_name = widget.winfo_class()
            if class_name in ["Frame", "Label", "Tk", "Toplevel", "Canvas"]:
                widget.focus_set()
        except:
            pass

    def global_ctrl_backspace(self, event):
        widget = event.widget
        try:
            if (
                hasattr(widget, "selection_present")
                and hasattr(widget, "index")
                and hasattr(widget, "delete")
            ):
                if widget.selection_present():
                    widget.delete("sel.first", "sel.last")
                    return "break"
                insert_idx = widget.index("insert")
                if insert_idx == 0:
                    return "break"
                text = widget.get()[:insert_idx]
                import re

                match = re.search(r"(\s*\w+|\s+)\s*$", text)
                if match:
                    start_idx = insert_idx - len(match.group(0))
                else:
                    start_idx = 0
                widget.delete(start_idx, insert_idx)
                return "break"
            elif hasattr(widget, "compare") and hasattr(widget, "delete"):
                if widget.compare("insert", "==", "1.0"):
                    return "break"
                start_idx = widget.index("insert -1c wordstart")
                if widget.index(start_idx) == widget.index("insert"):
                    start_idx = widget.index("insert -1c")
                widget.delete(start_idx, "insert")
                return "break"
        except:
            pass




if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
