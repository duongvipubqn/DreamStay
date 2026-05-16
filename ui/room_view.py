import os
from config import *
from PIL import Image
from database import db
from datetime import datetime, timedelta
from tkinter import messagebox
from tkcalendar import Calendar

class RoomView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(self, master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Phòng Nghỉ Của Chúng Tôi", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(
            pady=30)

        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", padx=50, pady=(0, 20))

        self.filter_container = ctk.CTkFrame(self.filter_frame, fg_color="transparent")
        self.filter_container.pack(anchor="center", pady=10)

        self.filter_vars = {}
        filters = [
            ("Địa điểm", ["Mọi địa điểm"] + LOCATIONS),
            ("Loại phòng", ["Mọi loại phòng"] + ROOM_TYPES),
            ("Số khách", ["Mọi số khách"] + CAPACITIES),
            ("Mức giá (VNĐ)", ["Mọi mức giá", "Dưới 3tr", "3tr - 6tr", "Trên 10tr"]),
            ("Trạng thái", ["Mọi trạng thái", "Trống", "Đã đặt"])
        ]

        for label, vals in filters:
            f = ctk.CTkFrame(self.filter_container, fg_color="transparent")
            f.pack(side="left", padx=12)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color="#aaa").pack(anchor="w")

            var = ctk.StringVar(value=vals[0])
            self.filter_vars[label] = var
            ctk.CTkOptionMenu(f, values=vals, variable=var, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                              button_color=COLOR_GOLD, width=150, height=35, dynamic_resizing=False).pack(pady=(5, 0))

        self.apply_btn = ctk.CTkButton(self.filter_container, text="LỌC PHÒNG",
                                       width=140, height=45, fg_color=COLOR_GOLD,
                                       hover_color=COLOR_GOLD_HOVER, text_color="white",
                                       command=self.apply_filter)
        self.apply_btn.pack(side="left", padx=(15, 0), pady=(18, 0))

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=50)

        for col in range(2):
            self.grid_frame.grid_columnconfigure(col, weight=1, uniform="column_group")

        self.page_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.page_frame.pack(pady=10)

        self.prev_btn = ctk.CTkButton(self.page_frame, text="Trước", command=self.prev_page, state="disabled")
        self.prev_btn.pack(side="left", padx=10)

        self.page_label = ctk.CTkLabel(self.page_frame, text="Trang 1 / 1", font=("Segoe UI", 14))
        self.page_label.pack(side="left", padx=20)

        self.next_btn = ctk.CTkButton(self.page_frame, text="Sau", command=self.next_page, state="disabled")
        self.next_btn.pack(side="left", padx=10)

        self.image_map = {
            "Deluxe Hướng Biển": "room-deluxe-ocean.png",
            "Suite Cao Cấp": "room-luxury-suite.png",
            "Villa Gia Đình Cổ Điển": "room-classic-villa.png",
            "Standard Hướng Vườn": "room-standard-garden.png",
            "Presidential Suite": "room-presidential.png"
        }
        self.ctk_image_cache = {}
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = 1
        self.filters = None

    def _get_room_bookings(self, room_id):
        raw_bookings = db.get_room_bookings(room_id)
        parsed = []
        for checkin, checkout, status in raw_bookings:
            try:
                start = datetime.strptime(checkin, "%Y-%m-%d").date()
                end = datetime.strptime(checkout, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            parsed.append((start, end, status))
        return parsed

    def _get_room_status_info(self, room_id):
        today = datetime.now().date()
        bookings = self._get_room_bookings(room_id)
        current_booking = any(start <= today < end and status != "Cancelled" for start, end, status in bookings)
        upcoming = [
            (start, end) for start, end, status in bookings
            if status != "Cancelled" and end > today
        ]
        upcoming.sort()
        return current_booking, upcoming

    def _format_booking_summary(self, upcoming):
        if not upcoming:
            return "Chưa có lịch đặt"

        formatted = [f"{start.strftime('%d/%m')} - {end.strftime('%d/%m')}" for start, end in upcoming[:2]]
        if len(upcoming) > 2:
            formatted.append(f"+{len(upcoming) - 2} lịch khác")
        return ", ".join(formatted)

    def load_data(self, filters=None, page=1):
        self.current_page = page
        self.filters = filters

        if filters:
            mapping = {
                "location": "Địa điểm",
                "type": "Loại phòng",
                "capacity": "Số khách",
                "price": "Mức giá (VNĐ)",
                "status": "Trạng thái"
            }
            for key, label in mapping.items():
                if label in self.filter_vars:
                    self.filter_vars[label].set(filters.get(key, self.filter_vars[label].get()))

        query = "SELECT room_id, location, room_type, status, capacity, price FROM rooms WHERE 1=1"
        params = []

        if filters:
            if filters["location"] != "Mọi địa điểm":
                query += " AND location = ?"
                params.append(filters["location"])

            if filters["type"] != "Mọi loại phòng":
                query += " AND room_type = ?"
                params.append(filters["type"])

            if filters["capacity"] != "Mọi số khách":
                query += " AND capacity = ?"
                params.append(filters["capacity"])

            p_range = filters["price"]
            if p_range == "Dưới 3tr":
                query += " AND price < 3000000"
            elif p_range == "3tr - 6tr":
                query += " AND price BETWEEN 3000000 AND 6000000"
            elif p_range == "Trên 10tr":
                query += " AND price > 10000000"

        db.cursor.execute(query, params)
        rooms_db = db.cursor.fetchall()

        status_filter = None
        if filters and filters.get("status") and filters["status"] != "Mọi trạng thái":
            status_filter = filters["status"]

        filtered_rooms = []
        for room in rooms_db:
            room_id = room[0]
            current_booking, _ = self._get_room_status_info(room_id)
            is_currently_booked = current_booking
            if status_filter == "Trống" and is_currently_booked:
                continue
            if status_filter == "Đã đặt" and not is_currently_booked:
                continue
            filtered_rooms.append(room)

        count = len(filtered_rooms)
        self.total_pages = max(1, (count + self.items_per_page - 1) // self.items_per_page)

        if page > self.total_pages:
            page = self.total_pages
        if page < 1:
            page = 1
        self.current_page = page

        offset = (page - 1) * self.items_per_page
        rooms_db = filtered_rooms[offset:offset + self.items_per_page]

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()
        if window_width < 100: window_width = 1300

        card_width = (window_width - 130) // 2
        img_w = int(card_width * 0.92)
        img_h = int(img_w * 0.62)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")

        if not rooms_db:
            ctk.CTkLabel(self.grid_frame, text="Rất tiếc, không tìm thấy phòng phù hợp với yêu cầu của sếp!",
                         font=("Segoe UI", 16), text_color=COLOR_GOLD).pack(pady=50)
        else:
            for i, (r_id, loc, r_type, status, cap, price) in enumerate(rooms_db):
                card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1,
                                    border_color=COLOR_BORDER)
                card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

                img_name = self.image_map.get(r_type, "default.png")
                cache_key = f"{img_name}_{img_w}"

                if cache_key not in self.ctk_image_cache:
                    img_path = os.path.join(img_dir, img_name)
                    if os.path.exists(img_path):
                        try:
                            pil_img = Image.open(img_path)
                            self.ctk_image_cache[cache_key] = ctk.CTkImage(light_image=pil_img, dark_image=pil_img,
                                                                           size=(img_w, img_h))
                        except (IOError, OSError, TypeError, ValueError):
                            self.ctk_image_cache[cache_key] = None
                    else:
                        self.ctk_image_cache[cache_key] = None

                ctk_img = self.ctk_image_cache[cache_key]
                if ctk_img:
                    ctk.CTkLabel(card, image=ctk_img, text="").pack(pady=10, padx=10, fill="x")
                else:
                    ctk.CTkLabel(card, text="[ Ảnh chưa cập nhật ]", width=img_w, height=img_h).pack()

                header_f = ctk.CTkFrame(card, fg_color="transparent")
                header_f.pack(fill="x", padx=20)
                ctk.CTkLabel(header_f, text=f"Mã: {r_id}", font=("Segoe UI", 11, "bold"), text_color="#888").pack(
                    side="left")

                current_booking, upcoming_bookings = self._get_room_status_info(r_id)
                current_text = "Đang đặt" if current_booking else "Trống"
                status_color = "#e74c3c" if current_booking else "#2ecc71"
                ctk.CTkLabel(header_f, text=current_text, font=("Segoe UI", 10, "bold"), text_color=status_color).pack(
                    side="right")

                ctk.CTkLabel(card, text=r_type, font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(pady=(5, 0))
                ctk.CTkLabel(card, text=f"📍 {loc} | 👥 {cap}", font=("Segoe UI", 12), text_color="#aaa").pack()
                ctk.CTkLabel(card, text=f"{price:,.0f} VNĐ / đêm", font=("Segoe UI", 16, "bold"),
                             text_color=COLOR_GOLD).pack(pady=10)

                if upcoming_bookings:
                    ctk.CTkLabel(card, text=f"Lịch đặt: {self._format_booking_summary(upcoming_bookings)}",
                                 font=("Segoe UI", 12), text_color="#888").pack(padx=20, pady=(0, 10), anchor="w")
                else:
                    ctk.CTkLabel(card, text="Chưa có lịch đặt", font=("Segoe UI", 12), text_color="#888").pack(
                                 padx=20, pady=(0, 10), anchor="w")

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(pady=(0, 20), padx=20, fill="x")

                ctk.CTkButton(btn_frame, text="CHI TIẾT",
                              fg_color="#3a3a50", text_color="white",
                              font=("Segoe UI", 11, "bold"), height=35, width=80,
                              command=lambda d=rooms_db[i], p=os.path.join(img_dir, img_name): self.show_details(d, p)).pack(
                    side="left", padx=(0, 5), expand=True, fill="x")

                ctk.CTkButton(btn_frame, text="ĐẶT PHÒNG",
                              fg_color=COLOR_GOLD, text_color="white", hover_color=COLOR_GOLD_HOVER,
                              font=("Segoe UI", 11, "bold"), height=35, width=80,
                              command=lambda r=rooms_db[i]: self.open_booking_modal(r)).pack(side="left", expand=True,
                                                                                          fill="x")

        self.page_label.configure(text=f"Trang {self.current_page} / {self.total_pages}")
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.total_pages else "disabled")

    def prev_page(self):
        if self.current_page > 1:
            self.load_data(self.filters, self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.load_data(self.filters, self.current_page + 1)

    def apply_filter(self):
        data = {
            "location": self.filter_vars["Địa điểm"].get(),
            "type": self.filter_vars["Loại phòng"].get(),
            "capacity": self.filter_vars["Số khách"].get(),
            "price": self.filter_vars["Mức giá (VNĐ)"].get(),
            "status": self.filter_vars["Trạng thái"].get()
        }
        self.load_data(data, 1)

    def show_details(self, data, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết phòng" in pages:
            detail_page = pages["Chi tiết phòng"]
            if hasattr(detail_page, "set_room"):
                detail_page.set_room(data, img_path)

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Chi tiết phòng")

    def open_booking_modal(self, room_data):
        app = self.winfo_toplevel()
        current_user = getattr(app, "current_user", None)
        if not current_user:
            return messagebox.showwarning("Thông báo", "Sếp vui lòng đăng nhập để đặt phòng!")

        modal = ctk.CTkToplevel(self)
        modal.title(f"Đặt phòng nhanh: {room_data[2]}")
        modal.geometry("400x600")
        modal.configure(fg_color=COLOR_CREAM)
        modal.grab_set()

        ctk.CTkLabel(modal, text="ĐẶT PHÒNG NHANH", font=("Segoe UI", 20, "bold"), text_color=COLOR_GOLD).pack(pady=20)

        info_f = ctk.CTkFrame(modal, fg_color=COLOR_NAVY, corner_radius=10)
        info_f.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(info_f, text=f"Phòng: {room_data[2]}", font=("Segoe UI", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(info_f, text=f"Giá: {room_data[5]:,.0f} VNĐ/đêm", font=("Segoe UI", 12)).pack(pady=2)

        date_f = ctk.CTkFrame(modal, fg_color="transparent")
        date_f.pack(pady=20)

        ctk.CTkLabel(date_f, text="Ngày nhận:").grid(row=0, column=0, padx=10)
        en_in = ctk.CTkEntry(date_f, width=120, state="readonly")
        en_in.grid(row=1, column=0, padx=10, pady=5)
        en_in.configure(state="normal")
        en_in.insert(0, datetime.now().strftime("%d/%m/%Y"))
        en_in.configure(state="readonly")

        ctk.CTkLabel(date_f, text="Ngày trả:").grid(row=0, column=1, padx=10)
        en_out = ctk.CTkEntry(date_f, width=120, state="readonly")
        en_out.grid(row=1, column=1, padx=10, pady=5)
        tomorrow = datetime.now() + timedelta(days=1)
        en_out.configure(state="normal")
        en_out.insert(0, tomorrow.strftime("%d/%m/%Y"))
        en_out.configure(state="readonly")

        def pick_date(entry):
            top_cal = ctk.CTkToplevel(modal)
            cal = Calendar(top_cal, selectmode='day', date_pattern='dd/mm/yyyy')
            cal.pack(pady=10, padx=10)

            def set_val():
                entry.configure(state="normal")
                entry.delete(0, "end")
                entry.insert(0, cal.get_date())
                entry.configure(state="readonly")
                top_cal.destroy()
                update_price()

            ctk.CTkButton(top_cal, text="OK", command=set_val).pack(pady=5)

        en_in.bind("<Button-1>", lambda e: pick_date(en_in))
        en_out.bind("<Button-1>", lambda e: pick_date(en_out))

        lbl_money = ctk.CTkLabel(modal, text="Tổng: 0 VNĐ", font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD)
        lbl_money.pack(pady=10)

        def update_price():
            try:
                d1 = datetime.strptime(en_in.get(), "%d/%m/%Y")
                d2 = datetime.strptime(en_out.get(), "%d/%m/%Y")
                days = (d2 - d1).days
                if days > 0:
                    total = days * room_data[5]
                    lbl_money.configure(text=f"Tổng ({days} đêm): {total:,.0f} VNĐ")
                else:
                    lbl_money.configure(text="Ngày không hợp lệ", text_color="red")
            except (ValueError, TypeError):
                pass

        update_price()

        def confirm():
            d_in = datetime.strptime(en_in.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            d_out = datetime.strptime(en_out.get(), "%d/%m/%Y").strftime("%Y-%m-%d")

            if not db.is_room_available(room_data[0], d_in, d_out):
                return messagebox.showerror("Hết chỗ", "Ngày này đã có người đặt!")

            days = (datetime.strptime(d_out, "%Y-%m-%d") - datetime.strptime(d_in, "%Y-%m-%d")).days
            total = days * room_data[5]

            db.cursor.execute(
                "INSERT INTO bookings (customer_name, room_id, checkin_date, checkout_date, total_price, status) VALUES (?,?,?,?,?,?)",
                (getattr(app, "current_user", "Unknown"), room_data[0], d_in, d_out, total, "Pending"))
            db.conn.commit()
            messagebox.showinfo("Thành công", "Đã gửi yêu cầu đặt phòng!")
            modal.destroy()
            return None

        ctk.CTkButton(modal, text="XÁC NHẬN ĐẶT", fg_color=COLOR_GOLD, height=45, command=confirm).pack(pady=30,
                                                                                                        padx=40,
                                                                                                        fill="x")
        return None