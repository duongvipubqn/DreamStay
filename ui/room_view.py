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

        ctk.CTkLabel(self, text="Phòng Nghỉ Của Chúng Tôi", font=FONT_HEADER, text_color=COLOR_TEXT).pack(
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
            ctk.CTkLabel(f, text=label, font=FONT_BODY_BOLD, text_color="#aaa").pack(anchor="w")

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
        self.page_frame.pack(pady=20, fill="x")

        self.pagination_container = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        self.pagination_container.pack(side="top")

        self.jump_frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        self.jump_frame.pack(side="top", pady=10)

        ctk.CTkLabel(self.jump_frame, text="Nhảy đến trang:", font=FONT_BODY).pack(side="left", padx=5)
        self.jump_entry = ctk.CTkEntry(self.jump_frame, width=50, height=28, justify="center")
        self.jump_entry.pack(side="left", padx=5)
        self.jump_entry.bind("<Return>", lambda e: self.go_to_page())
        
        ctk.CTkButton(self.jump_frame, text="ĐI", width=40, height=28, fg_color=COLOR_GOLD, 
                      hover_color=COLOR_GOLD_HOVER, command=self.go_to_page).pack(side="left", padx=5)

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
                         font=FONT_LABEL, text_color=COLOR_GOLD).pack(pady=50)
        else:
            for i, (r_id, loc, r_type, status, cap, price) in enumerate(rooms_db):
                card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1,
                                    border_color=COLOR_BORDER)
                card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

                img_name = self.image_map.get(r_type, "default.png")
                cache_key = f"{img_name}_{img_w}"
                img_path = os.path.join(img_dir, img_name)

                if cache_key not in self.ctk_image_cache:
                    if os.path.exists(img_path):
                        try:
                            pil_img = Image.open(img_path).convert("RGB")
                            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(img_w, img_h))
                            self.ctk_image_cache[cache_key] = (ctk_img, pil_img)
                        except:
                            self.ctk_image_cache[cache_key] = (None, None)
                    else:
                        self.ctk_image_cache[cache_key] = (None, None)

                ctk_img, pil_ref = self.ctk_image_cache[cache_key]

                if ctk_img:
                    img_label = ctk.CTkLabel(card, image=ctk_img, text="")
                    img_label.pack(pady=10, padx=10, fill="x")

                    def make_zoom_handler(lbl, p_img, base_img, w, h):
                        state = {"current_step": 0.0, "after_id": None}
                        max_zoom_factor = 0.05
                        total_steps = 5

                        def update_display():
                            if state["current_step"] <= 0:
                                lbl.configure(image=base_img)
                                return

                            zoom_val = state["current_step"] * max_zoom_factor
                            iw, ih = p_img.size
                            cw, ch = iw / (1 + zoom_val), ih / (1 + zoom_val)
                            l, t, r, b = (iw - cw) / 2, (ih - ch) / 2, (iw + cw) / 2, (ih + ch) / 2
                            zoomed_pil = p_img.crop((l, t, r, b))
                            zoomed_ctk = ctk.CTkImage(light_image=zoomed_pil, dark_image=zoomed_pil, size=(w, h))
                            lbl.configure(image=zoomed_ctk)

                        def animate(direction):
                            if state["after_id"]:
                                lbl.after_cancel(state["after_id"])
                                state["after_id"] = None

                            if direction == "in":
                                if state["current_step"] < 1.0:
                                    state["current_step"] += 1.0 / total_steps
                                    if state["current_step"] > 1.0: state["current_step"] = 1.0
                                    update_display()
                                    state["after_id"] = lbl.after(15, lambda: animate("in"))
                            else:
                                state["current_step"] = 0.0
                                lbl.configure(image=base_img)

                        return lambda e: animate("in"), lambda e: animate("out")

                    enter_fn, leave_fn = make_zoom_handler(img_label, pil_ref, ctk_img, img_w, img_h)
                    img_label.bind("<Enter>", enter_fn)
                    img_label.bind("<Leave>", leave_fn)
                else:
                    ctk.CTkLabel(card, text="[ Ảnh chưa cập nhật ]", width=img_w, height=img_h).pack()

                header_f = ctk.CTkFrame(card, fg_color="transparent")
                header_f.pack(fill="x", padx=20)
                ctk.CTkLabel(header_f, text=f"Mã: {r_id}", font=FONT_BODY_BOLD, text_color="#888").pack(
                    side="left")

                current_booking, upcoming_bookings = self._get_room_status_info(r_id)
                current_text = "Đang đặt" if current_booking else "Trống"
                status_color = "#e74c3c" if current_booking else "#2ecc71"
                ctk.CTkLabel(header_f, text=current_text, font=FONT_BODY_BOLD, text_color=status_color).pack(
                    side="right")

                ctk.CTkLabel(card, text=r_type, font=FONT_LABEL, text_color=COLOR_GOLD).pack(pady=(5, 0))
                ctk.CTkLabel(card, text=f"📍 {loc} | 👥 {cap}", font=FONT_BODY, text_color="#aaa").pack()
                ctk.CTkLabel(card, text=f"{price:,.0f} VNĐ / đêm", font=FONT_BODY,
                             text_color=COLOR_GOLD).pack(pady=10)

                if upcoming_bookings:
                    ctk.CTkLabel(card, text=f"Lịch đặt: {self._format_booking_summary(upcoming_bookings)}",
                                 font=FONT_BODY, text_color="#888").pack(padx=20, pady=(0, 10), anchor="w")
                else:
                    ctk.CTkLabel(card, text="Chưa có lịch đặt", font=FONT_BODY, text_color="#888").pack(
                                 padx=20, pady=(0, 10), anchor="w")

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(pady=(0, 20), padx=20, fill="x")

                ctk.CTkButton(btn_frame, text="CHI TIẾT",
                              fg_color="#3a3a50", text_color="white",
                              font=FONT_BODY_BOLD, height=35, width=80,
                              command=lambda d=rooms_db[i], p=os.path.join(img_dir, img_name): self.show_details(d, p)).pack(
                    side="left", padx=(0, 5), expand=True, fill="x")

                ctk.CTkButton(btn_frame, text="ĐẶT PHÒNG",
                              fg_color=COLOR_GOLD, text_color="white", hover_color=COLOR_GOLD_HOVER,
                              font=FONT_BODY_BOLD, height=35, width=80,
                              command=lambda r=rooms_db[i]: self.open_booking_modal(r)).pack(side="left", expand=True,
                                                                                          fill="x")

        self.render_pagination()

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

    def render_pagination(self):
        for widget in self.pagination_container.winfo_children():
            widget.destroy()

        pages_to_show = set()
        pages_to_show.update([1, 2, 3])
        pages_to_show.update([self.total_pages - 2, self.total_pages - 1, self.total_pages])
        
        if self.current_page > 1: pages_to_show.add(self.current_page - 1)
        pages_to_show.add(self.current_page)
        if self.current_page < self.total_pages: pages_to_show.add(self.current_page + 1)

        visible_pages = sorted([p for p in pages_to_show if 1 <= p <= self.total_pages])

        last_p = 0
        for p in visible_pages:
            if last_p != 0 and p - last_p > 1:
                ctk.CTkLabel(self.pagination_container, text="...", font=FONT_LABEL).pack(side="left", padx=5)
            
            is_active = (p == self.current_page)
            btn = ctk.CTkButton(self.pagination_container, text=str(p), width=35, height=35,
                                fg_color=COLOR_GOLD if is_active else COLOR_WHITE,
                                text_color="white" if is_active else COLOR_NAVY,
                                font=FONT_BODY_BOLD,
                                command=lambda page=p: self.load_data(self.filters, page))
            btn.pack(side="left", padx=3)
            last_p = p

    def go_to_page(self):
        val = self.jump_entry.get()
        if val.isdigit():
            page = int(val)
            if 1 <= page <= self.total_pages:
                self.load_data(self.filters, page)
                self.jump_entry.delete(0, "end")
            else:
                messagebox.showwarning("Lỗi", f"Vui lòng nhập trang từ 1 đến {self.total_pages}")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập số trang hợp lệ")

    def prev_page(self): pass
    def next_page(self): pass    

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
        w, h = 400, 600
        modal.update_idletasks()
        main_win = self.winfo_toplevel()
        x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
        y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
        modal.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        modal.configure(fg_color=COLOR_CREAM)
        modal.grab_set()

        ctk.CTkLabel(modal, text="ĐẶT PHÒNG NHANH", font=FONT_LABEL, text_color=COLOR_GOLD).pack(pady=20)

        info_f = ctk.CTkFrame(modal, fg_color=COLOR_NAVY, corner_radius=10)
        info_f.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(info_f, text=f"Phòng: {room_data[2]}", font=FONT_LABEL).pack(pady=5)
        ctk.CTkLabel(info_f, text=f"Giá: {room_data[5]:,.0f} VNĐ/đêm", font=FONT_BODY).pack(pady=2)

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

            tw, th = 300, 350
            top_cal.update_idletasks()
            mx = modal.winfo_x() + (modal.winfo_width() // 2) - (tw // 2)
            my = modal.winfo_y() + (modal.winfo_height() // 2) - (th // 2)
            top_cal.geometry(f"{tw}x{th}+{max(0, mx)}+{max(0, my)}")

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

        lbl_money = ctk.CTkLabel(modal, text="Tổng: 0 VNĐ", font=FONT_LABEL, text_color=COLOR_GOLD)
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