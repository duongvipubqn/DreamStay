import customtkinter as ctk
from config import *
from PIL import Image
import os


class RoomDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.room_data = None

    def set_room(self, data, img_path):
        self.room_data = data
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkButton(self, text="← QUAY LẠI DANH SÁCH", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 13, "bold"),
                      command=lambda: self.winfo_toplevel().switch_page("Phòng")).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        left_p = ctk.CTkFrame(main_container, fg_color="transparent")
        left_p.pack(side="left", padx=30, pady=30)

        if os.path.exists(img_path):
            pil_img = Image.open(img_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(500, 350))
            ctk.CTkLabel(left_p, image=ctk_img, text="").pack()

        right_p = ctk.CTkFrame(main_container, fg_color="transparent")
        right_p.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(right_p, text=data[2], font=("Segoe UI", 32, "bold"), text_color=COLOR_GOLD).pack(anchor="w")
        ctk.CTkLabel(right_p, text=f"Mã phòng: {data[0]}", font=("Segoe UI", 14), text_color="#888").pack(anchor="w")

        info_txt = f"📍 Địa điểm: {data[1]}\n👥 Sức chứa: {data[4]}\n💳 Giá niêm yết: {data[5]:,.0f} VNĐ / đêm\n✨ Trạng thái: {data[3]}"
        ctk.CTkLabel(right_p, text=info_txt, font=("Segoe UI", 18), text_color=COLOR_TEXT, justify="left").pack(
            anchor="w", pady=20)

        desc = ("Trải nghiệm không gian nghỉ dưỡng đẳng cấp tại DreamStay. \n"
                "Phòng được trang bị nội thất cao cấp, hệ thống điều hòa trung tâm, \n"
                "tivi màn hình lớn và ban công với tầm nhìn tuyệt đẹp. \n"
                "Dịch vụ dọn phòng 24/7 đảm bảo không gian luôn sạch sẽ và thơm mát.")
        ctk.CTkLabel(right_p, text=desc, font=("Segoe UI", 14), text_color="#aaa", justify="left").pack(anchor="w",
                                                                                                        pady=10)

        ctk.CTkButton(right_p, text="ĐẶT PHÒNG NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      height=50, width=250, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=20)

    def load_data(self):
        pass