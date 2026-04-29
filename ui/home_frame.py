import customtkinter as ctk
from config import *
from PIL import Image
import os


class HomeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        self.hero_section = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0, height=700)
        self.hero_section.pack(fill="x")
        self.hero_section.pack_propagate(False)

        self.raw_images = []
        self.images_ctk = []
        self.current_idx = 0
        self.load_all_images_raw()

        self.bg_1 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_1.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_2 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_2.place(relx=1, rely=0, relwidth=1, relheight=1)

        self.title_label = ctk.CTkLabel(self.hero_section, text="Sự Sang Trọng Vượt Thời Gian",
                                        font=("Segoe UI", 54, "bold"), text_color="white",
                                        fg_color="transparent", bg_color="transparent")
        self.title_label.place(relx=0.5, rely=0.35, anchor="center")

        self.subtitle_label = ctk.CTkLabel(self.hero_section,
                                           text="Chào mừng đến Khách sạn Mộng Mơ, nơi mọi khoảnh khắc là một giấc mơ.",
                                           font=("Segoe UI", 18), text_color="#f0f0f0",
                                           fg_color="transparent", bg_color="transparent")
        self.subtitle_label.place(relx=0.5, rely=0.45, anchor="center")

        self.search_bar = ctk.CTkFrame(self.hero_section, fg_color="#2c2c3e", corner_radius=12)
        self.search_bar.place(relx=0.5, rely=0.7, anchor="center")

        self.inner_padding = ctk.CTkFrame(self.search_bar, fg_color="transparent")
        self.inner_padding.pack(padx=25, pady=15)

        filters = [
            ("Địa điểm", LOCATIONS),
            ("Loại phòng", ROOM_TYPES),
            ("Số khách", CAPACITIES),
            ("Mức giá (VNĐ)", ["Mọi mức giá", "Dưới 3tr", "3tr - 6tr", "Trên 10tr"])
        ]

        for label, vals in filters:
            f = ctk.CTkFrame(self.inner_padding, fg_color="transparent")
            f.pack(side="left", padx=8)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color="#aaa").pack(anchor="w")
            ctk.CTkOptionMenu(f, values=vals, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                              button_color=COLOR_GOLD, width=150, height=35, dynamic_resizing=False).pack(pady=(5, 0))

        self.btn_check = ctk.CTkButton(self.inner_padding, text="KIỂM TRA\nPHÒNG",
                                       font=("Segoe UI", 12, "bold"),
                                       fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                                       text_color="white", width=120, height=55)
        self.btn_check.pack(side="left", padx=(15, 0))

        self.create_about_section()
        self.create_gallery_section()

        self.hero_section.bind("<Configure>", self.on_resize)
        self.after(5000, self.rotate_image)

    def load_all_images_raw(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(os.path.dirname(current_dir), "images")
        for i in range(13):
            img_path = os.path.join(img_dir, f"main-background-{i}.png")
            if os.path.exists(img_path):
                try:
                    raw = Image.open(img_path)
                    self.raw_images.append(raw)
                except:
                    pass

    def on_resize(self, event):
        if not self.raw_images: return
        new_width = event.width
        new_height = event.height
        self.images_ctk = []
        for raw in self.raw_images:
            self.images_ctk.append(ctk.CTkImage(light_image=raw, dark_image=raw, size=(new_width, new_height)))
        if self.images_ctk:
            self.bg_1.configure(image=self.images_ctk[self.current_idx])

    def rotate_image(self):
        if not self.images_ctk: return
        next_idx = (self.current_idx + 1) % len(self.images_ctk)
        self.bg_2.configure(image=self.images_ctk[next_idx])
        self.bg_2.place(relx=1, rely=0)
        self.animate(1.0, next_idx)

    def animate(self, pos, nxt_idx):
        if pos <= 0:
            self.current_idx = nxt_idx
            self.bg_1.configure(image=self.images_ctk[self.current_idx])
            self.bg_1.place(relx=0, rely=0)
            self.bg_2.place(relx=1, rely=0)
            self.after(5000, self.rotate_image)
            return
        pos -= 0.05
        self.bg_1.place(relx=pos - 1, rely=0)
        self.bg_2.place(relx=pos, rely=0)
        self.title_label.lift()
        self.subtitle_label.lift()
        self.search_bar.lift()
        self.after(15, lambda: self.animate(pos, nxt_idx))

    def create_about_section(self):
        about_frame = ctk.CTkFrame(self, fg_color="transparent")
        about_frame.pack(fill="x", padx=100, pady=80)

        img_label = ctk.CTkLabel(about_frame, text="[ Ảnh Giới Thiệu ]", width=500, height=350,
                                 fg_color=COLOR_WHITE, corner_radius=15)
        img_label.pack(side="left", padx=(0, 50))

        content_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(content_frame, text="Khách Sạn Mộng Mơ", font=("Segoe UI", 42, "bold"),
                     text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(content_frame, text="Khám Phá Di Sản Của Sự Tinh Tế", font=("Segoe UI", 18),
                     text_color=COLOR_GOLD).pack(anchor="w", pady=(5, 20))

        desc = ("Tọa lạc tại vị trí đắc địa, Khách sạn Mộng Mơ là sự giao thoa hoàn hảo\n"
                "giữa kiến trúc cổ điển và tiện nghi hiện đại. Chúng tôi tự hào mang\n"
                "đến một không gian nghỉ dưỡng không chỉ sang trọng mà còn ấm\n"
                "cúng, nơi mỗi chi tiết đều được chăm chút tỉ mỉ.\n\n"
                "Từ những bộ sảnh lộng lẫy đến khu vườn thượng uyển yên tĩnh,\n"
                "chúng tôi cam kết mang đến cho bạn một kỳ nghỉ khó quên, vượt\n"
                "trên cả sự mong đợi.")

        ctk.CTkLabel(content_frame, text=desc, font=("Segoe UI", 14), text_color="#ccc",
                     justify="left").pack(anchor="w")

        ctk.CTkButton(content_frame, text="TÌM HIỂU THÊM", fg_color="transparent",
                      border_width=1, border_color=COLOR_GOLD, text_color=COLOR_GOLD,
                      width=150, height=40).pack(anchor="w", pady=30)

    def create_gallery_section(self):
        gallery_container = ctk.CTkFrame(self, fg_color="transparent")
        gallery_container.pack(fill="x", padx=100, pady=(0, 80))

        ctk.CTkLabel(gallery_container, text="Không Gian Của Chúng Tôi", font=("Segoe UI", 36, "bold"),
                     text_color=COLOR_TEXT).pack(pady=10)
        ctk.CTkLabel(gallery_container, text="Trải nghiệm hình ảnh sang trọng tại các chi nhánh Mộng Mơ",
                     font=("Segoe UI", 16), text_color="#888").pack(pady=(0, 40))

        grid_frame = ctk.CTkFrame(gallery_container, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        for r in range(2): grid_frame.grid_rowconfigure(r, weight=1)
        for c in range(3): grid_frame.grid_columnconfigure(c, weight=1)

        for i in range(6):
            placeholder = ctk.CTkLabel(grid_frame, text=f"Ảnh Không Gian {i + 1}",
                                       fg_color=COLOR_WHITE, corner_radius=10,
                                       height=250)
            placeholder.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")

    def load_data(self):
        pass