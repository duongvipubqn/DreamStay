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

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=50)

        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=1, uniform="column_group")

        self.image_map = {
            "Deluxe Hướng Biển": "room-deluxe-ocean.png",
            "Suite Cao Cấp": "room-luxury-suite.png",
            "Villa Gia Đình Cổ Điển": "room-classic-villa.png",
            "Standard Hướng Vườn": "room-standard-garden.png",
            "Presidential Suite": "room-presidential.png"
        }
        self.ctk_image_cache = {}
        self.loading_task = None

    def load_data(self, filters=None):
        if self.loading_task:
            self.after_cancel(self.loading_task)

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()
        if window_width < 100: window_width = 1300

        card_width = (window_width - 150) // 3
        img_w = int(card_width * 0.9)
        img_h = int(img_w * 0.62)

        # Xây dựng SQL query động
        query = "SELECT room_id, location, room_type, status, capacity, price FROM rooms WHERE status IN ('Trống', 'Đã đặt')"
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

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")

        if not rooms_db:
            ctk.CTkLabel(self.grid_frame, text="Rất tiếc, không tìm thấy phòng phù hợp với yêu cầu của sếp!",
                         font=("Segoe UI", 16), text_color=COLOR_GOLD).pack(pady=50)
        else:
            self.render_batch(rooms_db, 0, img_dir, img_w, img_h)

    def render_batch(self, rooms, start_idx, img_dir, img_w, img_h, *_args):
        batch_size = 6
        end_idx = min(start_idx + batch_size, len(rooms))

        for i in range(start_idx, end_idx):
            r_id, loc, r_type, status, cap, price = rooms[i]

            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1,
                                border_color=COLOR_BORDER)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

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

            status_color = "#2ecc71" if status == "Trống" else "#e74c3c"
            ctk.CTkLabel(header_f, text=status.upper(), font=("Segoe UI", 10, "bold"), text_color=status_color).pack(
                side="right")

            ctk.CTkLabel(card, text=r_type, font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(pady=(5, 0))
            ctk.CTkLabel(card, text=f"📍 {loc} | 👥 {cap}", font=("Segoe UI", 12), text_color="#aaa").pack()
            ctk.CTkLabel(card, text=f"{price:,.0f} VNĐ / đêm", font=("Segoe UI", 16, "bold"),
                         text_color=COLOR_GOLD).pack(pady=10)

            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(pady=(0, 20), padx=20, fill="x")

            ctk.CTkButton(btn_frame, text="CHI TIẾT",
                          fg_color="#3a3a50", text_color="white",
                          font=("Segoe UI", 11, "bold"), height=35, width=80,
                          command=lambda d=rooms[i], p=os.path.join(img_dir, img_name): self.show_details(d, p)).pack(
                side="left", padx=(0, 5), expand=True, fill="x")

            btn_state = "normal" if status == "Trống" else "disabled"
            btn_text = "ĐẶT PHÒNG" if status == "Trống" else "HẾT PHÒNG"
            ctk.CTkButton(btn_frame, text=btn_text, state=btn_state,
                          fg_color=COLOR_GOLD, text_color="white", hover_color=COLOR_GOLD_HOVER,
                          font=("Segoe UI", 11, "bold"), height=35, width=80,
                          command=lambda r=rooms[i]: self.open_booking_modal(r)).pack(side="left", expand=True,
                                                                                      fill="x")

        if end_idx < len(rooms):
            self.loading_task = self.after(10, self.render_batch, rooms, end_idx, img_dir, img_w, img_h)

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

        # Hàm chọn ngày (Dùng lại logic từ trang chi tiết)
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