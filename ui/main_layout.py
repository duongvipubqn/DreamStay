import customtkinter as ctk
from config import *
from ui.reception import ReceptionFrame
from ui.crud_frame import CRUDFrame
from ui.statistics import StatisticsFrame
from tkinter import messagebox
from database import db


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=COLOR_NAVY, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.frames = {
            "Lễ Tân": ReceptionFrame(self.content),
            "Phòng": CRUDFrame(self.content, "Hệ Thống Quản Lý Phòng", "rooms",
                               ["Mã Phòng", "Địa điểm", "Loại Phòng", "Tình Trạng", "Sức Chứa", "Giá (VNĐ)"]),
            "Khách Hàng": CRUDFrame(self.content, "Quản lý Khách hàng (CRM)", "customers",
                                    ["Mã KH", "Họ và Tên", "Email", "Số Điện Thoại", "Thành phố", "Tổng chi tiêu"]),
            "Nhân Viên": CRUDFrame(self.content, "Quản lý Nhân sự (HRM)", "employees",
                                   ["Mã NV", "Họ và Tên", "Chức vụ", "Địa điểm", "Số Điện Thoại", "Lương (VNĐ)",
                                    "Trạng thái"]),
            "Thống Kê": StatisticsFrame(self.content)
        }

        ctk.CTkLabel(self.sidebar, text="", height=20).pack()

        for name in self.frames.keys():
            btn = ctk.CTkButton(self.sidebar, text=f"  {name}",
                                fg_color="transparent",
                                text_color="#ccc",
                                hover_color="#3a3a50",
                                anchor="w",
                                height=45,
                                font=("Segoe UI", 13, "bold"),
                                command=lambda n=name: self.switch(n))
            btn.pack(pady=2, padx=15, fill="x")

        self.staff_reg_btn = ctk.CTkButton(self.sidebar, text="  Cấp TK Nhân Viên",
                                           fg_color=COLOR_GOLD, text_color="white",
                                           hover_color=COLOR_GOLD_HOVER,
                                           anchor="w", height=45, font=("Segoe UI", 13, "bold"),
                                           command=self.open_staff_registration)

        self.voucher_grant_btn = ctk.CTkButton(self.sidebar, text="  Tặng Voucher",
                                               fg_color="#27ae60", text_color="white",
                                               hover_color="#219150",
                                               anchor="w", height=45, font=("Segoe UI", 13, "bold"),
                                               command=self.open_voucher_modal)

        ctk.CTkButton(self.sidebar, text="  Đăng Xuất",
                      fg_color="transparent", text_color="#e74c3c",
                      anchor="w", height=45, font=("Segoe UI", 13, "bold"),
                      command=self.logout_clicked).pack(side="bottom", pady=20, padx=15, fill="x")

        self.switch("Lễ Tân")

    def logout_clicked(self):
        self.master.master.show_login()

    def switch(self, name):
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        if hasattr(self.frames[name], 'load_data'):
            self.frames[name].load_data()

    def update_user(self, name, role):
        self.current_role = role
        if role == "manager":
            self.staff_reg_btn.pack(pady=2, padx=15, fill="x", before=self.sidebar.winfo_children()[-1])
            self.voucher_grant_btn.pack(pady=2, padx=15, fill="x", before=self.sidebar.winfo_children()[-1])
        else:
            self.staff_reg_btn.pack_forget()
            self.voucher_grant_btn.pack_forget()

    def open_staff_registration(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Cấp tài khoản nhân viên")
        modal.geometry("450x600")
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self)
        modal.grab_set()
        modal.resizable(False, False)

        ctk.CTkLabel(modal, text="ĐĂNG KÝ NHÂN VIÊN MỚI", font=("Segoe UI", 22, "bold"), text_color=COLOR_GOLD).pack(
            pady=30)

        entries = {}
        fields = [
            ("Họ và Tên", "name"),
            ("Tên đăng nhập", "user"),
            ("Email liên hệ", "email"),
            ("Số điện thoại", "phone"),
            ("Mật khẩu cấp", "pw")
        ]

        for label, key in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=8)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT).pack(anchor="w")
            e = ctk.CTkEntry(f, show="*" if key == "pw" else "", height=40, fg_color=COLOR_WHITE,
                             border_color=COLOR_BORDER)
            e.pack(fill="x", pady=5)
            entries[key] = e

        def confirm_save():
            vals = {k: v.get() for k, v in entries.items()}
            if "" in vals.values():
                return messagebox.showwarning("Chú ý", "Không được để trống thông tin!")

            try:
                hashed_pw = db.hash_password(vals["pw"])
                db.cursor.execute("""
                                  INSERT INTO users (full_name, username, email, phone, password, role)
                                  VALUES (?, ?, ?, ?, ?, ?)
                                  """, (vals["name"], vals["user"], vals["email"], vals["phone"], hashed_pw, "staff"))
                db.conn.commit()
                messagebox.showinfo("Thành công", f"Đã cấp tài khoản cho nhân viên: {vals['name']}")
                modal.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc Email đã tồn tại trên hệ thống!")

        ctk.CTkButton(modal, text="XÁC NHẬN CẤP TÀI KHOẢN", fg_color=COLOR_GOLD,
                      hover_color=COLOR_GOLD_HOVER, height=45, font=("Segoe UI", 13, "bold"),
                      command=confirm_save).pack(pady=40, padx=40, fill="x")

    def open_voucher_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Tặng Voucher cho khách hàng")
        modal.geometry("450x550")
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self)
        modal.grab_set()

        ctk.CTkLabel(modal, text="🎁 TẶNG VOUCHER MỚI", font=("Segoe UI", 22, "bold"), text_color=COLOR_GOLD).pack(
            pady=30)

        # Lấy danh sách username từ DB
        db.cursor.execute("SELECT username FROM users WHERE role='user'")
        user_list = [r[0] for r in db.cursor.fetchall()]
        if not user_list: user_list = ["Chưa có khách hàng"]

        f_user = ctk.CTkFrame(modal, fg_color="transparent")
        f_user.pack(fill="x", padx=40, pady=8)
        ctk.CTkLabel(f_user, text="Chọn khách hàng nhận:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        user_cb = ctk.CTkOptionMenu(f_user, values=user_list, height=40, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                                    button_color=COLOR_GOLD)
        user_cb.pack(fill="x", pady=5)

        entries = {}
        fields = [("Mã Voucher (VD: GIAM50)", "code"), ("Nội dung (VD: Tri ân sếp)", "desc"),
                  ("% Giảm giá (1-100)", "percent")]

        for label, key in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=8)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 12, "bold")).pack(anchor="w")
            e = ctk.CTkEntry(f, height=40, fg_color=COLOR_WHITE, border_color=COLOR_BORDER)
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
                db.cursor.execute("""
                                  INSERT INTO user_coupons (username, code, description, discount_percent)
                                  VALUES (?, ?, ?, ?)
                                  """, (target, code.upper(), desc, int(perc)))
                db.conn.commit()
                messagebox.showinfo("Thành công", f"Đã tặng voucher {code} cho {target}!")
                modal.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi hệ thống: {str(e)}")

        ctk.CTkButton(modal, text="XÁC NHẬN TẶNG", fg_color="#27ae60", hover_color="#219150",
                      height=45, font=("Segoe UI", 13, "bold"), command=confirm_grant).pack(pady=40, padx=40, fill="x")