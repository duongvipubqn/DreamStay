import customtkinter as ctk
from config import *
from PIL import Image
import os


class EventDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

    def set_event(self, title, subtitle, desc):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkButton(self, text="← QUAY LẠI SỰ KIỆN", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 13, "bold"),
                      command=lambda: self.winfo_toplevel().switch_page("Sự kiện")).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        top_section = ctk.CTkFrame(main_container, fg_color=COLOR_NAVY, height=300, corner_radius=20)
        top_section.pack(fill="x", padx=20, pady=20)
        top_section.pack_propagate(False)

        ctk.CTkLabel(top_section, text="✨", font=("Segoe UI", 80)).place(relx=0.1, rely=0.5, anchor="center")

        text_f = ctk.CTkFrame(top_section, fg_color="transparent")
        text_f.place(relx=0.25, rely=0.5, anchor="w")

        ctk.CTkLabel(text_f, text=title, font=("Segoe UI", 42, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(text_f, text=subtitle, font=("Segoe UI", 20), text_color=COLOR_GOLD).pack(anchor="w")

        content_f = ctk.CTkFrame(main_container, fg_color="transparent")
        content_f.pack(fill="x", padx=40, pady=30)

        ctk.CTkLabel(content_f, text="Thông Tin Chi Tiết", font=("Segoe UI", 24, "bold"), text_color=COLOR_GOLD).pack(
            anchor="w", pady=(0, 20))

        ctk.CTkLabel(content_f, text=desc, font=("Segoe UI", 16), text_color=COLOR_TEXT, justify="left",
                     wraplength=800).pack(anchor="w")

        if "ĐIỆN ẢNH" in title:
            rules = ("1. Thời gian: Mỗi tối thứ 6 và thứ 7 hằng tuần.\n"
                     "2. Địa điểm: Sky Bar tầng thượng - DreamStay.\n"
                     "3. Ưu đãi: Miễn phí 01 phần bắp rang và nước ngọt cho khách lưu trú.\n"
                     "4. Đăng ký: Vui lòng liên hệ lễ tân trước 18:00 cùng ngày.")
        elif "COSPLAY" in title:
            rules = ("1. Yêu cầu: Trang phục hóa trang theo chủ đề tự do.\n"
                     "2. Hoạt động: Diễu hành tại sảnh chính và chụp ảnh lưu niệm.\n"
                     "3. Quà tặng: Voucher 50% buffet tối tại nhà hàng The Golden.\n"
                     "4. Thời gian: 19:00 Chủ nhật tuần thứ 2 mỗi tháng.")
        else:
            rules = ("1. Đối tượng: Khách hàng đã sử dụng dịch vụ tại DreamStay.\n"
                     "2. Cách thức: Đăng tải video/ảnh lên mạng xã hội kèm hashtag #DreamStay.\n"
                     "3. Thời gian: Từ 01/05/2024 đến hết 31/08/2024.\n"
                     "4. Giải thưởng: 03 đêm nghỉ dưỡng tại phòng Presidential Suite.")

        rule_f = ctk.CTkFrame(content_f, fg_color=COLOR_NAVY, corner_radius=10)
        rule_f.pack(fill="x", pady=40)

        ctk.CTkLabel(rule_f, text="Thể Lệ Chương Trình", font=("Segoe UI", 16, "bold"), text_color="white").pack(
            anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(rule_f, text=rules, font=("Segoe UI", 14), text_color="#aaa", justify="left").pack(
            anchor="w", padx=20, pady=(0, 15))

        ctk.CTkButton(content_f, text="ĐĂNG KÝ THAM GIA NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      height=55, width=350, font=("Segoe UI", 16, "bold")).pack(pady=20)

    def load_data(self): pass