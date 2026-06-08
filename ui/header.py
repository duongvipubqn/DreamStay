import colorsys
import os
from config import *

try:
    import pygame

    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


class CTkToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.after_id = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Destroy>", self.on_leave, add="+")

    def on_enter(self, event=None):
        self.cancel_timer()
        self.after_id = self.widget.after(1500, self.show_tooltip)

    def on_leave(self, event=None):
        self.cancel_timer()
        self.hide_tooltip()

    def cancel_timer(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show_tooltip(self):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + (self.widget.winfo_width() // 2) - 50
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.configure(fg_color="#131324")

        label = ctk.CTkLabel(
            self.tooltip_window,
            text=self.text,
            font=("Segoe UI", 11, "bold"),
            text_color="#ffffff",
            fg_color="#252538",
            corner_radius=6,
            padx=8,
            pady=4,
        )
        label.pack()

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


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
        for idx, char in enumerate("DreamStay"):
            lbl = ctk.CTkLabel(self.brand_container, text=char, font=FONT_LOGO)
            lbl.pack(side="left", padx=0)
            self.letters.append(lbl)

            def make_click_handler(i):
                return lambda event: self.handle_logo_click(i)

            lbl.bind("<Button-1>", make_click_handler(idx))

        self.user_btn = ctk.CTkButton(
            self,
            text="ĐĂNG NHẬP",
            width=110,
            height=40,
            corner_radius=6,
            fg_color="white",
            text_color=COLOR_NAVY,
            hover_color=COLOR_GOLD,
            font=FONT_BODY_BOLD,
            command=self.handle_user_click,
        )
        self.user_btn.pack(side="right", padx=(4, 20))

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=(0, 0))

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
        heavy_tracks = [
            {
                "title": f"Heavy Caffeine {roman_nums[i]}",
                "file": f"musics/Heavy Caffeine {i+1}.mp3",
            }
            for i in range(10)
        ]
        drizzle_tracks = [
            {
                "title": f"Midnight Drizzle {roman_nums[i]}",
                "file": f"musics/Midnight Drizzle {i+1}.mp3",
            }
            for i in range(10)
        ]
        self.music_albums = [
            {"name": "Sunlit Arcade Collection", "tracks": arcade_tracks},
            {"name": "Velvet Suitcase Collection", "tracks": velvet_tracks},
            {"name": "Concrete Oasis Collection", "tracks": concrete_tracks},
            {"name": "Heavy Caffeine Collection", "tracks": heavy_tracks},
            {"name": "Midnight Drizzle Collection", "tracks": drizzle_tracks},
        ]

        self.cur_album = 0
        self.cur_track = 0
        self.is_playing = False
        self.volume_level = 0.5
        self.hide_timer_id = None
        self.play_mode = 2
        self.is_paused = False
        self.current_playing_file = None
        self.is_easter_egg = False
        self.logo_state = 0
        self.prev_track_clicks = 0

        self.load_music_state()

        self.music_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.music_panel.pack(side="left", padx=(0, 15))

        self.controls_frame = ctk.CTkFrame(
            self.music_panel,
            fg_color=COLOR_WHITE,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER,
            width=620,
            height=40,
        )
        self.controls_frame.pack(side="left")
        self.controls_frame.pack_propagate(False)

        btn_prev_album = ctk.CTkButton(
            self.controls_frame,
            text="⏮",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.prev_album,
        )
        btn_prev_album.pack(side="left", padx=1)
        CTkToolTip(btn_prev_album, "Lùi Album")

        btn_prev_track = ctk.CTkButton(
            self.controls_frame,
            text="⏪",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.prev_track,
        )
        btn_prev_track.pack(side="left", padx=1)
        CTkToolTip(btn_prev_track, "Bài trước (Tua lùi)")

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
        CTkToolTip(self.music_btn, "Phát / Tạm dừng")

        btn_next_track = ctk.CTkButton(
            self.controls_frame,
            text="⏩",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.next_track,
        )
        btn_next_track.pack(side="left", padx=1)
        CTkToolTip(btn_next_track, "Bài tiếp theo")

        btn_next_album = ctk.CTkButton(
            self.controls_frame,
            text="⏭",
            width=32,
            height=32,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            font=("Segoe UI", 13, "bold"),
            hover_color="#252538",
            command=self.next_album,
        )
        btn_next_album.pack(side="left", padx=1)
        CTkToolTip(btn_next_album, "Tiến Album")

        self.track_label = ctk.CTkLabel(
            self.controls_frame,
            text="DreamStay Player",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_TEXT,
            width=240,
        )
        self.track_label.pack(side="left", padx=5)

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
        self.volume_slider.pack(side="left", padx=(2, 5))
        self.volume_slider.set(self.volume_level * 100.0)
        CTkToolTip(self.volume_slider, "Điều chỉnh âm lượng")

        self.mode_btn_album = ctk.CTkButton(
            self.controls_frame,
            text="⇄",
            width=32,
            height=32,
            fg_color="transparent",
            font=("Segoe UI Symbol", 18, "bold"),
            hover_color="#252538",
            command=lambda: self.set_play_mode(2),
        )
        self.mode_btn_album.pack(side="left", padx=1)
        CTkToolTip(self.mode_btn_album, "Phát liên tục danh sách")

        self.mode_btn_one = ctk.CTkButton(
            self.controls_frame,
            text="↻",
            width=32,
            height=32,
            fg_color="transparent",
            font=("Segoe UI Symbol", 18, "bold"),
            hover_color="#252538",
            command=lambda: self.set_play_mode(3),
        )
        self.mode_btn_one.pack(side="left", padx=1)
        CTkToolTip(self.mode_btn_one, "Lặp lại bài hiện tại")

        self.mode_btn_single = ctk.CTkButton(
            self.controls_frame,
            text="✖",
            width=32,
            height=32,
            fg_color="transparent",
            font=("Segoe UI Symbol", 18, "bold"),
            hover_color="#252538",
            command=lambda: self.set_play_mode(1),
        )
        self.mode_btn_single.pack(side="left", padx=1)
        CTkToolTip(self.mode_btn_single, "Phát xong tự động dừng")

        self.update_mode_buttons_ui()

        album = self.music_albums[self.cur_album]
        track = album["tracks"][self.cur_track]
        self.track_label.configure(text=f"🎵 {track['title']}")

        if self.is_playing:
            self.play_current()
            self.music_btn.configure(text="⏸")
        else:
            self.stop_current()
            self.music_btn.configure(text="▶")

        self.check_music_end()

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
            "Phòng nghỉ",
            "Dịch vụ",
            "Tiện ích",
            "Sự kiện",
            "Liên hệ",
        ]

        if is_logged_in and role in ["staff", "manager"]:
            menus.append("Quản lý")

        for menu in menus:
            is_active = menu == self.active_menu

            if is_active:
                base_color = COLOR_GOLD
            else:
                base_color = "#e74c3c" if menu == "Quản lý" else "white"

            is_manual_hover = is_active or (menu == "Quản lý")

            btn = ctk.CTkButton(
                self.menu_frame,
                text=menu,
                font=FONT_LABEL,
                fg_color="transparent",
                text_color=base_color,
                hover_color=COLOR_GOLD,
                width=110,
                height=40,
                border_width=0,
                hover=False if is_manual_hover else True,
                command=lambda m=menu: self.switch_func(m),
            )

            if is_manual_hover:
                btn.bind(
                    "<Enter>",
                    lambda e, b=btn: b.configure(
                        text_color="white", fg_color=COLOR_GOLD
                    ),
                    add="+",
                )
                btn.bind(
                    "<Leave>",
                    lambda e, b=btn, c=base_color: b.configure(
                        text_color=c, fg_color="transparent"
                    ),
                    add="+",
                )

            btn.pack(side="left", padx=4)

    def handle_user_click(self):
        if self.app.current_user is None:
            self.app.show_login()
        else:
            self.app.switch_page("Hồ sơ")

    def save_music_state(self):
        try:
            if hasattr(self, "album_tracks"):
                self.album_tracks[self.cur_album] = self.cur_track
            else:
                self.album_tracks = [0, 0, 0, 0, 0]
                self.album_tracks[self.cur_album] = self.cur_track

            tracks_str = ",".join(map(str, self.album_tracks))
            state_str = f"{1 if self.is_playing else 0}|{self.cur_album}|{self.cur_track}|{self.volume_level}|{self.play_mode}|{tracks_str}"
            with open("music_state.txt", "w") as f:
                f.write(state_str)
        except Exception:
            pass

    def load_music_state(self):
        self.album_tracks = [0, 0, 0, 0, 0]
        if os.path.exists("music_state.txt"):
            try:
                with open("music_state.txt", "r") as f:
                    data = f.read().strip().split("|")
                if len(data) >= 4:
                    self.is_playing = data[0] == "1"
                    self.cur_album = int(data[1])
                    self.cur_track = int(data[2])
                    self.volume_level = float(data[3])
                    if len(data) >= 5:
                        self.play_mode = int(data[4])
                    if len(data) == 6:
                        self.album_tracks = list(map(int, data[5].split(",")))
                    else:
                        self.album_tracks[self.cur_album] = self.cur_track
                    return True
            except Exception:
                pass
        return False

    def set_play_mode(self, mode):
        self.play_mode = mode
        self.update_mode_buttons_ui()
        self.save_music_state()

    def update_mode_buttons_ui(self):
        self.mode_btn_single.configure(
            text_color=COLOR_GOLD if self.play_mode == 1 else "white"
        )
        self.mode_btn_album.configure(
            text_color=COLOR_GOLD if self.play_mode == 2 else "white"
        )
        self.mode_btn_one.configure(
            text_color=COLOR_GOLD if self.play_mode == 3 else "white"
        )

    def check_music_end(self):
        if self.is_playing and PYGAME_AVAILABLE:
            try:
                if not pygame.mixer.music.get_busy():
                    self.handle_track_end()
            except Exception:
                pass
        self.after(1000, self.check_music_end)

    def handle_track_end(self):
        if self.play_mode == 1:
            self.is_playing = False
            self.stop_current()
            self.music_btn.configure(text="▶")
            self.save_music_state()
        elif self.play_mode == 2:
            self.next_track()
        elif self.play_mode == 3:
            self.play_current()

    def play_current(self):
        album = self.music_albums[self.cur_album]
        track = album["tracks"][self.cur_track]
        track_name = f"{track['title']}"
        self.track_label.configure(text=f"🎵 {track_name}")

        if PYGAME_AVAILABLE and os.path.exists(track["file"]):
            try:
                if (
                    self.is_paused
                    and getattr(self, "current_playing_file", None) == track["file"]
                ):
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                else:
                    pygame.mixer.music.load(track["file"])
                    pygame.mixer.music.set_volume(self.volume_level)
                    pygame.mixer.music.play()
                    self.current_playing_file = track["file"]
                    self.is_paused = False
            except Exception:
                pass
        else:
            self.track_label.configure(text=f"🎵 {track_name} (Demo)")

    def toggle_play(self):
        self.prev_track_clicks = 0
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_current()
            self.music_btn.configure(text="⏸")
        else:
            self.stop_current()
            self.music_btn.configure(text="▶")
        self.save_music_state()

    def next_track(self):
        self.prev_track_clicks = 0
        album = self.music_albums[self.cur_album]
        self.cur_track = (self.cur_track + 1) % len(album["tracks"])
        self.save_music_state()
        if self.is_playing:
            self.play_current()
        else:
            self.stop_current()

    def next_album(self):
        self.prev_track_clicks = 0
        self.album_tracks[self.cur_album] = self.cur_track
        self.cur_album = (self.cur_album + 1) % len(self.music_albums)
        self.cur_track = self.album_tracks[self.cur_album]
        self.save_music_state()
        if self.is_playing:
            self.play_current()
        else:
            self.stop_current()

    def prev_album(self):
        self.prev_track_clicks = 0
        self.album_tracks[self.cur_album] = self.cur_track
        self.cur_album = (self.cur_album - 1) % len(self.music_albums)
        self.cur_track = self.album_tracks[self.cur_album]
        self.save_music_state()
        if self.is_playing:
            self.play_current()
        else:
            self.stop_current()

    def prev_track(self):
        self.prev_track_clicks += 1
        if self.prev_track_clicks == 12:
            self.prev_track_clicks = 0
            self.play_easter_egg("musics/Pushing Rewind.mp3", "Pushing Rewind")
            return

        album = self.music_albums[self.cur_album]
        self.cur_track = (self.cur_track - 1) % len(album["tracks"])
        self.save_music_state()
        if self.is_playing:
            self.play_current()
        else:
            self.stop_current()

    def change_volume(self, val):
        self.volume_level = float(val) / 100.0
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.set_volume(self.volume_level)
            except Exception:
                pass
        self.save_music_state()

    def play_easter_egg(self, file_path, title_name):
        self.is_playing = True
        self.is_easter_egg = True
        self.is_paused = False
        self.music_btn.configure(text="⏸")
        self.track_label.configure(text=f"🎵 {title_name}")
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.set_volume(self.volume_level)
                pygame.mixer.music.play()
            except Exception:
                pass
        self.save_music_state()

    def handle_logo_click(self, index):
        if index == self.logo_state:
            self.logo_state += 1
            if self.logo_state == 9:
                self.logo_state = 0
                self.play_easter_egg("musics/Sthlm Sunset.mp3", "Sthlm Sunset")
        else:
            if index == 0:
                self.logo_state = 1
            else:
                self.logo_state = 0

    def stop_current(self):
        if getattr(self, "is_easter_egg", False):
            self.is_easter_egg = False
            self.is_paused = False
            album = self.music_albums[self.cur_album]
            track = album["tracks"][self.cur_track]
            self.track_label.configure(text=f"🎵 {track['title']} (Paused)")
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
        else:
            album = self.music_albums[self.cur_album]
            track = album["tracks"][self.cur_track]
            self.track_label.configure(text=f"🎵 {track['title']} (Paused)")
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.pause()
                    self.is_paused = True
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

    def update_user_avatar(self, username):
        if not username:
            self.user_btn.configure(
                text="ĐĂNG NHẬP",
                width=110,
                height=40,
                corner_radius=6,
                font=FONT_BODY_BOLD,
                image=None,
            )
            return

        avatar_path = os.path.join(IMAGE_DIR, "avatars", f"{username}.png")
        if os.path.exists(avatar_path):
            try:
                from PIL import Image

                pil_img = Image.open(avatar_path).convert("RGB")
                ctk_img = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=(34, 34)
                )
                self.user_btn.configure(
                    image=ctk_img, text="", width=40, height=40, corner_radius=8
                )
                self.header_avatar_ref = ctk_img
            except:
                self.user_btn.configure(
                    text="👤",
                    image=None,
                    width=40,
                    height=40,
                    corner_radius=8,
                    font=FONT_LABEL,
                )
        else:
            self.user_btn.configure(
                text="👤",
                image=None,
                width=40,
                height=40,
                corner_radius=8,
                font=FONT_LABEL,
            )
