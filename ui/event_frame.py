from config import *

class EventFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Sự Kiện & Khuyến Mãi", font=FONT_HEADER, text_color=COLOR_TEXT).pack(pady=30)

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

            ctk.CTkLabel(f, text=ev["subtitle"], font=FONT_LABEL, text_color=COLOR_GOLD).pack(anchor="w")
            ctk.CTkLabel(f, text=ev["title"], font=FONT_TITLE, text_color="white").pack(anchor="w", pady=5)
            ctk.CTkLabel(f, text=ev["desc"], font=FONT_BODY, text_color="#ccc", justify="left").pack(anchor="w", pady=10)

            def make_cmd(d):
                return lambda: self.show_details(d)

            ctk.CTkButton(f, text="ĐĂNG KÝ THAM GIA NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                          text_color="white", font=FONT_BODY_BOLD, height=40,
                          command=make_cmd(ev)).pack(anchor="w", pady=10)

            ctk.CTkLabel(card, text=ev["icon"], font=FONT_ICON, text_color=COLOR_GOLD).pack(side="right", padx=60)

    def show_details(self, data):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết sự kiện" in pages:
            detail_page = pages["Chi tiết sự kiện"]
            if hasattr(detail_page, "set_event"):
                detail_page.set_event(data.get("title"), data.get("subtitle"), data.get("desc"))

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Chi tiết sự kiện")

    def load_data(self): pass