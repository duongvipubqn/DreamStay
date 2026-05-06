import customtkinter as ctk
from config import *


class EventFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Sự Kiện & Khuyến Mãi", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(pady=30)

        # Danh sách các sự kiện khác nhau hoàn toàn
        self.events_list = [
            {
                "title": "GIẤC MƠ VƯỢT THỜI GIAN",
                "subtitle": "✨ THỬ THÁCH ✨",
                "desc": "Quay video trải nghiệm để nhận 03 đêm nghỉ dưỡng tại Presidential Suite trị giá 100M+.",
                "icon": "🏆"
            },
            {
                "title": "ĐÊM ĐIỆN ẢNH PENACONY",
                "subtitle": "🎬 GIẢI TRÍ 🎬",
                "desc": "Thưởng thức những siêu phẩm điện ảnh dưới bầu trời sao tại Sky Bar hằng đêm.",
                "icon": "🍿"
            },
            {
                "title": "HÓA TRANG COSPLAY",
                "subtitle": "🎭 LỄ HỘI 🎭",
                "desc": "Tham gia lễ hội hóa trang và nhận ngay voucher giảm giá 50% cho tất cả dịch vụ ăn uống.",
                "icon": "🎭"
            }
        ]

        for ev in self.events_list:
            card = ctk.CTkFrame(self, fg_color=COLOR_NAVY, corner_radius=15)
            card.pack(fill="x", padx=50, pady=15)

            f = ctk.CTkFrame(card, fg_color="transparent")
            f.pack(side="left", padx=40, pady=30)

            ctk.CTkLabel(f, text=ev["subtitle"], font=("Segoe UI", 14, "bold"), text_color=COLOR_GOLD).pack(anchor="w")
            ctk.CTkLabel(f, text=ev["title"], font=("Segoe UI", 28, "bold"), text_color="white").pack(anchor="w", pady=5)
            ctk.CTkLabel(f, text=ev["desc"], font=("Segoe UI", 14), text_color="#ccc", justify="left").pack(anchor="w", pady=10)

            ctk.CTkButton(f, text="ĐĂNG KÝ THAM GIA NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                          text_color="white", font=("Segoe UI", 13, "bold"), height=40,
                          command=lambda data=ev: self.show_details(data)).pack(anchor="w", pady=10)

            ctk.CTkLabel(card, text=ev["icon"], font=("Segoe UI", 100), text_color=COLOR_GOLD).pack(side="right", padx=60)

    def show_details(self, data):
        app = self.winfo_toplevel()
        if hasattr(app, "pages") and "Chi tiết sự kiện" in app.pages:
            app.pages["Chi tiết sự kiện"].set_event(data["title"], data["subtitle"], data["desc"])
            app.switch_page("Chi tiết sự kiện")

    def load_data(self): pass