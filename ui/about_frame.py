from config import *
import os
from PIL import Image

class AboutFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        about_frame = ctk.CTkFrame(self, fg_color="transparent")
        about_frame.pack(padx=50, pady=60, anchor="center")

        # Ảnh chính có khung viền
        img_frame = ctk.CTkFrame(about_frame, fg_color=COLOR_WHITE, border_width=2, border_color=COLOR_GOLD, corner_radius=10)
        img_frame.pack(side="left", padx=(0, 50))

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")
        img_path = os.path.join(img_dir, "about-main.png")

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(640, 360))
                ctk.CTkLabel(img_frame, image=ctk_img, text="").pack(padx=0, pady=0)
                self.ctk_img_cache = ctk_img
            except (IOError, OSError, TypeError, ValueError):
                ctk.CTkLabel(img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360).pack()
        else:
            ctk.CTkLabel(img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360).pack()

        # Text bên phải
        content_frame = ctk.CTkFrame(about_frame, fg_color="transparent", width=380)
        content_frame.pack(side="left", fill="y")
        content_frame.pack_propagate(False)

        ctk.CTkLabel(content_frame, text="DreamStay", font=("Segoe UI", 42, "bold"),
                     text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(content_frame, text="Khám Phá Di Sản Của Sự Tinh Tế", font=("Segoe UI", 18),
                     text_color=COLOR_GOLD).pack(anchor="w", pady=(0, 20))

        desc = ("Tọa lạc tại vị trí đắc địa, DreamStay là sự giao thoa hoàn hảo giữa kiến trúc cổ điển và tiện nghi hiện đại. "
                "Chúng tôi tự hào mang đến một không gian nghỉ dưỡng không chỉ sang trọng mà còn ấm cúng, nơi mỗi chi tiết đều được chăm chút tỉ mỉ.\n\n"
                "Từ những bộ sảnh lộng lẫy đến khu vườn thượng uyển yên tĩnh, chúng tôi cam kết mang đến cho bạn một kỳ nghỉ khó quên, vượt trên cả sự mong đợi.")

        ctk.CTkLabel(content_frame, text=desc, font=("Segoe UI", 13), text_color="#ccc",
                     justify="left", wraplength=360, anchor="w").pack(anchor="w", padx=0, pady=(0, 0))

        gallery_container = ctk.CTkFrame(self, fg_color="transparent")
        gallery_container.pack(fill="x", padx=50, pady=(80, 80))

        ctk.CTkLabel(gallery_container, text="Không Gian Của Chúng Tôi", font=("Segoe UI", 36, "bold"),
                     text_color=COLOR_TEXT).pack(pady=10)
        ctk.CTkLabel(gallery_container, text="Trải nghiệm hình ảnh sang trọng tại các chi nhánh DreamStay",
                     font=("Segoe UI", 16), text_color="#888").pack(pady=(0, 40))

        grid_frame = ctk.CTkFrame(gallery_container, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        for r in range(2):
            grid_frame.grid_rowconfigure(r, weight=1)
        for c in range(3):
            grid_frame.grid_columnconfigure(c, weight=1)

        utility_images = [
            ("util-pool.png", "Hồ Bơi"),
            ("util-restaurant.png", "Nhà Hàng"),
            ("util-spa.png", "Spa"),
            ("util-gym.png", "Gym"),
            ("util-skybar.png", "Sky Bar"),
            ("util-ballroom.png", "Phòng Tiệc")
        ]

        for i, (img_name, label_text) in enumerate(utility_images):
            card = ctk.CTkFrame(grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1,
                                border_color=COLOR_GOLD)
            card.grid(row=i // 3, column=i % 3, padx=12, pady=12, sticky="nsew")

            card.grid_rowconfigure(0, weight=1)
            card.grid_columnconfigure(0, weight=1)

            img_path = os.path.join(img_dir, img_name)
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(360, 270))
                    ctk.CTkLabel(card, image=ctk_img, text="").grid(row=0, column=0, sticky="nsew")
                except (IOError, OSError, TypeError, ValueError):
                    ctk.CTkLabel(card, text=f"[ {label_text} ]", fg_color=COLOR_BORDER, height=270).grid(row=0, column=0, sticky="nsew")
            else:
                ctk.CTkLabel(card, text=f"[ {label_text} ]", fg_color=COLOR_BORDER, height=270).grid(row=0, column=0, sticky="nsew")

    def load_data(self):
        pass