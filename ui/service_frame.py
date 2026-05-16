import os
from config import *
from PIL import Image

class ServiceFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(self, master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(self, text="Dịch Vụ Đồ Uống & F&B", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT).pack(pady=30)

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
        img_h = int(img_w * 0.65)

        services = [
            ("Rượu Vang Đỏ Cao Cấp", "Hương vị nồng nàn từ những vùng nho nổi tiếng thế giới.", "service-wine.png"),
            ("Bia Nhập Khẩu", "Tiger, Heineken và các dòng bia thủ công mát lạnh.", "service-beer.png"),
            ("Nước Ngọt & Soda", "Coca-Cola, Pepsi và các loại nước giải khát đa dạng.", "service-softdrink.png"),
            ("Champagne Sang Trọng", "Dành cho những khoảnh khắc kỷ niệm đặc biệt.", "service-champagne.png"),
            ("Nước Ép Trái Cây", "Nguồn vitamin tự nhiên từ trái cây tươi trong ngày.", "service-juice.png"),
            ("Nước Khoáng Tinh Khiết", "Sự lựa chọn thanh khiết và đảm bảo sức khỏe.", "service-water.png")
        ]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(str(os.path.dirname(current_dir)), "images")

        for i, (name, desc, img_name) in enumerate(services):
            card = ctk.CTkFrame(self.grid_frame, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            img_path = os.path.join(img_dir, img_name)
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path).convert("RGB")
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(img_w, img_h))
                    img_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    img_lbl.pack(pady=10, padx=10, fill="x")

                    def make_zoom_handler(lbl, p_img, base_img, w, h):
                        state = {"current_step": 0.0, "after_id": None}
                        max_zoom_factor = 0.05
                        total_steps = 5
                        def update_display():
                            if state["current_step"] <= 0:
                                lbl.configure(image=base_img)
                                return
                            zv = state["current_step"] * max_zoom_factor
                            iw, ih = p_img.size
                            cw, ch = iw / (1 + zv), ih / (1 + zv)
                            l, t, r, b = (iw-cw)/2, (ih-ch)/2, (iw+cw)/2, (ih+ch)/2
                            zp = p_img.crop((l, t, r, b))
                            zc = ctk.CTkImage(light_image=zp, dark_image=zp, size=(w, h))
                            lbl.configure(image=zc)
                        def animate(direction):
                            if state["after_id"]:
                                lbl.after_cancel(state["after_id"])
                                state["after_id"] = None
                            if direction == "in":
                                if state["current_step"] < 1.0:
                                    state["current_step"] += 1.0 / total_steps
                                    update_display()
                                    state["after_id"] = lbl.after(15, lambda: animate("in"))
                            else:
                                state["current_step"] = 0.0
                                lbl.configure(image=base_img)
                        return lambda e: animate("in"), lambda e: animate("out")

                    in_f, out_f = make_zoom_handler(img_lbl, pil_img, ctk_img, img_w, img_h)
                    img_lbl.bind("<Enter>", in_f)
                    img_lbl.bind("<Leave>", out_f)
                except:
                    ctk.CTkLabel(card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h).pack()
            else:
                ctk.CTkLabel(card, text="[ Ảnh dịch vụ ]", width=img_w, height=img_h).pack()

            ctk.CTkLabel(card, text=name, font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD).pack(pady=(10, 0))
            ctk.CTkLabel(card, text=desc, font=("Segoe UI", 12), text_color=COLOR_TEXT, wraplength=img_w - 40).pack(pady=15, padx=15)
            ctk.CTkButton(card, text="CHI TIẾT", fg_color="#3a3a50", text_color="white",
                          font=("Segoe UI", 12, "bold"), height=35, width=200,
                          command=lambda n=name, d=desc, p=img_path: self.show_details(n, d, p)).pack(pady=(0, 20))

    def show_details(self, name, desc, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết dịch vụ" in pages:
            detail_page = pages["Chi tiết dịch vụ"]
            if hasattr(detail_page, "set_service"):
                detail_page.set_service(name, desc, img_path)
            sf = getattr(app, "switch_page", None)
            if callable(sf): sf("Chi tiết dịch vụ")