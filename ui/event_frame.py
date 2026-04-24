import customtkinter as ctk
from config import *


class EventFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Sự Kiện & Khuyến Mãi", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(
            pady=30)

        self.main_event = ctk.CTkFrame(self, fg_color=COLOR_NAVY, corner_radius=15)
        self.main_event.pack(fill="x", padx=50, pady=20)

        f = ctk.CTkFrame(self.main_event, fg_color="transparent")
        f.pack(side="left", padx=40, pady=40)

        ctk.CTkLabel(f, text="✨ THỬ THÁCH ✨", font=("Segoe UI", 14, "bold"), text_color=COLOR_GOLD).pack(anchor="w")
        ctk.CTkLabel(f, text="GIẤC MƠ VƯỢT THỜI GIAN", font=("Segoe UI", 28, "bold"), text_color="white").pack(
            anchor="w", pady=5)

        desc = "Hãy quay video trải nghiệm tại khách sạn để có cơ hội\nnhận 03 đêm nghỉ dưỡng tại Presidential Suite trị giá 100M+."
        ctk.CTkLabel(f, text=desc, font=("Segoe UI", 14), text_color="#ccc", justify="left").pack(anchor="w", pady=10)

        ctk.CTkButton(f, text="ĐĂNG KÝ THAM GIA NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 13, "bold"), height=40).pack(anchor="w", pady=10)

        ctk.CTkLabel(self.main_event, text="🏆", font=("Segoe UI", 120), text_color=COLOR_GOLD).pack(side="right",
                                                                                                    padx=60)

    def load_data(self): pass