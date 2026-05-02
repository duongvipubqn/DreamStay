import customtkinter as ctk
from config import *
from PIL import Image
import os

class HomeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(self, master, fg_color=COLOR_CREAM, corner_radius=0)

        self.hero_section = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
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
            ("Địa điểm", LOCATIONS),
            ("Loại phòng", ROOM_TYPES),
            ("Số khách", CAPACITIES),
            ("Mức giá (VNĐ)", ["Mọi mức giá", "Dưới 3tr", "3tr - 6tr", "Trên 10tr"])
        ]

        for label, vals in filters:
            f = ctk.CTkFrame(self.inner_padding, fg_color="transparent")
            f.pack(side="left", padx=10)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color="#aaa").pack(anchor="w")
            ctk.CTkOptionMenu(f, values=vals, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                              button_color=COLOR_GOLD, width=150, height=35, dynamic_resizing=False).pack(pady=(5, 0))

        self.btn_check = ctk.CTkButton(self.inner_padding, text="KIỂM TRA\nPHÒNG",
                                       font=("Segoe UI", 12, "bold"),
                                       fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                                       text_color="white", width=120, height=55)
        self.btn_check.pack(side="left", padx=(15, 0))

        self.hero_section.bind("<Configure>", self.on_resize)
        self.anim_id = self.after(5000, self.rotate_image)

    def load_all_images_raw(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(os.path.dirname(current_dir), "images")
        for i in range(13):
            img_path = os.path.join(img_dir, f"main-background-{i}.png")
            if os.path.exists(img_path):
                try:
                    raw = Image.open(img_path)
                    self.raw_images.append(raw)
                except: pass

    def on_resize(self, event):
        if not self.raw_images: return

        self.winfo_toplevel().update_idletasks()

        window_width = self.winfo_toplevel().winfo_width()
        window_height = self.winfo_toplevel().winfo_height()

        available_height = window_height - 70

        self.hero_section.configure(width=window_width, height=available_height)

        self.images_ctk = []
        for raw in self.raw_images:
            self.images_ctk.append(ctk.CTkImage(light_image=raw, dark_image=raw,
                                                size=(window_width, available_height)))

        if self.images_ctk:
            self.bg_1.configure(image=self.images_ctk[self.current_idx])

    def rotate_image(self):
        if not self.images_ctk: return
        next_idx = (self.current_idx + 1) % len(self.images_ctk)
        self.bg_2.configure(image=self.images_ctk[next_idx])
        self.bg_2.place(relx=1, rely=0)
        self.anim_id = self.animate(1.0, next_idx)

    def animate(self, pos, nxt_idx):
        if pos <= 0:
            self.current_idx = nxt_idx
            self.bg_1.configure(image=self.images_ctk[self.current_idx])
            self.bg_1.place(relx=0, rely=0)
            self.bg_2.place(relx=1, rely=0)

            self.search_bar.lift()

            self.anim_id = self.after(5000, self.rotate_image)
            return

        pos -= 0.05
        self.bg_1.place(relx=pos - 1, rely=0)
        self.bg_2.place(relx=pos, rely=0)

        self.search_bar.lift()

        self.anim_id = self.after(15, lambda: self.animate(pos, nxt_idx))

    def destroy(self):
        if hasattr(self, "anim_id") and self.anim_id:
            self.after_cancel(self.anim_id)
        super().destroy()

    def load_data(self): pass