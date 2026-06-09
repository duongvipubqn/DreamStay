import os
from config import *
from PIL import Image, ImageEnhance


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        self.hero_section = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.hero_section.pack(fill="both", expand=True)
        self.hero_section.pack_propagate(False)

        self.current_w = 2000
        self.current_h = 1000

        self.raw_images = []
        self.images_ctk = []
        self.current_idx = 0
        self.anim_started = False
        self.anim_id = None
        self.current_blend = None
        self.idle_timer_id = None
        self.root_click_bind = None
        self.load_all_images_raw()

        for raw in self.raw_images:
            self.images_ctk.append(
                ctk.CTkImage(
                    light_image=raw,
                    dark_image=raw,
                    size=(2000, 1000),
                )
            )

        self.bg_1 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_1.place(relx=0, rely=0, relwidth=1, relheight=1)
        if self.images_ctk:
            self.bg_1.configure(image=self.images_ctk[self.current_idx])

        self.bg_2 = ctk.CTkLabel(self.hero_section, text="", fg_color="transparent")
        self.bg_2.place(relx=1, rely=0, relwidth=1, relheight=1)

        self.search_bar = ctk.CTkFrame(
            self.hero_section, fg_color="transparent", corner_radius=20, width=900
        )
        self.search_bar.place(relx=0.5, rely=0.93, anchor="center")

        self.search_bar_bg_image = None
        self.search_bar_bg = ctk.CTkLabel(
            self.search_bar, text="", fg_color="transparent"
        )
        self.search_bar_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.search_content = ctk.CTkFrame(self.search_bar, fg_color="transparent")
        self.search_content.pack(fill="both", expand=True, padx=40, pady=40)

        self.title_label = ctk.CTkLabel(
            self.search_content,
            text="Sự Sang Trọng Vượt Thời Gian",
            font=FONT_HEADER,
            text_color="white",
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.search_content,
            text="Chào mừng đến với DreamStay, nơi mọi khoảnh khắc là một giấc mơ.",
            font=FONT_LABEL,
            text_color="#ddd",
            wraplength=760,
            justify="center",
        )
        self.subtitle_label.pack(pady=(0, 0))

        self.hero_section.bind("<Configure>", self.on_resize)

    def load_all_images_raw(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")
        for i in range(13):
            img_path = os.path.join(str(img_dir), f"main-background-{i}.png")
            if os.path.exists(img_path):
                try:
                    raw = Image.open(img_path)
                    raw_resized = raw.resize(
                        (2000, 1000), Image.Resampling.LANCZOS
                    ).convert("RGB")
                    darkened = ImageEnhance.Brightness(raw_resized).enhance(0.4)
                    self.raw_images.append(darkened)
                except (IOError, OSError):
                    pass

    def on_resize(self, _event=None):
        if not self.raw_images:
            return
        self._update_search_bar_overlay()
        if not self.anim_started:
            self.anim_started = True
            self.anim_id = self.after(5000, self.rotate_image, "start")

    def rotate_image(self, *_args):
        if not self.images_ctk:
            return
        next_idx = (self.current_idx + 1) % len(self.images_ctk)
        self.animate_fade(1.0, next_idx)

    def _update_search_bar_overlay(self):
        self.search_bar.update_idletasks()
        width = self.search_bar.winfo_width()
        height = self.search_bar.winfo_height()
        if width > 0 and height > 0:
            overlay = Image.new("RGBA", (width, height), (28, 34, 52, 120))
            self.search_bar_bg_image = ctk.CTkImage(
                light_image=overlay, dark_image=overlay, size=(width, height)
            )
            self.search_bar_bg.configure(image=self.search_bar_bg_image)

    def fade_images(self, img1, img2, alpha):
        if not img1 or not img2:
            return img1 or img2
        try:
            return Image.blend(img1, img2, alpha)
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
        w = self.current_w
        h = self.current_h
        if w > 1 and h > 1:
            faded = self.fade_images(
                self.raw_images[self.current_idx], self.raw_images[nxt_idx], 1.0 - alpha
            )
            if faded:
                self.current_blend = ctk.CTkImage(
                    light_image=faded, dark_image=faded, size=(w, h)
                )
                self.bg_1.configure(image=self.current_blend)
        self.search_bar.lift()
        self.anim_id = self.after(15, self.animate_fade, alpha, nxt_idx)

    def destroy(self):
        if hasattr(self, "anim_id") and self.anim_id:
            self.after_cancel(self.anim_id)
        super().destroy()

    def load_data(self):
        pass

    def apply_filter(self):
        app = self.winfo_toplevel()
        switch_func = getattr(app, "switch_page", None)
        if callable(switch_func):
            switch_func("Phòng nghỉ")

    def on_show(self):
        self.reset_idle_timer()
        self.root_click_bind = self.winfo_toplevel().bind(
            "<Button-1>", lambda e: self.reset_idle_timer(), add="+"
        )
        if not self.anim_started and self.raw_images:
            self.anim_started = True
            self.anim_id = self.after(5000, self.rotate_image, "start")

    def on_hide(self):
        if hasattr(self, "idle_timer_id") and self.idle_timer_id:
            self.after_cancel(self.idle_timer_id)
            self.idle_timer_id = None
        if hasattr(self, "root_click_bind") and self.root_click_bind:
            try:
                self.winfo_toplevel().unbind("<Button-1>", self.root_click_bind)
            except:
                pass
            self.root_click_bind = None
        if hasattr(self, "anim_id") and self.anim_id:
            self.after_cancel(self.anim_id)
            self.anim_id = None
        self.anim_started = False

    def reset_idle_timer(self):
        if hasattr(self, "idle_timer_id") and self.idle_timer_id:
            self.after_cancel(self.idle_timer_id)
            self.idle_timer_id = None
        if self.winfo_ismapped():
            self.idle_timer_id = self.after(60000, self.play_hope_music)

    def play_hope_music(self):
        if not self.winfo_ismapped():
            return
        app = self.winfo_toplevel()
        header = getattr(app, "header", None)
        if header and hasattr(header, "play_easter_egg"):
            header.play_easter_egg(
                "musics/Hope Is the Thing With Feathers.mp3",
                "Hope Is the Thing With Feathers",
            )
