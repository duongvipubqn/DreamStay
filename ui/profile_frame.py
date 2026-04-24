import customtkinter as ctk
from tkinter import messagebox
from config import *
from database import db


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.app = master.master

        self.panel = ctk.CTkFrame(self, width=500, height=650, fg_color=COLOR_WHITE,
                                  corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="Hồ Sơ Của Bạn", font=("Segoe UI", 32, "bold"),
                     text_color=COLOR_GOLD).pack(pady=(40, 10))

        ctk.CTkLabel(self.panel, text="👤", font=("Segoe UI", 100)).pack(pady=10)

        self.info_label = ctk.CTkLabel(self.panel, text="Sếp: Đang tải...", font=("Segoe UI", 20, "bold"),
                                       text_color=COLOR_TEXT)
        self.info_label.pack(pady=10)

        self.email_label = ctk.CTkLabel(self.panel, text="Email: ...", font=("Segoe UI", 14), text_color="#aaa")
        self.email_label.pack()

        self.phone_label = ctk.CTkLabel(self.panel, text="SĐT: ...", font=("Segoe UI", 14), text_color="#aaa")
        self.phone_label.pack(pady=5)

        btn_f = ctk.CTkFrame(self.panel, fg_color="transparent")
        btn_f.pack(pady=40)

        ctk.CTkButton(btn_f, text="CHỈNH SỬA THÔNG TIN", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"), width=200, height=40,
                      command=self.open_edit_modal).pack(pady=10)

        ctk.CTkButton(btn_f, text="ĐĂNG XUẤT", fg_color="#e74c3c", hover_color="#c0392b",
                      text_color="white", font=("Segoe UI", 13, "bold"), width=200, height=40,
                      command=self.app.logout).pack(pady=10)

    def load_data(self):
        if self.app.current_user:
            db.cursor.execute("SELECT full_name, email, phone FROM users WHERE full_name=?", (self.app.current_user,))
            res = db.cursor.fetchone()
            if res:
                self.info_label.configure(text=f"Sếp: {res[0].upper()}")
                self.email_label.configure(text=f"Email: {res[1]}")
                self.phone_label.configure(text=f"Số điện thoại: {res[2]}")

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
                self.app.pages["Quản lý"].update_user(new_name)
                modal.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật hồ sơ sếp!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")

        ctk.CTkButton(modal, text="LƯU THAY ĐỔI", fg_color=COLOR_GOLD, height=45, command=save).pack(pady=30, padx=40,
                                                                                                     fill="x")