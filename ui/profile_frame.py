import customtkinter as ctk
from tkinter import messagebox, ttk
from config import *
from database import db


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.app = master.master

        self.panel = ctk.CTkFrame(self, width=900, height=700, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")
        self.panel.pack_propagate(False)

        self.tabview = ctk.CTkTabview(self.panel, fg_color="transparent",
                                      segmented_button_selected_color=COLOR_GOLD,
                                      segmented_button_selected_hover_color=COLOR_GOLD_HOVER)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_info = self.tabview.add("👤 THÔNG TIN")
        self.tab_history = self.tabview.add("📜 LỊCH SỬ ĐẶT")
        self.tab_coupons = self.tabview.add("🎁 KHO VOUCHER")

        self.setup_info_tab()
        self.setup_history_tab()
        self.setup_coupons_tab()

    def setup_info_tab(self):
        container = ctk.CTkFrame(self.tab_info, fg_color="transparent")
        container.pack(expand=True)

        ctk.CTkLabel(container, text="👤", font=("Segoe UI", 100)).pack()
        self.info_label = ctk.CTkLabel(container, text="Sếp: ...", font=("Segoe UI", 24, "bold"), text_color=COLOR_GOLD)
        self.info_label.pack(pady=10)

        self.email_label = ctk.CTkLabel(container, text="Email: ...", font=("Segoe UI", 14), text_color="#aaa")
        self.email_label.pack()

        self.phone_label = ctk.CTkLabel(container, text="SĐT: ...", font=("Segoe UI", 14), text_color="#aaa")
        self.phone_label.pack(pady=5)

        btn_f = ctk.CTkFrame(container, fg_color="transparent")
        btn_f.pack(pady=30)

        ctk.CTkButton(btn_f, text="CHỈNH SỬA HỒ SƠ", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"), width=180, height=40,
                      command=self.open_edit_modal).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="ĐĂNG XUẤT", fg_color="#e74c3c", hover_color="#c0392b",
                      text_color="white", font=("Segoe UI", 13, "bold"), width=180, height=40,
                      command=self.app.logout).pack(side="left", padx=10)

    def setup_history_tab(self):
        cols = ("Mã", "Phòng", "Ngày Nhận", "Ngày Trả", "Tổng Tiền", "Trạng Thái")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background=COLOR_NAVY, foreground="white",
                        fieldbackground=COLOR_NAVY, rowheight=35, borderwidth=0)
        style.map('Custom.Treeview', background=[('selected', COLOR_GOLD)])

        self.tree = ttk.Treeview(self.tab_history, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_coupons_tab(self):
        self.coupon_scroll = ctk.CTkScrollableFrame(self.tab_coupons, fg_color="transparent")
        self.coupon_scroll.pack(fill="both", expand=True)

    def load_data(self):
        if not self.app.current_user: return

        db.cursor.execute("SELECT full_name, email, phone, username FROM users WHERE full_name=?",
                          (self.app.current_user,))
        user_res = db.cursor.fetchone()
        if user_res:
            self.info_label.configure(text=f"Tài khoản: {user_res[0].upper()}")
            self.email_label.configure(text=f"Email: {user_res[1]}")
            self.phone_label.configure(text=f"Số điện thoại: {user_res[2]}")
            username = user_res[3]

            for i in self.tree.get_children(): self.tree.delete(i)
            db.cursor.execute(
                "SELECT id, room_id, checkin_date, checkout_date, total_price, status FROM bookings WHERE customer_name=?",
                (self.app.current_user,))
            for row in db.cursor.fetchall():
                self.tree.insert("", "end", values=row)

            for w in self.coupon_scroll.winfo_children(): w.destroy()
            db.cursor.execute("SELECT code, description, discount_percent FROM user_coupons WHERE username=?",
                              (username,))
            coupons = db.cursor.fetchall()
            if not coupons:
                ctk.CTkLabel(self.coupon_scroll, text="Bạn chưa có voucher nào. Hãy tham gia sự kiện để nhận quà!",
                             font=("Segoe UI", 14), text_color="#888").pack(pady=50)
            else:
                for code, desc, disc in coupons:
                    f = ctk.CTkFrame(self.coupon_scroll, fg_color=COLOR_NAVY, corner_radius=10)
                    f.pack(fill="x", pady=5, padx=10)
                    ctk.CTkLabel(f, text="🎟️", font=("Segoe UI", 30)).pack(side="left", padx=20)
                    txt_f = ctk.CTkFrame(f, fg_color="transparent")
                    txt_f.pack(side="left", fill="both", expand=True, pady=10)
                    ctk.CTkLabel(txt_f, text=f"Code: {code} (-{disc}%)", font=("Segoe UI", 16, "bold"),
                                 text_color=COLOR_GOLD).pack(anchor="w")
                    ctk.CTkLabel(txt_f, text=desc, font=("Segoe UI", 12), text_color="#ccc").pack(anchor="w")
                    ctk.CTkButton(f, text="DÙNG NGAY", width=100, fg_color="transparent", border_width=1,
                                  border_color=COLOR_GOLD, text_color=COLOR_GOLD).pack(side="right", padx=20)

    def open_edit_modal(self):
        db.cursor.execute("SELECT full_name, email, phone, username FROM users WHERE full_name=?",
                          (self.app.current_user,))
        data = db.cursor.fetchone()
        if not data: return

        modal = ctk.CTkToplevel(self)
        modal.title("Chỉnh sửa hồ sơ")
        modal.geometry("400x500")
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self)
        modal.grab_set()

        ctk.CTkLabel(modal, text="CẬP NHẬT THÔNG TIN", font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(
            pady=20)

        entries = {}
        fields = [("Họ và Tên", data[0]), ("Email", data[1]), ("Số điện thoại", data[2])]

        for label, val in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=10)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 12), text_color=COLOR_TEXT).pack(anchor="w")
            e = ctk.CTkEntry(f, fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color=COLOR_TEXT, height=40)
            e.insert(0, val)
            e.pack(fill="x", pady=5)
            entries[label] = e

        def save():
            new_name = entries["Họ và Tên"].get()
            new_email = entries["Email"].get()
            new_phone = entries["Số điện thoại"].get()

            if not new_name or not new_email:
                return messagebox.showwarning("Lỗi", "Không được để trống Tên hoặc Email!")

            try:
                db.cursor.execute("UPDATE users SET full_name=?, email=?, phone=? WHERE full_name=?",
                                  (new_name, new_email, new_phone, self.app.current_user))
                db.conn.commit()
                self.app.current_user = new_name
                self.load_data()
                self.app.pages["Quản lý"].update_user(new_name, self.app.current_role)
                modal.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật hồ sơ sếp!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

        ctk.CTkButton(modal, text="LƯU THAY ĐỔI", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 14, "bold"), height=45, command=save).pack(pady=30, padx=40,
                                                                                                       fill="x")