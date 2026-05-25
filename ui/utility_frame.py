import os
from config import *
from PIL import Image


class UtilityFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(
            self, master, fg_color=COLOR_CREAM, corner_radius=0
        )

        ctk.CTkLabel(
            self, text="Tiện Ích Cao Cấp", font=FONT_HEADER, text_color=COLOR_TEXT
        ).pack(pady=30)

        self.filter_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.filter_frame.pack(anchor="center", pady=(0, 25))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.trigger_search)

        search_container = ctk.CTkFrame(self.filter_frame, fg_color="transparent")
        search_container.pack(side="left", padx=(20, 10), pady=15)

        ctk.CTkLabel(search_container, text=" ", font=FONT_BODY_BOLD).pack(anchor="w")

        search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Tìm kiếm nhanh...",
            width=200,
            textvariable=self.search_var,
            fg_color=COLOR_NAVY,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            height=35,
        )
        search_entry.pack(pady=(5, 0))

        self.filter_container = ctk.CTkFrame(self.filter_frame, fg_color="transparent")
        self.filter_container.pack(side="left", padx=(10, 20), pady=15)

        self.filter_vars = {}
        filters = [
            ("Khu vực", ["Mọi khu vực", "Trong nhà", "Ngoài trời"]),
            ("Trạng thái", ["Mọi trạng thái", "Hoạt động", "Bảo trì"]),
        ]

        for label, vals in filters:
            f = ctk.CTkFrame(self.filter_container, fg_color="transparent")
            f.pack(side="left", padx=12)
            ctk.CTkLabel(f, text=label, font=FONT_BODY_BOLD, text_color="#aaa").pack(
                anchor="w"
            )

            var = ctk.StringVar(value=vals[0])
            self.filter_vars[label] = var
            ctk.CTkOptionMenu(
                f,
                values=vals,
                variable=var,
                fg_color=COLOR_NAVY,
                text_color=COLOR_TEXT,
                button_color=COLOR_GOLD,
                width=150,
                height=35,
                dynamic_resizing=False,
            ).pack(pady=(5, 0))

        btn_container = ctk.CTkFrame(self.filter_container, fg_color="transparent")
        btn_container.pack(side="left", padx=(15, 0))

        ctk.CTkLabel(btn_container, text=" ", font=FONT_BODY_BOLD).pack(anchor="w")

        self.apply_btn = ctk.CTkButton(
            btn_container,
            text="LỌC TIỆN ÍCH",
            width=140,
            height=35,
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            command=self.apply_filter,
        )
        self.apply_btn.pack(pady=(5, 0))

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=250)

        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=1)

        self.filters = None

    def trigger_search(self, *args):
        self.load_data(self.filters)

    def apply_filter(self):
        data = {
            "area": self.filter_vars["Khu vực"].get(),
            "status": self.filter_vars["Trạng thái"].get(),
        }
        self.load_data(data)

    def load_data(self, filters=None):
        self.filters = filters
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.winfo_toplevel().update_idletasks()
        window_width = self.winfo_toplevel().winfo_width()
        if window_width < 100:
            window_width = 1300

        scale = self._widget_scaling if hasattr(self, "_widget_scaling") else 1.0
        if scale == 0:
            scale = 1.0

        card_width = (window_width - 550) // 3
        img_w = int(card_width * 0.9)
        img_h = int(img_w * 0.62)

        logical_img_w = int(img_w / scale)
        logical_img_h = int(img_h / scale)

        utils = [
            (
                "Hồ Bơi Vô Cực",
                "Thư giãn và đắm mình trong làn nước mát với tầm nhìn bao trọn bờ biển.",
                "util-pool.png",
                "Ngoài trời",
                "Hoạt động",
            ),
            (
                "Nhà Hàng The Golden",
                "Khám phá tinh hoa ẩm thực Á-Âu với các món ăn từ nguyên liệu tươi ngon nhất.",
                "util-restaurant.png",
                "Trong nhà",
                "Hoạt động",
            ),
            (
                "Mộng Mơ Spa",
                "Tái tạo năng lượng với các liệu pháp spa và massage chuyên nghiệp.",
                "util-spa.png",
                "Trong nhà",
                "Hoạt động",
            ),
            (
                "Fitness Center",
                "Duy trì thói quen luyện tập với trung tâm thể hình hiện đại.",
                "util-gym.png",
                "Trong nhà",
                "Hoạt động",
            ),
            (
                "Sky Bar Tầng Thượng",
                "Ngắm hoàng hôn lãng mạn và thưởng thức cocktail sáng tạo.",
                "util-skybar.png",
                "Ngoài trời",
                "Hoạt động",
            ),
            (
                "Phòng Đại Tiệc",
                "Không gian tổ chức sự kiện lý tưởng với trang thiết bị hiện đại.",
                "util-ballroom.png",
                "Trong nhà",
                "Hoạt động",
            ),
            (
                "Sảnh Đón Hoàng Gia",
                "Không gian sảnh lộng lẫy tráng lệ chào đón sếp bằng trà hoa cúc và dịch vụ concierge thượng lưu.",
                "util-lobby.png",
                "Trong nhà",
                "Hoạt động",
            ),
            (
                "Vườn Thượng Uyển",
                "Khu vườn hoàng gia xanh mướt ngập tràn kỳ hoa dị thảo, nơi dạo bước tĩnh tâm tuyệt vời.",
                "util-garden.png",
                "Ngoài trời",
                "Hoạt động",
            ),
            (
                "Bãi Biển Riêng Tư",
                "Bờ cát trắng mịn màng trải dài ôm lấy làn nước trong vắt, biệt lập hoàn toàn cho sự riêng tư tuyệt đối.",
                "util-beach.png",
                "Ngoài trời",
                "Hoạt động",
            ),
        ]

        search_text = (
            self.search_var.get().lower() if hasattr(self, "search_var") else ""
        )
        area_filter = filters["area"] if filters else "Mọi khu vực"
        status_filter = filters["status"] if filters else "Mọi trạng thái"

        filtered_utils = []
        for item in utils:
            name, desc, img, area, status = item

            if (
                search_text
                and search_text not in name.lower()
                and search_text not in desc.lower()
            ):
                continue
            if area_filter != "Mọi khu vực" and area != area_filter:
                continue
            if status_filter != "Mọi trạng thái" and status != status_filter:
                continue

            filtered_utils.append(item)

        for i, (name, desc, img_name, _, _) in enumerate(filtered_utils):
            card = ctk.CTkFrame(
                self.grid_frame,
                fg_color=COLOR_WHITE,
                corner_radius=15,
                border_width=1,
                border_color=COLOR_BORDER,
            )
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")

            img_path = os.path.join(IMAGE_DIR, img_name)
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path).convert("RGB")
                    ctk_img = ctk.CTkImage(
                        light_image=pil_img,
                        dark_image=pil_img,
                        size=(logical_img_w, logical_img_h),
                    )
                    util_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    util_lbl.pack(pady=10, padx=10, fill="x")

                    in_f, out_f = make_zoom_handler(
                        util_lbl, pil_img, ctk_img, img_w, img_h
                    )
                    util_lbl.bind("<Enter>", in_f)
                    util_lbl.bind("<Leave>", out_f)
                except:
                    ctk.CTkLabel(
                        card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h
                    ).pack()
            else:
                ctk.CTkLabel(
                    card, text="[ Ảnh chưa cập nhật ]", width=img_w, height=img_h
                ).pack()

            ctk.CTkLabel(card, text=name, font=FONT_LABEL, text_color=COLOR_GOLD).pack(
                pady=(10, 0)
            )
            ctk.CTkLabel(
                card,
                text=desc,
                font=FONT_BODY,
                text_color=COLOR_TEXT,
                wraplength=img_w - 40,
            ).pack(pady=15, padx=15)

            ctk.CTkButton(
                card,
                text="CHI TIẾT",
                fg_color="#3a3a50",
                text_color="white",
                font=FONT_BODY_BOLD,
                height=35,
                width=200,
                command=lambda n=name, d=desc, p=img_path: self.show_details(n, d, p),
            ).pack(pady=(0, 20))

    def show_details(self, name, desc, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết tiện ích" in pages:
            detail_page = pages["Chi tiết tiện ích"]
            if hasattr(detail_page, "set_utility"):
                detail_page.set_utility(name, desc, img_path)

            switch_func = getattr(app, "switch_page", None)
            if callable(switch_func):
                switch_func("Chi tiết tiện ích")
