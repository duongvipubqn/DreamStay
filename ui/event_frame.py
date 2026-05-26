from config import *


class EventFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(
            self, text="Sự Kiện & Khuyến Mãi", font=FONT_HEADER, text_color=COLOR_TEXT
        ).pack(pady=30)

        self.events_list = [
            {
                "title": "GIẤC MƠ VƯỢT THỜI GIAN",
                "subtitle": "✨ THỬ THÁCH ✨",
                "desc": "Quay video trải nghiệm để nhận 03 đêm nghỉ dưỡng tại Presidential Suite trị giá 100M+.",
                "icon": "🏆",
            },
            {
                "title": "ĐÊM ĐIỆN ẢNH PENACONY",
                "subtitle": "🎬 GIẢI TRÍ 🎬",
                "desc": "Thưởng thức những siêu phẩm điện ảnh dưới bầu trời sao tại Sky Bar hằng đêm.",
                "icon": "🍿",
            },
            {
                "title": "HÓA TRANG COSPLAY",
                "subtitle": "🎭 LỄ HỘI 🎭",
                "desc": "Tham gia lễ hội hóa trang và nhận ngay voucher giảm giá 50% cho tất cả dịch vụ ăn uống.",
                "icon": "🎭",
            },
            {
                "title": "TIỆC TRÀ CHIỀU HOÀNG GIA",
                "subtitle": "🍰 THƯ THƯỞNG 🍰",
                "desc": "Thưởng thức set trà chiều thượng hạng cùng các loại bánh ngọt Pháp tinh tế tại sảnh đón hoàng gia.",
                "icon": "🍰",
            },
            {
                "title": "KHOẢNH KHẮC MỘNG MƠ SPA",
                "subtitle": "💆 TÁI TẠO 💆",
                "desc": "Liệu pháp massage đá nóng và xông hơi thảo dược giúp giải tỏa căng thẳng, phục hồi năng lượng.",
                "icon": "💆",
            },
            {
                "title": "HỘI NGHỊ THƯỢNG ĐỈNH",
                "subtitle": "💼 DOANH NHÂN 💼",
                "desc": "Phòng đại tiệc sang trọng hỗ trợ tối đa cho các buổi hội thảo, ký kết và gala dinner đẳng cấp.",
                "icon": "💼",
            },
            {
                "title": "GIAI ĐIỆU CỦA BIỂN CẢ",
                "subtitle": "🎵 KHÔNG GIAN 🎵",
                "desc": "Đêm nhạc Acoustic sống động hòa cùng tiếng sóng biển rì rào tại bãi biển riêng tư hằng đêm.",
                "icon": "🎸",
            },
            {
                "title": "HOÀNG HÔN RỰC RỠ",
                "subtitle": "🍹 CUỘC SỐNG 🍹",
                "desc": "Thưởng thức menu cocktail sáng tạo và ngắm nhìn hoàng hôn lộng lẫy tại Sky Bar tầng thượng.",
                "icon": "🍹",
            },
            {
                "title": "MỸ VỊ Á - ÂU NĂM SAO",
                "subtitle": "🍲 ẨM THỰC 🍲",
                "desc": "Khám phá hành trình ẩm thực phong phú được chuẩn bị bởi đội ngũ đầu bếp tại Nhà Hàng The Golden.",
                "icon": "🍲",
            },
            {
                "title": "KỶ NGUYÊN SỐ CYBERSPACE",
                "subtitle": "👾 KỸ THUẬT SỐ 👾",
                "desc": "Khai phá không gian ảo hiện đại tại resort và khám phá những bí mật kỹ thuật số ẩn giấu.",
                "icon": "👾",
            },
        ]

        for ev in self.events_list:
            card = ctk.CTkFrame(self, fg_color=COLOR_NAVY, corner_radius=15)
            card.pack(fill="x", padx=250, pady=15)

            f = ctk.CTkFrame(card, fg_color="transparent")
            f.pack(side="left", padx=40, pady=30)

            ctk.CTkLabel(
                f, text=ev["subtitle"], font=FONT_LABEL, text_color=COLOR_GOLD
            ).pack(anchor="w")
            ctk.CTkLabel(f, text=ev["title"], font=FONT_TITLE, text_color="white").pack(
                anchor="w", pady=5
            )
            ctk.CTkLabel(
                f, text=ev["desc"], font=FONT_BODY, text_color="#ccc", justify="left"
            ).pack(anchor="w", pady=10)

            def make_cmd(d):
                return lambda: self.show_details(d)

            ctk.CTkButton(
                f,
                text="ĐĂNG KÝ THAM GIA NGAY",
                fg_color=COLOR_GOLD,
                hover_color=COLOR_GOLD_HOVER,
                text_color="white",
                font=FONT_BODY_BOLD,
                height=40,
                command=make_cmd(ev),
            ).pack(anchor="w", pady=10)

            icon_lbl = ctk.CTkLabel(
                card, text=ev["icon"], font=FONT_ICON, text_color=COLOR_GOLD
            )
            icon_lbl.pack(side="right", padx=60)

            if ev["title"] == "KỶ NGUYÊN SỐ CYBERSPACE":
                icon_lbl.bind("<Button-1>", lambda e: self.trigger_cyber_music())

    def show_details(self, data):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết sự kiện" in pages:
            detail_page = pages["Chi tiết sự kiện"]
            if hasattr(detail_page, "set_event"):
                detail_page.set_event(
                    data.get("title"), data.get("subtitle"), data.get("desc")
                )

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Chi tiết sự kiện")

    def trigger_cyber_music(self):
        if not hasattr(self, "cyber_clicks"):
            self.cyber_clicks = 0
        self.cyber_clicks += 1
        if self.cyber_clicks == 5:
            self.cyber_clicks = 0
            app = self.winfo_toplevel()
            header = getattr(app, "header", None)
            if header and hasattr(header, "play_easter_egg"):
                header.play_easter_egg("musics/A Cybers World.mp3", "A Cyber's World")

    def load_data(self):
        pass
