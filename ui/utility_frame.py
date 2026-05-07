import os
from config import *
from PIL import Image

class UtilityFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(self, master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Tiện Ích & Dịch Vụ", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(pady=30)

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=50)

        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=1)

    def load_data(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()
        if window_width < 100: window_width = 1300

        card_width = (window_width - 150) // 3
        img_w = int(card_width * 0.9)
        img_h = int(img_w * 0.62)

        utils = [
            ("Hồ Bơi Vô Cực", "Thư giãn và đắm mình trong làn nước mát với tầm nhìn bao trọn bờ biển.", "util-pool.png"),
            ("Nhà Hàng The Golden", "Khám phá tinh hoa ẩm thực Á-Âu với các món ăn từ nguyên liệu tươi ngon nhất.", "util-restaurant.png"),
            ("Mộng Mơ Spa", "Tái tạo năng lượng với các liệu pháp spa và massage chuyên nghiệp.", "util-spa.png"),
            ("Fitness Center", "Duy trì thói quen luyện tập với trung tâm thể hình hiện đại.", "util-gym.png"),
            ("Sky Bar Tầng Thượng", "Ngắm hoàng hôn lãng mạn và thưởng thức cocktail sáng tạo.", "util-skybar.png"),
            ("Phòng Đại Tiệc", "Không gian tổ chức sự kiện lý tưởng với trang thiết bị hiện đại.", "util-ballroom.png")
        ]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")

        for i, (name, desc, img_name) in enumerate(utils):
            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1,
                                border_color=COLOR_BORDER)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            img_path = os.path.join(img_dir, img_name)
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(img_w, img_h))
                    ctk.CTkLabel(card, image=ctk_img, text="").pack(pady=10, padx=10, fill="x")
                except (IOError, OSError, TypeError, ValueError):
                    ctk.CTkLabel(card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h).pack()
            else:
                ctk.CTkLabel(card, text="[ Ảnh chưa cập nhật ]", width=img_w, height=img_h).pack()

            ctk.CTkLabel(card, text=name, font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(pady=(10, 0))
            ctk.CTkLabel(card, text=desc, font=("Segoe UI", 12), text_color=COLOR_TEXT, wraplength=img_w - 40).pack(pady=15, padx=15)

            ctk.CTkButton(card, text="CHI TIẾT", fg_color="#3a3a50", text_color="white",
                          font=("Segoe UI", 12, "bold"), height=35, width=200,
                          command=lambda n=name, d=desc, p=img_path: self.show_details(n, d, p)).pack(pady=(0, 20))

    def show_details(self, name, desc, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết tiện ích" in pages:
            detail_page = pages["Chi tiết tiện ích"]
            if hasattr(detail_page, "set_utility"):
                detail_page.set_utility(name, desc, img_path)

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Chi tiết tiện ích")