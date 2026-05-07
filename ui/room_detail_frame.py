import os
from config import *
from PIL import Image
from datetime import datetime, timedelta
from tkinter import messagebox
from database import db
from tkcalendar import Calendar

class RoomDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.room_data = None
        self.img_path = None
        self.right_p = None
        self.entry_in = None
        self.entry_out = None
        self.lbl_total = None
        self.btn_book = None

    def set_room(self, data, img_path):
        self.room_data = data
        self.img_path = img_path
        for widget in self.winfo_children():
            widget.destroy()

        def go_back():
            app = self.winfo_toplevel()
            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Phòng")

        ctk.CTkButton(self, text="← QUAY LẠI DANH SÁCH", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 13, "bold"),
                      command=go_back).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        left_p = ctk.CTkFrame(main_container, fg_color="transparent")
        left_p.pack(side="left", padx=30, pady=30, anchor="n")

        if os.path.exists(img_path):
            pil_img = Image.open(img_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(500, 350))
            ctk.CTkLabel(left_p, image=ctk_img, text="").pack()

        self.right_p = ctk.CTkFrame(main_container, fg_color="transparent")
        self.right_p.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(self.right_p, text=data[2], font=("Segoe UI", 32, "bold"), text_color=COLOR_GOLD).pack(anchor="w")

        info_f = ctk.CTkFrame(self.right_p, fg_color="transparent")
        info_f.pack(fill="x", pady=10)

        ctk.CTkLabel(info_f, text=f"Mã phòng: {data[0]}", font=("Segoe UI", 14), text_color="#888").pack(anchor="w")

        details = [
            (f"📍 Địa điểm: {data[1]}", COLOR_TEXT),
            (f"👥 Sức chứa: {data[4]}", COLOR_TEXT),
            (f"💳 Giá niêm yết: {data[5]:,.0f} VNĐ / đêm", COLOR_GOLD),
            (f"✨ Trạng thái: {data[3]}", "#2ecc71" if data[3] == "Trống" else "#e74c3c")
        ]

        for txt, clr in details:
            ctk.CTkLabel(info_f, text=txt, font=("Segoe UI", 16), text_color=clr).pack(anchor="w", pady=2)

        desc_txt = ("Trải nghiệm không gian nghỉ dưỡng đẳng cấp tại DreamStay. \n"
                    "Phòng được trang bị nội thất cao cấp, hệ thống điều hòa trung tâm, \n"
                    "tivi màn hình lớn và ban công với tầm nhìn tuyệt đẹp. \n"
                    "Dịch vụ dọn phòng 24/7 đảm bảo không gian luôn sạch sẽ và thơm mát.")
        ctk.CTkLabel(self.right_p, text=desc_txt, font=("Segoe UI", 14), text_color="#aaa", justify="left").pack(
            anchor="w", pady=(15, 0))

        booking_f = ctk.CTkFrame(self.right_p, fg_color=COLOR_NAVY, corner_radius=10)
        booking_f.pack(fill="x", pady=25)

        date_grid = ctk.CTkFrame(booking_f, fg_color="transparent")
        date_grid.pack(pady=15, padx=20, fill="x")

        f1 = ctk.CTkFrame(date_grid, fg_color="transparent")
        f1.pack(side="left", expand=True)
        ctk.CTkLabel(f1, text="Ngày nhận", font=("Segoe UI", 11, "bold"), text_color="#aaa").pack()
        self.entry_in = ctk.CTkEntry(f1, placeholder_text="Chọn ngày", width=150, height=35, state="readonly")
        self.entry_in.pack(pady=5)
        self.entry_in.bind("<Button-1>", lambda e: self.open_calendar(self.entry_in))
        self.entry_in.configure(state="normal")
        self.entry_in.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_in.configure(state="readonly")

        f2 = ctk.CTkFrame(date_grid, fg_color="transparent")
        f2.pack(side="left", expand=True)
        ctk.CTkLabel(f2, text="Ngày trả", font=("Segoe UI", 11, "bold"), text_color="#aaa").pack()
        self.entry_out = ctk.CTkEntry(f2, placeholder_text="Chọn ngày", width=150, height=35, state="readonly")
        self.entry_out.pack(pady=5)
        self.entry_out.bind("<Button-1>", lambda e: self.open_calendar(self.entry_out))

        tomorrow = datetime.now() + timedelta(days=1)
        self.entry_out.configure(state="normal")
        self.entry_out.insert(0, tomorrow.strftime("%d/%m/%Y"))
        self.entry_out.configure(state="readonly")

        calc_f = ctk.CTkFrame(booking_f, fg_color="transparent")
        calc_f.pack(fill="x", padx=20, pady=(0, 15))

        self.lbl_total = ctk.CTkLabel(calc_f, text="Vui lòng chọn ngày để tính tiền", font=("Segoe UI", 16, "italic"),
                                      text_color="#888")
        self.lbl_total.pack(side="right")

        self.calculate_total()

        self.btn_book = ctk.CTkButton(self.right_p, text="XÁC NHẬN ĐẶT PHÒNG NGAY", fg_color=COLOR_GOLD,
                                      hover_color=COLOR_GOLD_HOVER, height=50, width=300,
                                      font=("Segoe UI", 14, "bold"), command=self.process_booking)
        self.btn_book.pack(anchor="w")

    def open_calendar(self, target_entry):
        top = ctk.CTkToplevel(self)
        top.title("Chọn ngày")
        top.geometry("320x400")
        top.configure(fg_color=COLOR_CREAM)
        top.transient(self.winfo_toplevel())
        top.grab_set()
        top.resizable(False, False)

        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy',
                       background=COLOR_NAVY, foreground='white',
                       selectbackground=COLOR_GOLD,
                       headersbackground=COLOR_WHITE,
                       headersforeground=COLOR_NAVY)
        cal.pack(pady=20, padx=20, fill="both", expand=True)

        def select_date():
            target_entry.configure(state="normal")
            target_entry.delete(0, "end")
            target_entry.insert(0, cal.get_date())
            target_entry.configure(state="readonly")
            top.destroy()
            self.calculate_total()

        ctk.CTkButton(top, text="XÁC NHẬN", fg_color=COLOR_GOLD,
                      hover_color=COLOR_GOLD_HOVER, command=select_date).pack(pady=20)

    def calculate_total(self):
        try:
            d_in_str = self.entry_in.get()
            d_out_str = self.entry_out.get()
            if not d_in_str or not d_out_str: return None

            d1 = datetime.strptime(d_in_str, "%d/%m/%Y")
            d2 = datetime.strptime(d_out_str, "%d/%m/%Y")
            days = (d2 - d1).days
            if days <= 0: raise ValueError

            total = days * self.room_data[5]
            self.lbl_total.configure(text=f"Tổng ({days} đêm): {total:,.0f} VNĐ", font=("Segoe UI", 18, "bold"),
                                     text_color="white")
            return total
        except (ValueError, TypeError, AttributeError):
            self.lbl_total.configure(text="Ngày không hợp lệ", text_color="#e74c3c")
            return None

    def process_booking(self):
        app = self.winfo_toplevel()
        curr_user = getattr(app, "current_user", None)
        if not curr_user:
            return messagebox.showwarning("Thông báo", "Sếp vui lòng đăng nhập để đặt phòng!")

        total = self.calculate_total()
        if total is None: return None

        try:
            d_in_dt = datetime.strptime(self.entry_in.get(), "%d/%m/%Y")
            d_out_dt = datetime.strptime(self.entry_out.get(), "%d/%m/%Y")
            stay_days = (d_out_dt - d_in_dt).days

            level, limits = db.get_user_level_info(curr_user)
            active_bookings = db.count_active_bookings(curr_user)

            if stay_days > limits["max_days"]:
                return messagebox.showerror("Từ chối", f"Tối đa {limits['max_days']} ngày cho hạng {limits['label']}")

            if active_bookings >= limits["max_rooms"]:
                return messagebox.showerror("Từ chối",
                                            f"Hạng {limits['label']} chỉ được đặt tối đa {limits['max_rooms']} phòng!")

            d_in = d_in_dt.strftime("%Y-%m-%d")
            d_out = d_out_dt.strftime("%Y-%m-%d")

            if not db.is_room_available(self.room_data[0], d_in, d_out):
                return messagebox.showerror("Hết chỗ", "Khoảng thời gian này đã có người đặt!")

            db.cursor.execute("""
                INSERT INTO bookings (customer_name, room_id, checkin_date, checkout_date, total_price, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (curr_user, self.room_data[0], d_in, d_out, total, "Pending"))
            db.conn.commit()

            messagebox.showinfo("Thành công", f"Yêu cầu đặt phòng {self.room_data[0]} đã được gửi!")

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Phòng")

        except (ValueError, Exception) as e:
            messagebox.showerror("Lỗi", f"Không thể đặt phòng: {str(e)}")

    def load_data(self):
        pass