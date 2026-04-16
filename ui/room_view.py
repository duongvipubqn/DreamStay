import customtkinter as ctk
from config import *


class RoomView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Phòng Nghỉ Của Chúng Tôi", font=("Georgia", 32, "bold"), text_color=COLOR_NAVY).pack(
            pady=30)

        # Lưới hiển thị phòng
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=50)

        # Tạo mẫu vài phòng
        rooms = [
            ("Deluxe Hướng Biển", "9.200.000đ", "🛁 Bồn tắm riêng, ⛰️ Hướng nhìn đẹp"),
            ("Suite Cao Cấp", "15.200.000đ", "🛋️ Khu tiếp khách, ☕ Máy pha cà phê"),
            ("Presidential Suite", "62.000.000đ", "🏊 Bể bơi riêng, 💻 Phòng họp riêng")
        ]

        for i, (name, price, info) in enumerate(rooms):
            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=10, border_width=1,
                                border_color=COLOR_BORDER)
            card.grid(row=i // 2, column=i % 2, padx=20, pady=20, sticky="nsew")

            ctk.CTkLabel(card, text="🏨", font=("Segoe UI", 50)).pack(pady=10)
            ctk.CTkLabel(card, text=name, font=("Segoe UI", 20, "bold"), text_color=COLOR_NAVY).pack()
            ctk.CTkLabel(card, text=f"Từ {price} / đêm", font=("Segoe UI", 14), text_color=COLOR_GOLD).pack(pady=5)
            ctk.CTkLabel(card, text=info, font=("Segoe UI", 12), text_color=COLOR_TEXT).pack(pady=10)
            ctk.CTkButton(card, text="XEM CHI TIẾT", fg_color="transparent", border_width=1, border_color=COLOR_GOLD,
                          text_color=COLOR_GOLD).pack(pady=15)

    def load_data(self):
        pass