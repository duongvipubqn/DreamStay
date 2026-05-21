import colorsys
import os
from config import *

try:
    import pygame

    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


class Header(ctk.CTkFrame):
    def __init__(self, master, switch_func):
        super().__init__(master, fg_color=COLOR_NAVY, height=70, corner_radius=0)
        self.pack_propagate(False)
        self.switch_func = switch_func
        self.app = master
        self.hue = 0

        self.brand_container = ctk.CTkFrame(self, fg_color="transparent")
        self.brand_container.pack(side="left", padx=30)

        self.letters = []
        for char in "DreamStay":
            lbl = ctk.CTkLabel(self.brand_container, text=char, font=FONT_LOGO)
            lbl.pack(side="left", padx=0)
            self.letters.append(lbl)

        self.user_btn = ctk.CTkButton(
            self,
            text="ĐĂNG NHẬP",
            width=90,
            height=32,
            corner_radius=6,
            fg_color="white",
            text_color=COLOR_NAVY,
            hover_color=COLOR_GOLD,
            font=FONT_BODY_BOLD,
            command=self.handle_user_click,
        )
        self.user_btn.pack(side="right", padx=30)

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=20)

        self.active_menu = None
        self.update_menu(False, None, "Trang chủ")
        self.animate_rainbow()

        roman_nums = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        arcade_tracks = [
            {
                "title": f"Sunlit Arcade {roman_nums[i]}",
                "file": f"musics/Sunlit Arcade {i+1}.mp3",
            }
            for i in range(10)
        ]
        velvet_tracks = [
            {
                "title": f"Velvet Suitcase {roman_nums[i]}",
                "file": f"musics/Velvet Suitcase {i+1}.mp3",
            }
            for i in range(10)
        ]
        concrete_tracks = [
            {
                "title": f"Concrete Oasis {roman_nums[i]}",
                "file": f"musics/Concrete Oasis {i+1}.mp3",
            }
            for i in range(10)
        ]
        self.music_albums = [
            {"name": "Sunlit Arcade Collection", "tracks": arcade_tracks},
            {"name": "Velvet Suitcase Collection", "tracks": velvet_tracks},
            {"name": "Concrete Oasis Collection", "tracks": concrete_tracks},
        ]

        self.cur_album = 0
        self.cur_track = 0
        self.is_playing = False
        self.volume_level = 0.5
        self.hide_timer_id = None

        self.music_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.music_panel.pack(side="left", padx=15)

        self.controls_frame = ctk.CTkFrame(
            self.music_panel,
            fg_color=COLOR_WHITE,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER,
            width=470,
            height=40,
        )
        self.controls_frame.pack(side="left")
        self.controls_frame.pack_propagate(False)

        ctk.CTkButton(
            self.controls_frame,
            text="⏮",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.prev_album,
        ).pack(side="left", padx=1)

        ctk.CTkButton(
            self.controls_frame,
            text="⏪",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.prev_track,
        ).pack(side="left", padx=1)

        self.music_btn = ctk.CTkButton(
            self.controls_frame,
            text="▶",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            hover_color="#252538",
            font=("Segoe UI", 13, "bold"),
            command=self.toggle_play,
        )
        self.music_btn.pack(side="left", padx=1)

        ctk.CTkButton(
            self.controls_frame,
            text="⏩",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.next_track,
        ).pack(side="left", padx=1)

        ctk.CTkButton(
            self.controls_frame,
            text="⏭",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.next_album,
        ).pack(side="left", padx=1)

        self.track_label = ctk.CTkLabel(
            self.controls_frame,
            text="DreamStay Player",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_TEXT,
            width=180,
        )
        self.track_label.pack(side="left", padx=10)

        self.volume_slider = ctk.CTkSlider(
            self.controls_frame,
            width=80,
            height=15,
            from_=0,
            to=100,
            number_of_steps=100,
            button_color=COLOR_GOLD,
            button_hover_color=COLOR_GOLD_HOVER,
            progress_color=COLOR_GOLD,
            command=self.change_volume,
        )
        self.volume_slider._canvas.configure(takefocus=0)
        self.volume_slider.pack(side="left", padx=(5, 10))
        self.volume_slider.set(50)

        self.update_idletasks()

    def animate_rainbow(self, *_args):
        self.hue += 0.005
        if self.hue > 1.0:
            self.hue = 0

        for i, lbl in enumerate(self.letters):
            char_hue = (self.hue + (i * 0.05)) % 1.0

            rgb = colorsys.hsv_to_rgb(char_hue, 0.4, 1.0)
            color_hex = "#%02x%02x%02x" % (
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255),
            )

            lbl.configure(text_color=color_hex)

        self.after(30, self.animate_rainbow, "rainbow")

    def update_menu(self, is_logged_in, role=None, active_page=None):
        if active_page is not None:
            self.active_menu = active_page

        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        menus = [
            "Trang chủ",
            "Giới thiệu",
            "Phòng",
            "Dịch vụ",
            "Tiện ích",
            "Sự kiện",
            "Liên hệ",
        ]

        if is_logged_in and role in ["staff", "manager"]:
            menus.append("Quản lý")

        for menu in menus:
            is_active = menu == self.active_menu
            btn = ctk.CTkButton(
                self.menu_frame,
                text=menu,
                font=FONT_LABEL,
                fg_color="transparent",
                text_color="white",
                hover_color=COLOR_GOLD,
                width=110,
                height=40,
                border_width=2 if is_active else 0,
                border_color=COLOR_GOLD,
                command=lambda m=menu: self.switch_func(m),
            )
            btn.pack(side="left", padx=8)

    def handle_user_click(self):
        if self.app.current_user is None:
            self.app.show_login()
        else:
            self.app.switch_page("Hồ sơ")

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_current()
            self.music_btn.configure(text="⏸")
        else:
            self.stop_current()
            self.music_btn.configure(text="▶")

    def play_current(self):
        album = self.music_albums[self.cur_album]
        track = album["tracks"][self.cur_track]
        track_name = f"{track['title']}"
        self.track_label.configure(text=track_name)

        if PYGAME_AVAILABLE and os.path.exists(track["file"]):
            try:
                pygame.mixer.music.load(track["file"])
                pygame.mixer.music.set_volume(self.volume_level)
                pygame.mixer.music.play()
            except Exception:
                pass
        else:
            self.track_label.configure(text=f"🎵 {track_name} (Demo)")

    def stop_current(self):
        self.track_label.configure(text="Player Paused")
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def next_track(self):
        album = self.music_albums[self.cur_album]
        self.cur_track = (self.cur_track + 1) % len(album["tracks"])
        if self.is_playing:
            self.play_current()

    def prev_track(self):
        album = self.music_albums[self.cur_album]
        self.cur_track = (self.cur_track - 1) % len(album["tracks"])
        if self.is_playing:
            self.play_current()

    def next_album(self):
        self.cur_album = (self.cur_album + 1) % len(self.music_albums)
        self.cur_track = 0
        if self.is_playing:
            self.play_current()

    def prev_album(self):
        self.cur_album = (self.cur_album - 1) % len(self.music_albums)
        self.cur_track = 0
        if self.is_playing:
            self.play_current()

    def change_volume(self, val):
        self.volume_level = float(val) / 100.0
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.set_volume(self.volume_level)
            except Exception:
                pass

    def on_music_leave(self, event):
        self.update_music_icon(hover=False)
        self.start_hide_timer()

    def on_panel_enter(self, event):
        if self.hide_timer_id:
            self.after_cancel(self.hide_timer_id)
            self.hide_timer_id = None

    def on_panel_leave(self, event):
        self.start_hide_timer()

    def start_hide_timer(self):
        if self.hide_timer_id is None:
            self.hide_timer_id = self.after(800, self.hide_controls)

    def hide_controls(self):
        self.controls_frame.pack_forget()
        self.hide_timer_id = None
