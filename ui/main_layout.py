import sqlite3
import webbrowser
import threading
import requests
import time
from config import *
from ui.reception import ReceptionFrame
from ui.order_mgmt_frame import OrderMgmtFrame
from ui.crud_frame import CRUDFrame
from ui.statistics import StatisticsFrame
from ui.log_frame import LogFrame
from ui.mgmt_log_frame import MgmtLogFrame
from ui.utility_mgmt_frame import UtilityMgmtFrame
from tkinter import messagebox
from database import db


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master
        self.current_role = None
        self.staff_reg_btn = None
        self.voucher_grant_btn = None

        self.sidebar = ctk.CTkFrame(
            self, width=200, fg_color=COLOR_NAVY, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.frames = {
            "Lễ Tân": ReceptionFrame(self.content),
            "Đơn Hàng": OrderMgmtFrame(self.content),
            "Tiện Ích": UtilityMgmtFrame(self.content),
            "Phòng Nghỉ": CRUDFrame(
                self.content,
                "Quản Lý Phòng Nghỉ (PMS)",
                "rooms",
                [
                    "ID",
                    "Địa Điểm",
                    "Loại Phòng",
                    "Tình Trạng",
                    "Sức Chứa",
                    "Giá (VNĐ)",
                ],
            ),
            "Khách Hàng": CRUDFrame(
                self.content,
                "Quản Lý Khách Hàng (CRM)",
                "customers",
                [
                    "ID",
                    "Họ Tên",
                    "Email",
                    "Số Điện Thoại",
                    "Thành Phố",
                    "Tổng Chi Tiêu",
                ],
            ),
            "Nhân Viên": CRUDFrame(
                self.content,
                "Quản Lý Nhân Sự (HRM)",
                "employees",
                [
                    "ID",
                    "Họ Tên",
                    "Chức Vụ",
                    "Địa Điểm",
                    "Số Điện Thoại",
                    "Lương (VNĐ)",
                    "Trạng thái",
                ],
            ),
            "Kho Hàng": CRUDFrame(
                self.content,
                "Quản Lý Kho Hàng (F&B)",
                "inventory",
                [
                    "ID",
                    "Danh Mục",
                    "Tên Món",
                    "Giá (VNĐ)",
                    "Số Lượng Tồn",
                ],
            ),
            "Phản Hồi": CRUDFrame(
                self.content,
                "Quản Lý Phản Hồi & Góp Ý",
                "contact_messages",
                [
                    "ID",
                    "Họ Tên",
                    "Email",
                    "Chủ Đề",
                    "Nội Dung",
                    "Thời Gian",
                ],
            ),
            "Nhật Ký Hệ Thống": LogFrame(self.content),
            "Nhật Ký Quản Lý": MgmtLogFrame(self.content),
            "Thống Kê": StatisticsFrame(self.content),
        }

        ctk.CTkLabel(self.sidebar, text="", height=20).pack()

        self.sidebar_buttons = {}

        for name in self.frames.keys():
            if name in ["Nhật Ký Hệ Thống", "Nhật Ký Quản Lý"]:
                continue
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {name}",
                fg_color="transparent",
                text_color="#ccc",
                hover_color="#3a3a50",
                anchor="w",
                height=45,
                font=FONT_BODY_BOLD,
                command=lambda n=name: self.switch(n),
            )
            btn.pack(pady=2, padx=15, fill="x")
            self.sidebar_buttons[name] = btn

        self.separator = ctk.CTkFrame(self.sidebar, height=2, fg_color=COLOR_BORDER)

        self.log_btn = ctk.CTkButton(
            self.sidebar,
            text="  Nhật Ký Hệ Thống",
            fg_color="transparent",
            text_color="#ccc",
            hover_color="#3a3a50",
            anchor="w",
            height=45,
            font=FONT_BODY_BOLD,
            command=lambda: self.switch("Nhật Ký Hệ Thống"),
        )
        self.sidebar_buttons["Nhật Ký Hệ Thống"] = self.log_btn

        self.mgmt_log_btn = ctk.CTkButton(
            self.sidebar,
            text="  Nhật Ký Quản Lý",
            fg_color="transparent",
            text_color="#ccc",
            hover_color="#3a3a50",
            anchor="w",
            height=45,
            font=FONT_BODY_BOLD,
            command=lambda: self.switch("Nhật Ký Quản Lý"),
        )
        self.sidebar_buttons["Nhật Ký Quản Lý"] = self.mgmt_log_btn

        self.staff_reg_btn = ctk.CTkButton(
            self.sidebar,
            text="  Cấp TK Nhân Viên",
            fg_color="transparent",
            text_color="#ccc",
            hover_color="#3a3a50",
            anchor="w",
            height=45,
            font=FONT_BODY_BOLD,
            command=self.open_staff_registration,
        )
        self.sidebar_buttons["Cấp TK Nhân Viên"] = self.staff_reg_btn

        self.voucher_grant_btn = ctk.CTkButton(
            self.sidebar,
            text="  Tặng Voucher",
            fg_color="transparent",
            text_color="#ccc",
            hover_color="#3a3a50",
            anchor="w",
            height=45,
            font=FONT_BODY_BOLD,
            command=self.open_voucher_modal,
        )
        self.sidebar_buttons["Tặng Voucher"] = self.voucher_grant_btn

        self.api_label = ctk.CTkLabel(
            self.sidebar,
            text="Tỷ giá: Chưa có dữ liệu",
            font=("Segoe UI", 12),
            text_color=COLOR_GOLD,
            anchor="w",
        )
        self.api_label.pack(side="bottom", pady=(5, 5), padx=20, fill="x")

        self.api_btn = ctk.CTkButton(
            self.sidebar,
            text="⚙ TẢI TỶ GIÁ LIVE",
            fg_color="#3a3a50",
            text_color="white",
            hover_color=COLOR_GOLD_HOVER,
            anchor="w",
            height=35,
            font=FONT_BODY_BOLD,
            command=self.fetch_api_data,
        )
        self.api_btn.pack(side="bottom", pady=5, padx=15, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="📖 HƯỚNG DẪN (PDF)",
            fg_color="#3a3a50",
            text_color="white",
            hover_color=COLOR_GOLD_HOVER,
            anchor="w",
            height=35,
            font=FONT_BODY_BOLD,
            command=self.open_pdf,
        ).pack(side="bottom", pady=5, padx=15, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="ℹ GIỚI THIỆU",
            fg_color="#3a3a50",
            text_color="white",
            hover_color=COLOR_GOLD_HOVER,
            anchor="w",
            height=35,
            font=FONT_BODY_BOLD,
            command=self.show_about,
        ).pack(side="bottom", pady=5, padx=15, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="  Đăng Xuất",
            fg_color="transparent",
            text_color="#e74c3c",
            anchor="w",
            height=45,
            font=FONT_BODY_BOLD,
            command=self.logout_clicked,
        ).pack(side="bottom", pady=(20, 5), padx=15, fill="x")

        self.switch("Lễ Tân")

    def logout_clicked(self):
        app = self.winfo_toplevel()
        func = getattr(app, "show_login", None)
        if callable(func):
            func()

    def switch(self, name):
        for f in self.frames.values():
            f.pack_forget()
            if hasattr(f, "on_hide"):
                f.on_hide()
        self.frames[name].pack(fill="both", expand=True)

        for b_name, btn in self.sidebar_buttons.items():
            if b_name == name:
                btn.configure(text_color=COLOR_GOLD)
            else:
                btn.configure(text_color="#ccc")

        if hasattr(self.frames[name], "load_data"):
            self.frames[name].load_data()

    def update_user(self, _name, role):
        self.current_role = role
        if hasattr(self, "separator") and self.separator is not None:
            self.separator.pack_forget()
        if self.staff_reg_btn is not None:
            self.staff_reg_btn.pack_forget()
        if self.voucher_grant_btn is not None:
            self.voucher_grant_btn.pack_forget()
        if hasattr(self, "log_btn") and self.log_btn is not None:
            self.log_btn.pack_forget()
        if hasattr(self, "mgmt_log_btn") and self.mgmt_log_btn is not None:
            self.mgmt_log_btn.pack_forget()

        if role == "manager":
            if hasattr(self, "separator") and self.separator is not None:
                self.separator.pack(fill="x", padx=20, pady=10)
            if hasattr(self, "log_btn") and self.log_btn is not None:
                self.log_btn.pack(pady=2, padx=15, fill="x")
            if hasattr(self, "mgmt_log_btn") and self.mgmt_log_btn is not None:
                self.mgmt_log_btn.pack(pady=2, padx=15, fill="x")
            if self.staff_reg_btn is not None:
                self.staff_reg_btn.pack(pady=2, padx=15, fill="x")
            if self.voucher_grant_btn is not None:
                self.voucher_grant_btn.pack(pady=2, padx=15, fill="x")

    def open_staff_registration(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Cấp tài khoản nhân viên")
        w, h = 450, 680
        center_window(modal, self, w, h)
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal, text="ĐĂNG KÝ NHÂN VIÊN MỚI", font=FONT_TITLE, text_color=COLOR_GOLD
        ).pack(pady=30)

        entries = {}
        fields = [
            ("Họ và Tên", "name"),
            ("Tên đăng nhập", "user"),
            ("Email liên hệ", "email"),
            ("Số điện thoại", "phone"),
            ("Mật khẩu cấp", "pw"),
        ]

        for label, key in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=8)
            ctk.CTkLabel(
                f, text=label, font=FONT_BODY_BOLD, text_color=COLOR_TEXT
            ).pack(anchor="w")
            e = ctk.CTkEntry(
                f,
                show="*" if key == "pw" else "",
                height=40,
                fg_color=COLOR_WHITE,
                border_color=COLOR_BORDER,
            )
            e.pack(fill="x", pady=5)
            entries[key] = e

        def confirm_save():
            vals = {k: v.get() for k, v in entries.items()}
            if "" in vals.values():
                return messagebox.showwarning("Chú ý", "Không được để trống thông tin!")

            try:
                hashed_pw = db.hash_password(vals["pw"], vals["user"])
                db.execute_query(
                    "INSERT INTO users (full_name, username, email, phone, password, role) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        vals["name"],
                        vals["user"],
                        vals["email"],
                        vals["phone"],
                        hashed_pw,
                        "staff",
                    ),
                    commit=True,
                )
                messagebox.showinfo(
                    "Thành công", f"Đã cấp tài khoản cho nhân viên: {vals['name']}"
                )
                modal.destroy()
            except sqlite3.Error as err:
                messagebox.showerror(
                    "Lỗi", f"Tên đăng nhập hoặc Email đã tồn tại: {str(err)}"
                )

        ctk.CTkButton(
            modal,
            text="XÁC NHẬN CẤP TÀI KHOẢN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            height=45,
            font=FONT_BODY_BOLD,
            command=confirm_save,
        ).pack(pady=40, padx=40, fill="x")

        modal.bind("<Return>", lambda event: confirm_save())

    def open_voucher_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Tặng Voucher cho khách hàng")
        w, h = 450, 620
        center_window(modal, self, w, h)
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal, text="🎁 TẶNG VOUCHER MỚI", font=FONT_TITLE, text_color=COLOR_GOLD
        ).pack(pady=30)

        res_users = db.execute_query(
            "SELECT username FROM users WHERE role='user'", fetch=True
        )
        user_list = [r[0] for r in res_users] if res_users else []
        if not user_list:
            user_list = ["Chưa có khách hàng"]

        f_user = ctk.CTkFrame(modal, fg_color="transparent")
        f_user.pack(fill="x", padx=40, pady=8)
        ctk.CTkLabel(f_user, text="Chọn khách hàng nhận:", font=FONT_BODY_BOLD).pack(
            anchor="w"
        )
        user_cb = ctk.CTkOptionMenu(
            f_user,
            values=user_list,
            height=40,
            fg_color=COLOR_WHITE,
            text_color=COLOR_TEXT,
            button_color=COLOR_GOLD,
        )
        user_cb.pack(fill="x", pady=5)

        entries = {}
        fields = [
            ("Mã Voucher (VD: GIAM50)", "code"),
            ("Nội dung (VD: Tri ân sếp)", "desc"),
            ("% Giảm giá (1-100)", "percent"),
        ]

        for label, key in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=8)
            ctk.CTkLabel(f, text=label, font=FONT_BODY_BOLD).pack(anchor="w")
            e = ctk.CTkEntry(
                f, height=40, fg_color=COLOR_WHITE, border_color=COLOR_BORDER
            )
            e.pack(fill="x", pady=5)
            entries[key] = e

        def confirm_grant():
            target = user_cb.get()
            code = entries["code"].get()
            desc = entries["desc"].get()
            perc = entries["percent"].get()

            if target == "Chưa có khách hàng" or not code or not perc:
                return messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")

            try:
                db.execute_query(
                    "INSERT INTO user_coupons (username, code, description, discount_percent) VALUES (?, ?, ?, ?)",
                    (target, code.upper(), desc, int(perc)),
                    commit=True,
                )
                messagebox.showinfo(
                    "Thành công", f"Đã tặng voucher {code} cho {target}!"
                )
                modal.destroy()
            except (sqlite3.Error, ValueError) as err:
                messagebox.showerror("Lỗi", f"Lỗi hệ thống: {str(err)}")

        ctk.CTkButton(
            modal,
            text="XÁC NHẬN TẶNG",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            height=45,
            font=FONT_BODY_BOLD,
            command=confirm_grant,
        ).pack(pady=40, padx=40, fill="x")

        modal.bind("<Return>", lambda event: confirm_grant())

    def show_about(self):
        from datetime import datetime

        current_date = datetime.now().strftime("%d/%m/%Y")
        messagebox.showinfo(
            "Giới thiệu Phần mềm",
            "Tên phần mềm: DreamStay Resort Management System\n"
            "Phiên bản: v2.5.0 Premium\n"
            "Tác giả: Nhóm Phát triển DreamStay\n"
            "Ngày phát hành: " + current_date + " (Bản cập nhật mới nhất)\n"
            "Mô tả: Hệ thống quản lý toàn diện bao gồm đặt phòng, lễ tân, dịch vụ F&B, quản lý kho hàng và báo cáo tài chính tích hợp.",
        )

    def open_pdf(self):
        try:
            webbrowser.open("user_guide.pdf")
        except Exception:
            messagebox.showerror(
                "Lỗi", "Không thể mở file tài liệu hướng dẫn sử dụng user_guide.pdf!"
            )

    def fetch_api_data(self):
        self.api_btn.configure(state="disabled")
        loading_win = ctk.CTkToplevel(self)
        loading_win.title("Đang xử lý")
        w, h = 300, 150
        center_window(loading_win, self, w, h)
        loading_win.configure(fg_color=COLOR_CREAM)
        loading_win.transient(self.winfo_toplevel())
        loading_win.grab_set()

        ctk.CTkLabel(
            loading_win,
            text="🔄 Đang tải dữ liệu từ REST API...",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT,
        ).pack(pady=30)

        progress = ctk.CTkProgressBar(loading_win, width=200, progress_color=COLOR_GOLD)
        progress.pack(pady=5)
        progress.start()

        def worker():
            time.sleep(1.0)
            try:
                response = requests.get(
                    "https://open.er-api.com/v6/latest/USD", timeout=5
                )
                if response.status_code == 401:
                    raise PermissionError("Unauthorized access (401)")
                if response.status_code != 200:
                    raise ConnectionError(f"HTTP Error {response.status_code}")

                data = response.json()
                rates = data.get("rates", {})
                vnd_rate = rates.get("VND", 25000.0)
                vnd_f = f"{int(vnd_rate):,}".replace(",", ".")

                def success_ui():
                    self.api_label.configure(text=f"Tỷ giá: 1 USD = {vnd_f} VND")
                    try:
                        loading_win.grab_release()
                    except:
                        pass
                    try:
                        loading_win.destroy()
                    except:
                        pass
                    self.api_btn.configure(state="normal")
                    messagebox.showinfo(
                        "Thành công",
                        f"Đã cập nhật tỷ giá thực tế hôm nay: 1 USD = {vnd_f} VNĐ",
                        parent=self.winfo_toplevel(),
                    )

                self.after(0, success_ui)

            except requests.exceptions.Timeout:

                def error_ui():
                    try:
                        loading_win.grab_release()
                    except:
                        pass
                    try:
                        loading_win.destroy()
                    except:
                        pass
                    self.api_btn.configure(state="normal")
                    messagebox.showerror(
                        "Lỗi kết nối",
                        "Hết thời gian chờ phản hồi (Timeout)! Xin sếp vui lòng kiểm tra lại đường truyền mạng.",
                        parent=self.winfo_toplevel(),
                    )

                self.after(0, error_ui)

            except PermissionError:

                def error_ui():
                    try:
                        loading_win.grab_release()
                    except:
                        pass
                    try:
                        loading_win.destroy()
                    except:
                        pass
                    self.api_btn.configure(state="normal")
                    messagebox.showerror(
                        "Lỗi xác thực",
                        "Yêu cầu API bị từ chối do lỗi xác thực người dùng (Mã 401 Unauthorized)!",
                        parent=self.winfo_toplevel(),
                    )

                self.after(0, error_ui)

            except Exception as e:
                error_msg = str(e)

                def error_ui():
                    try:
                        loading_win.grab_release()
                    except:
                        pass
                    try:
                        loading_win.destroy()
                    except:
                        pass
                    self.api_btn.configure(state="normal")
                    messagebox.showerror(
                        "Lỗi hệ thống",
                        f"Không thể lấy thông tin tỷ giá trực tuyến: {error_msg}",
                        parent=self.winfo_toplevel(),
                    )

                self.after(0, error_ui)

        threading.Thread(target=worker, daemon=True).start()

    def load_data(self):
        pass
