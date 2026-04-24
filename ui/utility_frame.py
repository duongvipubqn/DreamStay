import customtkinter as ctk
from config import *


class UtilityFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Tiện Ích & Dịch Vụ", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(pady=30)

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=50)
        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=1)

        utils = [
            ("Hồ Bơi Vô Cực", "Thư giãn và đắm mình trong làn nước mát với tầm nhìn bao trọn bờ biển."),
            ("Nhà Hàng The Golden", "Khám phá tinh hoa ẩm thực Á-Âu với các món ăn từ nguyên liệu tươi ngon nhất."),
            ("Mộng Mơ Spa", "Tái tạo năng lượng với các liệu pháp spa và massage chuyên nghiệp."),
            ("Fitness Center", "Duy trì thói quen luyện tập với trung tâm thể hình hiện đại."),
            ("Sky Bar Tầng Thượng", "Ngắm hoàng hôn lãng mạn và thưởng thức cocktail sáng tạo."),
            ("Phòng Đại Tiệc", "Không gian tổ chức sự kiện lý tưởng với trang thiết bị hiện đại.")
        ]

        for i, (name, desc) in enumerate(utils):
            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=10, border_width=1,
                                border_color=COLOR_BORDER)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            ctk.CTkLabel(card, text="", height=20).pack()
            ctk.CTkLabel(card, text=name, font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(pady=(10, 0))
            ctk.CTkLabel(card, text=desc, font=("Segoe UI", 12), text_color=COLOR_TEXT, wraplength=200).pack(pady=15,
                                                                                                             padx=10)
            ctk.CTkButton(card, text="XEM CHI TIẾT", fg_color="transparent", border_width=1, border_color=COLOR_GOLD,
                          text_color=COLOR_GOLD).pack(pady=(0, 20))

    def load_data(self): pass