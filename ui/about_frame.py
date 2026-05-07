from config import *

class AboutFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        about_frame = ctk.CTkFrame(self, fg_color="transparent")
        about_frame.pack(fill="x", padx=100, pady=80)

        img_label = ctk.CTkLabel(about_frame, text="[ Ảnh Giới Thiệu ]", width=500, height=350,
                                 fg_color=COLOR_WHITE, corner_radius=15)
        img_label.pack(side="left", padx=(0, 50))

        content_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(content_frame, text="DreamStay", font=("Segoe UI", 42, "bold"),
                     text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(content_frame, text="Khám Phá Di Sản Của Sự Tinh Tế", font=("Segoe UI", 18),
                     text_color=COLOR_GOLD).pack(anchor="w", pady=(5, 20))

        desc = ("Tọa lạc tại vị trí đắc địa, DreamStay là sự giao thoa hoàn hảo\n"
                "giữa kiến trúc cổ điển và tiện nghi hiện đại. Chúng tôi tự hào mang\n"
                "đến một không gian nghỉ dưỡng không chỉ sang trọng mà còn ấm\n"
                "cúng, nơi mỗi chi tiết đều được chăm chút tỉ mỉ.\n\n"
                "Từ những bộ sảnh lộng lẫy đến khu vườn thượng uyển yên tĩnh,\n"
                "chúng tôi cam kết mang đến cho bạn một kỳ nghỉ khó quên, vượt\n"
                "trên cả sự mong đợi.")

        ctk.CTkLabel(content_frame, text=desc, font=("Segoe UI", 14), text_color="#ccc",
                     justify="left").pack(anchor="w")

        gallery_container = ctk.CTkFrame(self, fg_color="transparent")
        gallery_container.pack(fill="x", padx=100, pady=(0, 80))

        ctk.CTkLabel(gallery_container, text="Không Gian Của Chúng Tôi", font=("Segoe UI", 36, "bold"),
                     text_color=COLOR_TEXT).pack(pady=10)
        ctk.CTkLabel(gallery_container, text="Trải nghiệm hình ảnh sang trọng tại các chi nhánh DreamStay",
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