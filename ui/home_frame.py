import os
from config import *
from PIL import Image

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        self.hero_section = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.hero_section.pack(fill="x")
        self.hero_section.pack_propagate(False)

        self.raw_images = []
        self.images_ctk = []
        self.current_idx = 0
        self.anim_started = False
        self.anim_id = None
        self.current_blend = None
        self.load_all_images_raw()

        self.bg_1 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_1.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_2 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_2.place(relx=1, rely=0, relwidth=1, relheight=1)

        self.search_bar = ctk.CTkFrame(self.hero_section, fg_color="#2c2c3e", corner_radius=15)
        self.search_bar.place(relx=0.5, rely=0.7, anchor="center")

        self.title_label = ctk.CTkLabel(self.search_bar, text="Sự Sang Trọng Vượt Thời Gian",
                                        font=("Segoe UI", 36, "bold"), text_color="white")
        self.title_label.pack(pady=(25, 5))

        self.subtitle_label = ctk.CTkLabel(self.search_bar,
                                           text="Chào mừng đến với DreamStay, nơi mọi khoảnh khắc là một giấc mơ.",
                                           font=("Segoe UI", 16), text_color="#aaa")
        self.subtitle_label.pack(pady=(0, 15))

        self.inner_padding = ctk.CTkFrame(self.search_bar, fg_color="transparent")
        self.inner_padding.pack(padx=30, pady=(0, 25))

        filters = [
            ("Địa điểm", ["Mọi địa điểm"] + LOCATIONS),
            ("Loại phòng", ["Mọi loại phòng"] + ROOM_TYPES),
            ("Số khách", ["Mọi số khách"] + CAPACITIES),
            ("Mức giá (VNĐ)", ["Mọi mức giá", "Dưới 3tr", "3tr - 6tr", "Trên 10tr"])
        ]

        self.filter_vars = {}
        for label, vals in filters:
            f = ctk.CTkFrame(self.inner_padding, fg_color="transparent")
            f.pack(side="left", padx=10)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color="#aaa").pack(anchor="w")

            var = ctk.StringVar(value=vals[0])
            self.filter_vars[label] = var
            ctk.CTkOptionMenu(f, values=vals, variable=var, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                              button_color=COLOR_GOLD, width=150, height=35, dynamic_resizing=False).pack(pady=(5, 0))

        self.btn_check = ctk.CTkButton(self.inner_padding, text="KIỂM TRA\nPHÒNG",
                                       font=("Segoe UI", 12, "bold"),
                                       fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                                       text_color="white", width=120, height=55,
                                       command=self.apply_filter)
        self.btn_check.pack(side="left", padx=(15, 0))

        self.hero_section.bind("<Configure>", self.on_resize)

    def load_all_images_raw(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Ép kiểu str để PyCharm không báo Unexpected type
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")
        for i in range(13):
            img_path = os.path.join(str(img_dir), f"main-background-{i}.png")
            if os.path.exists(img_path):
                try:
                    raw = Image.open(img_path)
                    self.raw_images.append(raw)
                except (IOError, OSError):
                    pass

    def on_resize(self, _event=None):
        if not self.raw_images: return
        toplevel = self.winfo_toplevel()
        toplevel.update_idletasks()

        window_width = toplevel.winfo_width()
        window_height = toplevel.winfo_height()
        available_height = window_height - 70

        self.hero_section.configure(width=window_width, height=available_height)

        self.images_ctk = []
        for raw in self.raw_images:
            self.images_ctk.append(ctk.CTkImage(light_image=raw, dark_image=raw,
                                                size=(window_width, available_height)))

        if self.images_ctk:
            self.bg_1.configure(image=self.images_ctk[self.current_idx])
            
            if not self.anim_started:
                self.anim_started = True
                self.anim_id = self.after(5000, self.rotate_image, "start")

    def rotate_image(self, *_args):
        if not self.images_ctk: return
        next_idx = (self.current_idx + 1) % len(self.images_ctk)
        self.animate_fade(1.0, next_idx)

    def fade_images(self, img1, img2, alpha):
        """Blend hai ảnh PIL: dùng Image.blend() để tối ưu"""
        if not img1 or not img2:
            return img1 or img2
        try:
            if img1.size != img2.size:
                img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
            return Image.blend(img1.convert("RGB"), img2.convert("RGB"), alpha)
        except Exception:
            return img1

    def animate_fade(self, alpha, nxt_idx, *_args):
        if alpha <= 0:
            self.current_idx = nxt_idx
            self.bg_1.configure(image=self.images_ctk[self.current_idx])
            self.search_bar.lift()
            self.anim_id = self.after(5000, self.rotate_image, "loop")
            return

        alpha -= 0.05
        faded = self.fade_images(self.raw_images[self.current_idx], self.raw_images[nxt_idx], 1.0 - alpha)
        if faded:
            w = self.hero_section.winfo_width()
            h = self.hero_section.winfo_height()
            if w > 1 and h > 1:
                self.current_blend = ctk.CTkImage(light_image=faded, dark_image=faded, size=(w, h))
                self.bg_1.configure(image=self.current_blend)
        self.search_bar.lift()
        self.anim_id = self.after(15, self.animate_fade, alpha, nxt_idx)

    def destroy(self):
        if hasattr(self, "anim_id") and self.anim_id:
            self.after_cancel(self.anim_id)
        super().destroy()

    def load_data(self): pass

    def apply_filter(self):
        data = {
            "location": self.filter_vars["Địa điểm"].get(),
            "type": self.filter_vars["Loại phòng"].get(),
            "capacity": self.filter_vars["Số khách"].get(),
            "price": self.filter_vars["Mức giá (VNĐ)"].get()
        }
        app = self.winfo_toplevel()
        # Dùng getattr để gọi switch_page an toàn, xóa lỗi Member not found
        switch_func = getattr(app, "switch_page", None)
        if callable(switch_func):
            switch_func("Phòng", filters=data)