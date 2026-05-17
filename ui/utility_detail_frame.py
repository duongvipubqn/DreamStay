import os
from config import *
from PIL import Image

class UtilityDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

    def set_utility(self, name, desc, img_path):
        for widget in self.winfo_children():
            widget.destroy()

        def go_back():
            app = self.winfo_toplevel()
            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Tiện ích")

        ctk.CTkButton(self, text="← QUAY LẠI TIỆN ÍCH", fg_color="transparent",
                      text_color=COLOR_GOLD, font=FONT_BODY_BOLD,
                      command=go_back).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        left_p = ctk.CTkFrame(main_container, fg_color="transparent")
        left_p.pack(side="left", padx=30, pady=30, anchor="n")

        if os.path.exists(img_path):
            pil_img = Image.open(img_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(550, 380))
            ctk.CTkLabel(left_p, image=ctk_img, text="").pack()

        right_p = ctk.CTkFrame(main_container, fg_color="transparent")
        right_p.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(right_p, text=name, font=FONT_HEADER, text_color=COLOR_GOLD).pack(anchor="w")

        ctk.CTkLabel(right_p, text="Dịch vụ cao cấp tại DreamStay", font=FONT_BODY, text_color="#888").pack(
            anchor="w", pady=(0, 20))

        ctk.CTkLabel(right_p, text=desc, font=FONT_LABEL, text_color=COLOR_TEXT, justify="left",
                     wraplength=400).pack(anchor="w", pady=10)

        more_info = ("Giờ phục vụ: 06:00 - 22:00 hằng ngày\n"
                     "Địa điểm: Tầng 5 - Khu vực trung tâm\n"
                     "Lưu ý: Quý khách vui lòng đặt chỗ trước 30 phút để được phục vụ tốt nhất.")
        ctk.CTkLabel(right_p, text=more_info, font=FONT_BODY, text_color="#aaa", justify="left").pack(anchor="w",
                                                                                                             pady=30)

        ctk.CTkButton(right_p, text="ĐẶT DỊCH VỤ NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      height=50, width=250, font=FONT_LABEL).pack(anchor="w")

    def load_data(self):
        pass