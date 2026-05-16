import os
from config import *
from PIL import Image

class ServiceDetailFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

    def set_service(self, name, desc, img_path):
        for widget in self.winfo_children():
            widget.destroy()

        def go_back():
            app = self.winfo_toplevel()
            sf = getattr(app, "switch_page", None)
            if callable(sf): sf("Dịch vụ")

        ctk.CTkButton(self, text="← QUAY LẠI DỊCH VỤ", fg_color="transparent",
                      text_color=COLOR_GOLD, font=("Segoe UI", 13, "bold"),
                      command=go_back).pack(anchor="w", padx=50, pady=20)

        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20)
        main_container.pack(fill="x", padx=50, pady=10)

        left_p = ctk.CTkFrame(main_container, fg_color="transparent")
        left_p.pack(side="left", padx=30, pady=30, anchor="n")

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path).convert("RGB")
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(550, 380))
                img_lbl = ctk.CTkLabel(left_p, image=ctk_img, text="")
                img_lbl.pack()

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

                in_f, out_f = make_zoom_handler(img_lbl, pil_img, ctk_img, 550, 380)
                img_lbl.bind("<Enter>", in_f)
                img_lbl.bind("<Leave>", out_f)
            except:
                ctk.CTkLabel(left_p, text="[ Lỗi tải ảnh ]", width=550, height=380).pack()
        else:
            ctk.CTkLabel(left_p, text="[ Ảnh dịch vụ ]", width=550, height=380).pack()

        right_p = ctk.CTkFrame(main_container, fg_color="transparent")
        right_p.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(right_p, text=name, font=("Segoe UI", 32, "bold"), text_color=COLOR_GOLD).pack(anchor="w")
        ctk.CTkLabel(right_p, text="Dịch vụ F&B phục vụ tại phòng 24/7", font=("Segoe UI", 14), text_color="#888").pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(right_p, text=desc, font=("Segoe UI", 16), text_color=COLOR_TEXT, justify="left", wraplength=400).pack(anchor="w", pady=10)

        more_info = ("Thời gian phục vụ: 24/7\n"
                     "Phí phục vụ: Đã bao gồm trong giá niêm yết\n"
                     "Lưu ý: Đồ uống có cồn chỉ phục vụ cho khách trên 18 tuổi.")
        ctk.CTkLabel(right_p, text=more_info, font=("Segoe UI", 14), text_color="#aaa", justify="left").pack(anchor="w", pady=30)

        ctk.CTkButton(right_p, text="GỌI DỊCH VỤ NGAY", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      height=50, width=250, font=("Segoe UI", 14, "bold")).pack(anchor="w")

    def load_data(self): pass