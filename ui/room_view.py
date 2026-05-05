import customtkinter as ctk
from config import *
from PIL import Image
import os
from database import db


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
        img_dir = os.path.join(os.path.dirname(current_dir), "images")

        if not rooms_db:
            ctk.CTkLabel(self.grid_frame, text="Rất tiếc, không tìm thấy phòng phù hợp với yêu cầu của sếp!",
                         font=("Segoe UI", 16), text_color=COLOR_GOLD).pack(pady=50)
        else:
            self.render_batch(rooms_db, 0, img_dir, img_w, img_h)

    def render_batch(self, rooms, start_idx, img_dir, img_w, img_h):
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
                    except:
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
                          font=("Segoe UI", 11, "bold"), height=35, width=80).pack(side="left", expand=True, fill="x")

        if end_idx < len(rooms):
            self.loading_task = self.after(10, lambda: self.render_batch(rooms, end_idx, img_dir, img_w, img_h))

    def show_details(self, data, img_path):
        app = self.winfo_toplevel()
        if hasattr(app, "pages") and "Chi tiết phòng" in app.pages:
            detail_page = app.pages["Chi tiết phòng"]
            detail_page.set_room(data, img_path)
            app.switch_page("Chi tiết phòng")