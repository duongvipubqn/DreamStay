from config import *
import os
from PIL import Image


class AboutFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.easter_egg_clicks = 0
        self.clicked_indices = set()
        self.final_lesson_active = False
        self.card_labels = {}
        self.current_img_w = 0
        self.current_img_h = 0
        self.hi3_text_label = None

        about_frame = ctk.CTkFrame(self, fg_color="transparent")
        about_frame.pack(padx=50, pady=60, anchor="center")

        img_frame = ctk.CTkFrame(
            about_frame,
            fg_color=COLOR_WHITE,
            border_width=4,
            border_color=COLOR_GOLD,
            corner_radius=10,
        )
        img_frame.pack(side="left", padx=(0, 50))

        img_path = os.path.join(IMAGE_DIR, "about-main.png")

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path).convert("RGB")
                ctk_img = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=(640, 360)
                )
                img_lbl = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                img_lbl.pack(padx=4, pady=4)
                self.ctk_img_cache = ctk_img

                in_f, out_f = make_zoom_handler(img_lbl, pil_img, ctk_img, 640, 360)
                img_lbl.bind("<Enter>", in_f)
                img_lbl.bind("<Leave>", out_f)
            except:
                ctk.CTkLabel(
                    img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360
                ).pack()
        else:
            ctk.CTkLabel(
                img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360
            ).pack()

        content_frame = ctk.CTkFrame(about_frame, fg_color="transparent", width=380)
        content_frame.pack(side="left", fill="y")
        content_frame.pack_propagate(False)

        ctk.CTkLabel(
            content_frame, text="DreamStay", font=FONT_HEADER, text_color=COLOR_TEXT
        ).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(
            content_frame,
            text="Khám Phá Di Sản Của Sự Tinh Tế",
            font=FONT_LABEL,
            text_color=COLOR_GOLD,
        ).pack(anchor="w", pady=(0, 20))

        desc = (
            "Tọa lạc tại vị trí đắc địa, DreamStay là sự giao thoa hoàn hảo giữa kiến trúc cổ điển và tiện nghi hiện đại. "
            "Chúng tôi tự hào mang đến một không gian nghỉ dưỡng không chỉ sang trọng mà còn ấm cúng, nơi mỗi chi tiết đều được chăm chút tỉ mỉ.\n\n"
            "Từ những bộ sảnh lộng lẫy đến khu vườn thượng uyển yên tĩnh, chúng tôi cam kết mang đến cho bạn một kỳ nghỉ khó quên, vượt trên cả sự mong đợi."
        )

        ctk.CTkLabel(
            content_frame,
            text=desc,
            font=FONT_BODY,
            text_color="#ccc",
            justify="left",
            wraplength=360,
            anchor="w",
        ).pack(anchor="w", padx=0, pady=(0, 0))

        gallery_container = ctk.CTkFrame(self, fg_color="transparent")
        gallery_container.pack(fill="x", padx=250, pady=(80, 80))

        ctk.CTkLabel(
            gallery_container,
            text="Khu Trưng Bày Huyền Thoại",
            font=FONT_HEADER,
            text_color=COLOR_TEXT,
        ).pack(pady=(10, 40))

        self.grid_frame = ctk.CTkFrame(gallery_container, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)

        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=1)

    def load_data(self):
        self.clicked_indices.clear()
        self.final_lesson_active = False
        self.card_labels.clear()

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()
        if window_width < 100:
            window_width = 1300

        scale = self._widget_scaling if hasattr(self, "_widget_scaling") else 1.0
        if scale == 0:
            scale = 1.0

        logical_window_width = window_width / scale
        card_width = (logical_window_width - 550) // 3
        img_w = int(card_width * 0.9)
        img_h = int(img_w * 0.65)

        about_images = [
            ("about-kingdom-two-crowns.png", "Kingdom Two Crowns"),
            ("about-detroit-become-human.png", "Detroit: Become Human"),
            ("about-stardew-valley.png", "Stardew Valley"),
            ("about-epic-battle-fantasy-5.png", "Epic Battle Fantasy 5"),
            ("about-honkai-impact-3rd.png", "Honkai Impact 3rd"),
            ("about-katana-zero.png", "Katana Zero"),
            ("about-minecraft.png", "Minecraft"),
            ("about-baldurs-gate-3.png", "Baldur's Gate 3"),
            ("about-muse-dash.png", "Muse Dash"),
        ]

        for i, (img_name, label_text) in enumerate(about_images):
            card = ctk.CTkFrame(
                self.grid_frame,
                fg_color=COLOR_WHITE,
                corner_radius=15,
                border_width=1,
                border_color=COLOR_BORDER,
            )
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            self.current_img_w = img_w
            self.current_img_h = img_h

            img_path = os.path.join(IMAGE_DIR, img_name)
            gallery_lbl = None
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path).convert("RGB")
                    ctk_img = ctk.CTkImage(
                        light_image=pil_img,
                        dark_image=pil_img,
                        size=(img_w, img_h),
                    )
                    gallery_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    gallery_lbl.pack(pady=10, padx=10, fill="x")

                    enter_fn, leave_fn = make_zoom_handler(
                        gallery_lbl, pil_img, ctk_img, img_w, img_h
                    )
                    gallery_lbl.bind("<Enter>", enter_fn)
                    gallery_lbl.bind("<Leave>", leave_fn)
                except:
                    gallery_lbl = ctk.CTkLabel(
                        card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h
                    )
                    gallery_lbl.pack()
            else:
                gallery_lbl = ctk.CTkLabel(
                    card, text="[ Ảnh chưa cập nhật ]", width=img_w, height=img_h
                )
                gallery_lbl.pack()

            if gallery_lbl:
                self.card_labels[i] = gallery_lbl

            lbl_text = ctk.CTkLabel(
                card, text=label_text, font=FONT_LABEL, text_color=COLOR_GOLD
            )
            lbl_text.pack(pady=(10, 20))

            if i == 4:
                self.hi3_text_label = lbl_text

            def make_handler(idx):
                return lambda event: self.handle_card_click(idx)

            card_handler = make_handler(i)
            card.bind("<Button-1>", card_handler)
            if gallery_lbl:
                gallery_lbl.bind("<Button-1>", card_handler)
            lbl_text.bind("<Button-1>", card_handler)

    def handle_card_click(self, index):
        target_indices = {0, 2, 3, 5, 6, 8}
        if index in target_indices:
            if index in self.clicked_indices:
                self.clicked_indices.clear()
                if self.final_lesson_active:
                    self.final_lesson_active = False
                    self.restore_hi3_image()
            else:
                self.clicked_indices.add(index)
                if len(self.clicked_indices) == 6:
                    self.final_lesson_active = True
                    self.change_to_final_lesson()
        elif index == 4:
            if self.final_lesson_active:
                app = self.winfo_toplevel()
                header = getattr(app, "header", None)
                if header and hasattr(header, "play_easter_egg"):
                    header.play_easter_egg("musics/Nightglow.mp3", "Nightglow")
                self.final_lesson_active = False
                self.clicked_indices.clear()
                self.restore_hi3_image()

    def change_to_final_lesson(self):
        lbl = self.card_labels.get(4)
        if not lbl:
            return
        card = lbl.master
        lbl.destroy()

        if self.hi3_text_label:
            self.hi3_text_label.configure(text="Final Lesson")

        final_path = os.path.join(IMAGE_DIR, "final-lesson.png")
        if os.path.exists(final_path):
            try:
                pil_img = Image.open(final_path).convert("RGB")
                ctk_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(self.current_img_w, self.current_img_h),
                )
                new_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                new_lbl.pack(pady=10, padx=10, fill="x", before=self.hi3_text_label)

                enter_fn, leave_fn = make_zoom_handler(
                    new_lbl, pil_img, ctk_img, self.current_img_w, self.current_img_h
                )
                new_lbl.bind("<Enter>", enter_fn)
                new_lbl.bind("<Leave>", leave_fn)

                card_handler = lambda event: self.handle_card_click(4)
                new_lbl.bind("<Button-1>", card_handler)

                self.card_labels[4] = new_lbl
            except:
                pass

    def restore_hi3_image(self):
        lbl = self.card_labels.get(4)
        if not lbl:
            return
        card = lbl.master
        lbl.destroy()

        if self.hi3_text_label:
            self.hi3_text_label.configure(text="Honkai Impact 3rd")

        hi3_path = os.path.join(IMAGE_DIR, "about-honkai-impact-3rd.png")
        if os.path.exists(hi3_path):
            try:
                pil_img = Image.open(hi3_path).convert("RGB")
                ctk_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(self.current_img_w, self.current_img_h),
                )
                new_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                new_lbl.pack(pady=10, padx=10, fill="x", before=self.hi3_text_label)

                enter_fn, leave_fn = make_zoom_handler(
                    new_lbl, pil_img, ctk_img, self.current_img_w, self.current_img_h
                )
                new_lbl.bind("<Enter>", enter_fn)
                new_lbl.bind("<Leave>", leave_fn)

                card_handler = lambda event: self.handle_card_click(4)
                new_lbl.bind("<Button-1>", card_handler)

                self.card_labels[4] = new_lbl
            except:
                pass
