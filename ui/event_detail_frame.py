from config import *


class EventDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

    def set_event(self, title, subtitle, desc):
        for widget in self.winfo_children():
            widget.destroy()

        def go_back():
            app = self.winfo_toplevel()
            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Sự kiện")

        ctk.CTkButton(
            self,
            text="← QUAY LẠI SỰ KIỆN",
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=FONT_BODY_BOLD,
            command=go_back,
        ).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        top_section = ctk.CTkFrame(
            main_container, fg_color=COLOR_NAVY, height=300, corner_radius=20
        )
        top_section.pack(fill="x", padx=20, pady=20)
        top_section.pack_propagate(False)

        ctk.CTkLabel(top_section, text="✨", font=("Segoe UI", 80)).place(
            relx=0.1, rely=0.5, anchor="center"
        )

        text_f = ctk.CTkFrame(top_section, fg_color="transparent")
        text_f.place(relx=0.25, rely=0.5, anchor="w")

        ctk.CTkLabel(text_f, text=title, font=FONT_HEADER, text_color="white").pack(
            anchor="w"
        )
        ctk.CTkLabel(
            text_f, text=subtitle, font=("Segoe UI", 20), text_color=COLOR_GOLD
        ).pack(anchor="w")

        content_f = ctk.CTkFrame(main_container, fg_color="transparent")
        content_f.pack(fill="x", padx=40, pady=30)

        ctk.CTkLabel(
            content_f, text="Thông Tin Chi Tiết", font=FONT_TITLE, text_color=COLOR_GOLD
        ).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(
            content_f,
            text=desc,
            font=FONT_LABEL,
            text_color=COLOR_TEXT,
            justify="left",
            wraplength=800,
        ).pack(anchor="w")

        if "CYBERSPACE" in title:
            rules = (
                "1. Đối tượng: Tất cả các cư dân không gian số thuộc hệ thống resort DreamStay.\n"
                "2. Hoạt động: Khám phá cổng kết nối mạng nội bộ và tìm kiếm các thông điệp mật mã ẩn.\n"
                "3. Gợi ý: Hãy nhấp chuột liên tiếp đúng 5 lần vào biểu tượng quái vật pixel ngoại hành tinh tại trang sự kiện ngoài kia.\n"
                "4. Phần thưởng: Giải mã thành công và kích hoạt trực tiếp bản nhạc nền huyền thoại A Cyber's World."
            )
        elif "VƯỢT THỜI GIAN" in title:
            rules = (
                "1. Đối tượng: Tất cả khách hàng đang lưu trú tại resort DreamStay.\n"
                "2. Cách thức: Đăng tải video/ảnh trải nghiệm lên mạng xã hội kèm hashtag #DreamStay.\n"
                "3. Thời gian diễn ra: Từ ngày 01/05/2026 đến hết ngày 31/08/2026.\n"
                "4. Giải thưởng: 03 đêm nghỉ dưỡng hoàn toàn miễn phí tại phòng hạng Presidential Suite."
            )
        elif "ĐIỆN ẢNH" in title:
            rules = (
                "1. Thời gian: Mỗi tối thứ 6 và thứ 7 hằng tuần.\n"
                "2. Địa điểm: Sky Bar tầng thượng - DreamStay.\n"
                "3. Ưu đãi: Miễn phí 01 phần bắp rang và nước ngọt cho khách lưu trú.\n"
                "4. Đăng ký: Vui lòng liên hệ lễ tân trước 18:00 cùng ngày."
            )
        elif "COSPLAY" in title:
            rules = (
                "1. Yêu cầu: Trang phục hóa trang theo chủ đề tự do.\n"
                "2. Hoạt động: Diễu hành tại sảnh chính và chụp ảnh lưu niệm.\n"
                "3. Quà tặng: Voucher 50% buffet tối tại nhà hàng The Golden.\n"
                "4. Thời gian: 19:00 Chủ nhật tuần thứ 2 mỗi tháng."
            )
        elif "TRÀ CHIỀU" in title:
            rules = (
                "1. Thời gian: Từ 14:00 đến 17:00 hằng ngày.\n"
                "2. Địa điểm: Khu vực Sảnh Đón Hoàng Gia (Lobby) - DreamStay.\n"
                "3. Thực đơn: Trà hoa cúc thượng hạng kết hợp bánh sừng bò bơ tỏi và mousse Pháp ngọt mịn.\n"
                "4. Ưu đãi: Giảm ngay 20% tổng hóa đơn cho khách hàng sở hữu thẻ thành viên hạng Bạc trở lên."
            )
        elif "SPA" in title:
            rules = (
                "1. Thời gian hoạt động: 08:00 - 22:00 hằng ngày.\n"
                "2. Địa điểm: Khu vực Mộng Mơ Spa - Tầng 5 - DreamStay.\n"
                "3. Liệu pháp: Liệu trình massage đá nóng núi lửa kết hợp xông hơi thảo dược phục hồi sức khỏe.\n"
                "4. Đăng ký: Vui lòng liên hệ và đặt chỗ trước 1 tiếng tại quầy lễ tân để được phục vụ chu đáo nhất."
            )
        elif "HỘI NGHỊ" in title:
            rules = (
                "1. Quy mô: Không gian thiết kế chuyên biệt cho các buổi ký kết, gala và hội nghị chuẩn quốc tế.\n"
                "2. Trang thiết bị: Hệ thống âm thanh, ánh sáng và màn hình LED 4K thế hệ mới nhất.\n"
                "3. Địa điểm: Phòng Đại Tiệc (Ballroom) - DreamStay.\n"
                "4. Liên hệ: Vui lòng đặt lịch đặt phòng sự kiện trước ít nhất 1 tuần qua phòng kinh doanh."
            )
        elif "BIỂN CẢ" in title:
            rules = (
                "1. Thời gian: 20:00 - 22:00 hằng đêm.\n"
                "2. Địa điểm: Khu vực Bãi Biển Riêng Tư - DreamStay.\n"
                "3. Hoạt động: Đêm nhạc Acoustic mộc mạc dưới ánh nến và tiếng sóng vỗ.\n"
                "4. Chi phí: Hoàn toàn miễn phí vé vào cửa cho tất cả khách hàng đang lưu trú tại resort."
            )
        elif "HOÀNG HÔN" in title:
            rules = (
                "1. Thời gian: 17:00 - 19:00 hằng ngày.\n"
                "2. Địa điểm: Sky Bar Tầng Thượng - DreamStay.\n"
                "3. Khuyến mãi: Happy Hour - Mua 1 tặng 1 cho tất cả các loại cocktail sáng tạo.\n"
                "4. Đặc quyền: Trải nghiệm không gian ngắm hoàng hôn biển lãng mạn không giới hạn."
            )
        elif "MỸ VỊ" in title:
            rules = (
                "1. Thời gian: Sáng 06:00 - 10:00 | Trưa 11:30 - 14:30 | Tối 18:00 - 22:00.\n"
                "2. Địa điểm: Nhà Hàng The Golden - DreamStay.\n"
                "3. Ẩm thực: Thực đơn Á-Âu chuẩn 5 sao được chế biến tỉ mỉ bởi bếp trưởng.\n"
                "4. Đặt bàn: Khách hàng nên liên hệ đặt trước bàn qua hệ thống lễ tân đối với các tối cuối tuần."
            )
        else:
            rules = (
                "1. Đối tượng: Khách hàng đã sử dụng dịch vụ tại DreamStay.\n"
                "2. Cách thức: Đăng ký tại quầy lễ tân hoặc trực tiếp tại địa điểm tổ chức.\n"
                "3. Thời gian: Theo khung giờ hoạt động được niêm yết của sự kiện.\n"
                "4. Ưu đãi: Nhận ngay quà lưu niệm độc bản từ DreamStay khi tham gia."
            )

        rule_f = ctk.CTkFrame(content_f, fg_color=COLOR_NAVY, corner_radius=10)
        rule_f.pack(fill="x", pady=40)

        ctk.CTkLabel(
            rule_f, text="Thể Lệ Chương Trình", font=FONT_BODY, text_color="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(
            rule_f, text=rules, font=FONT_BODY, text_color="#aaa", justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        def register_event():
            from tkinter import messagebox
            from database import db
            import re
            
            app = self.winfo_toplevel()
            curr_user = getattr(app, "current_user", None)
            curr_username = getattr(app, "current_username", None)
            
            if not curr_user:
                messagebox.showwarning("Thông báo", "Vui lòng đăng nhập để đăng ký tham gia sự kiện!")
                return
            
            try:
                clean_title = re.sub(r"[^\w]", "", title).upper()[:8]
                code = f"EV_{clean_title}"
                
                db.cursor.execute(
                    "SELECT 1 FROM user_coupons WHERE username=? AND code=?", 
                    (curr_username, code)
                )
                if db.cursor.fetchone():
                    messagebox.showinfo("Thông báo", f"Sếp đã đăng ký tham gia sự kiện '{title}' trước đó rồi!")
                    return
                
                db.cursor.execute(
                    "INSERT INTO user_coupons (username, code, description, discount_percent) VALUES (?,?,?,?)",
                    (curr_username, code, f"Voucher qua tang tu su kien: {title}", 15)
                )
                db.conn.commit()
                
                messagebox.showinfo(
                    "Thành công",
                    f"Đăng ký tham gia sự kiện '{title}' thành công!\n"
                    f"Món quà tri ân 1 mã giảm giá {code} (Giảm 15%) đã được gửi trực tiếp vào Kho Voucher của sếp!",
                    parent=self.winfo_toplevel()
                )
            except Exception as err:
                db.conn.rollback()
                messagebox.showerror("Lỗi", f"Không thể xử lý đăng ký: {str(err)}")

        ctk.CTkButton(
            content_f,
            text="ĐĂNG KÝ THAM GIA NGAY",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            height=55,
            width=350,
            font=FONT_BODY,
            command=register_event,
        ).pack(pady=20)

    def load_data(self):
        pass
