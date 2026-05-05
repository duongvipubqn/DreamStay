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
            self.grid_frame.grid_columnconfigure(col, weight=1)

        self.image_map = {
            "Deluxe Hướng Biển": "room-deluxe-ocean.png",
            "Suite Cao Cấp": "room-luxury-suite.png",
            "Villa Gia Đình Cổ Điển": "room-classic-villa.png",
            "Standard Hướng Vườn": "room-standard-garden.png",
            "Presidential Suite": "room-presidential.png"
        }

    def load_data(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()

        if window_width < 100: window_width = 1300

        card_width = (window_width - 150) // 3
        img_w = int(card_width * 0.9)
        img_h = int(img_w * 0.62)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(os.path.dirname(current_dir), "images")

        db.cursor.execute(
            "SELECT room_id, location, room_type, status, capacity, price FROM rooms WHERE status IN ('Trống', 'Đã đặt')")
        rooms_db = db.cursor.fetchall()

        for i, (r_id, loc, r_type, status, cap, price) in enumerate(rooms_db):
            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15,
                                border_width=1, border_color=COLOR_BORDER)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            img_name = self.image_map.get(r_type, "default.png")
            img_path = os.path.join(img_dir, img_name)

            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(img_w, img_h))
                    ctk.CTkLabel(card, image=ctk_img, text="").pack(pady=10, padx=10, fill="x")
                except:
                    ctk.CTkLabel(card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h).pack()
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

            btn_state = "normal" if status == "Trống" else "disabled"
            btn_text = "ĐẶT PHÒNG NGAY" if status == "Trống" else "ĐÃ ĐẶT"

            ctk.CTkButton(card, text=btn_text, state=btn_state,
                          fg_color="transparent", border_width=1, border_color=COLOR_GOLD,
                          text_color=COLOR_GOLD, hover_color="#3a3a50",
                          font=("Segoe UI", 12, "bold"), height=35).pack(pady=(0, 20), padx=20, fill="x")