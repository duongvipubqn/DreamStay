from config import *
import os
from PIL import Image

class AboutFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        about_frame = ctk.CTkFrame(self, fg_color="transparent")
        about_frame.pack(padx=50, pady=60, anchor="center")

        img_frame = ctk.CTkFrame(about_frame, fg_color=COLOR_WHITE, border_width=2, border_color=COLOR_GOLD, corner_radius=10)
        img_frame.pack(side="left", padx=(0, 50))

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")
        img_path = os.path.join(img_dir, "about-main.png")

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path).convert("RGB")
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(640, 360))
                img_lbl = ctk.CTkLabel(img_frame, image=ctk_img, text="")
                img_lbl.pack(padx=0, pady=0)
                self.ctk_img_cache = ctk_img

                def make_zoom_handler(lbl, p_img, base_img, w, h):
                    state = {"current_step": 0.0, "after_id": None}
                    max_zoom_factor = 0.05
                    total_steps = 5

                    def update_display():
                        if state["current_step"] <= 0:
                            lbl.configure(image=base_img)
                            return
                        zoom_val = state["current_step"] * max_zoom_factor
                        iw, ih = p_img.size
                        cw, ch = iw / (1 + zoom_val), ih / (1 + zoom_val)
                        l, t, r, b = (iw - cw) / 2, (ih - ch) / 2, (iw + cw) / 2, (ih + ch) / 2
                        zoomed_pil = p_img.crop((l, t, r, b))
                        zoomed_ctk = ctk.CTkImage(light_image=zoomed_pil, dark_image=zoomed_pil, size=(w, h))
                        lbl.configure(image=zoomed_ctk)

                    def animate(direction):
                        if state["after_id"]:
                            lbl.after_cancel(state["after_id"])
                            state["after_id"] = None
                        if direction == "in":
                            if state["current_step"] < 1.0:
                                state["current_step"] += 1.0 / total_steps
                                if state["current_step"] > 1.0: state["current_step"] = 1.0
                                update_display()
                                state["after_id"] = lbl.after(15, lambda: animate("in"))
                        else:
                            state["current_step"] = 0.0
                            lbl.configure(image=base_img)

                    return lambda e: animate("in"), lambda e: animate("out")

                in_f, out_f = make_zoom_handler(img_lbl, pil_img, ctk_img, 640, 360)
                img_lbl.bind("<Enter>", in_f)
                img_lbl.bind("<Leave>", out_f)
            except:
                ctk.CTkLabel(img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360).pack()
        else:
            ctk.CTkLabel(img_frame, text="[ Ảnh Giới Thiệu ]", width=640, height=360).pack()

        content_frame = ctk.CTkFrame(about_frame, fg_color="transparent", width=380)
        content_frame.pack(side="left", fill="y")
        content_frame.pack_propagate(False)

        ctk.CTkLabel(content_frame, text="DreamStay", font=FONT_HEADER,
                     text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(content_frame, text="Khám Phá Di Sản Của Sự Tinh Tế", font=FONT_LABEL,
                     text_color=COLOR_GOLD).pack(anchor="w", pady=(0, 20))

        desc = ("Tọa lạc tại vị trí đắc địa, DreamStay là sự giao thoa hoàn hảo giữa kiến trúc cổ điển và tiện nghi hiện đại. "
                "Chúng tôi tự hào mang đến một không gian nghỉ dưỡng không chỉ sang trọng mà còn ấm cúng, nơi mỗi chi tiết đều được chăm chút tỉ mỉ.\n\n"
                "Từ những bộ sảnh lộng lẫy đến khu vườn thượng uyển yên tĩnh, chúng tôi cam kết mang đến cho bạn một kỳ nghỉ khó quên, vượt trên cả sự mong đợi.")

        ctk.CTkLabel(content_frame, text=desc, font=FONT_BODY, text_color="#ccc",
                     justify="left", wraplength=360, anchor="w").pack(anchor="w", padx=0, pady=(0, 0))

        gallery_container = ctk.CTkFrame(self, fg_color="transparent")
        gallery_container.pack(fill="x", padx=50, pady=(80, 80))

        ctk.CTkLabel(gallery_container, text="Không Gian Của Chúng Tôi", font=FONT_HEADER,
                     text_color=COLOR_TEXT).pack(pady=10)
        ctk.CTkLabel(gallery_container, text="Trải nghiệm hình ảnh sang trọng tại các chi nhánh DreamStay",
                     font=FONT_LABEL, text_color="#888").pack(pady=(0, 40))

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
                    pil_img = Image.open(img_path).convert("RGB")
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(360, 270))
                    gallery_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    gallery_lbl.grid(row=0, column=0, sticky="nsew")

                    def make_zoom_handler(lbl, p_img, base_img, w, h):
                        state = {"current_step": 0.0, "after_id": None}
                        max_zoom_factor = 0.05
                        total_steps = 5

                        def update_display():
                            if state["current_step"] <= 0:
                                lbl.configure(image=base_img)
                                return
                            zoom_val = state["current_step"] * max_zoom_factor
                            iw, ih = p_img.size
                            cw, ch = iw / (1 + zoom_val), ih / (1 + zoom_val)
                            l, t, r, b = (iw - cw) / 2, (ih - ch) / 2, (iw + cw) / 2, (ih + ch) / 2
                            zoomed_pil = p_img.crop((l, t, r, b))
                            zoomed_ctk = ctk.CTkImage(light_image=zoomed_pil, dark_image=zoomed_pil, size=(w, h))
                            lbl.configure(image=zoomed_ctk)

                        def animate(direction):
                            if state["after_id"]:
                                lbl.after_cancel(state["after_id"])
                                state["after_id"] = None
                            if direction == "in":
                                if state["current_step"] < 1.0:
                                    state["current_step"] += 1.0 / total_steps
                                    if state["current_step"] > 1.0: state["current_step"] = 1.0
                                    update_display()
                                    state["after_id"] = lbl.after(15, lambda: animate("in"))
                            else:
                                state["current_step"] = 0.0
                                lbl.configure(image=base_img)

                        return lambda e: animate("in"), lambda e: animate("out")

                    in_f, out_f = make_zoom_handler(gallery_lbl, pil_img, ctk_img, 360, 270)
                    gallery_lbl.bind("<Enter>", in_f)
                    gallery_lbl.bind("<Leave>", out_f)
                except:
                    ctk.CTkLabel(card, text=f"[ {label_text} ]", fg_color=COLOR_BORDER, height=270).grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky="nsew")
            else:
                ctk.CTkLabel(card, text=f"[ {label_text} ]", fg_color=COLOR_BORDER, height=270).grid(row=0, column=0, sticky="nsew")

    def load_data(self):
        pass