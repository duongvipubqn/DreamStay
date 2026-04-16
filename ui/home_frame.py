import customtkinter as ctk
from config import *
from PIL import Image
import os


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)

        # --- 1. KHUNG CHÍNH (TRÀN VIỀN) ---
        # Bỏ fixed height, để nó chiếm toàn bộ không gian được giao
        self.container = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0)
        self.container.pack(fill="both", expand=True)  # Tràn hết cỡ

        # --- 2. TẢI ẢNH GỐC (DẠNG PIL ĐỂ RESIZE ĐỘNG) ---
        self.raw_images = []
        self.images_ctk = []  # Lưu danh sách CTkImage đã resize
        self.current_idx = 0
        self.load_all_images_raw()

        # --- 3. TẠO CÁC LỚP HIỂN THỊ ---
        self.bg_1 = ctk.CTkLabel(self.container, text="", fg_color="transparent")
        self.bg_1.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_2 = ctk.CTkLabel(self.container, text="", fg_color="transparent")
        self.bg_2.place(relx=1, rely=0, relwidth=1, relheight=1)

        # --- 4. NỘI DUNG CHỮ & BỘ LỌC ---
        self.title = ctk.CTkLabel(self.container, text="Sự Sang Trọng Vượt Thời Gian",
                                  font=("Georgia", 54, "bold"), text_color="white",
                                  fg_color="transparent")
        self.title.place(relx=0.5, rely=0.35, anchor="center")

        self.subtitle = ctk.CTkLabel(self.container,
                                     text="Chào mừng đến Khách sạn Mộng Mơ, nơi mọi khoảnh khắc là một giấc mơ.",
                                     font=("Segoe UI", 18), text_color="#f0f0f0",
                                     fg_color="transparent")
        self.subtitle.place(relx=0.5, rely=0.45, anchor="center")

        # Booking Form
        self.search_bar = ctk.CTkFrame(self.container, fg_color="#2c2c3e", corner_radius=12)
        self.search_bar.place(relx=0.5, rely=0.7, anchor="center")

        self.inner_padding = ctk.CTkFrame(self.search_bar, fg_color="transparent")
        self.inner_padding.pack(padx=25, pady=15)

        filters = [
            ("Địa điểm", LOCATIONS),
            ("Loại phòng", ROOM_TYPES),
            ("Số khách", CAPACITIES),
            ("Mức giá", ["Mọi mức giá", "Dưới 3tr", "3tr - 6tr", "Trên 10tr"])
        ]

        for label, vals in filters:
            f = ctk.CTkFrame(self.inner_padding, fg_color="transparent")
            f.pack(side="left", padx=8)
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 11, "bold"), text_color="#aaa").pack(anchor="w")
            ctk.CTkOptionMenu(f, values=vals, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                              button_color=COLOR_GOLD, width=150, height=35, dynamic_resizing=False).pack(pady=(5, 0))

        self.btn_check = ctk.CTkButton(self.inner_padding, text="KIỂM TRA\nPHÒNG",
                                       font=("Segoe UI", 12, "bold"),
                                       fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                                       text_color="white", width=120, height=55)
        self.btn_check.pack(side="left", padx=(15, 0))

        # --- 5. THEO DÕI SỰ KIỆN THAY ĐỔI KÍCH THƯỚC ---
        self.container.bind("<Configure>", self.on_resize)

        # Khởi chạy slide
        self.after(5000, self.rotate_image)

    def load_all_images_raw(self):
        """Chỉ nạp ảnh gốc từ ổ cứng vào bộ nhớ PIL"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(os.path.dirname(current_dir), "images")
        for i in range(13):
            img_path = os.path.join(img_dir, f"penacony-{i}.png")
            if os.path.exists(img_path):
                try:
                    raw = Image.open(img_path)
                    self.raw_images.append(raw)
                except:
                    pass

    def on_resize(self, event):
        """Hàm tự chạy khi sếp phóng to/thu nhỏ cửa sổ"""
        if not self.raw_images: return

        # Lấy kích thước hiện tại của container
        new_width = event.width
        new_height = event.height

        # Cập nhật lại toàn bộ danh sách CTkImage theo size mới
        self.images_ctk = []
        for raw in self.raw_images:
            self.images_ctk.append(ctk.CTkImage(light_image=raw, dark_image=raw, size=(new_width, new_height)))

        # Cập nhật ảnh đang hiển thị ngay lập tức để tránh bị lệch
        if self.images_ctk:
            self.bg_1.configure(image=self.images_ctk[self.current_idx])

    def rotate_image(self):
        if not self.images_ctk: return
        next_idx = (self.current_idx + 1) % len(self.images_ctk)
        self.bg_2.configure(image=self.images_ctk[next_idx])
        self.bg_2.place(relx=1, rely=0)
        self.animate(1.0, next_idx)

    def animate(self, pos, nxt_idx):
        if pos <= 0:
            self.current_idx = nxt_idx
            self.bg_1.configure(image=self.images_ctk[self.current_idx])
            self.bg_1.place(relx=0, rely=0)
            self.bg_2.place(relx=1, rely=0)
            self.after(5000, self.rotate_image)
            return
        pos -= 0.05
        self.bg_1.place(relx=pos - 1, rely=0)
        self.bg_2.place(relx=pos, rely=0)

        # Nâng các thành phần lên trên
        self.title.lift()
        self.subtitle.lift()
        self.search_bar.lift()
        self.after(15, lambda: self.animate(pos, nxt_idx))

    def load_data(self):
        pass