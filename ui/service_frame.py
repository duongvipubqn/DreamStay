import os
from config import *
from PIL import Image
from tkinter import messagebox
from database import db
from datetime import datetime


class OrderModal(ctk.CTkToplevel):
    def __init__(self, parent, category_name):
        super().__init__(parent)
        self.title(f"Đặt hàng: {category_name}")
        w, h = 500, 700
        self.update_idletasks()
        main_win = parent.winfo_toplevel()
        main_win.update_idletasks()
        x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
        y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        self.configure(fg_color=COLOR_CREAM)
        self.grab_set()

        db.cursor.execute(
            "SELECT item_name, price, stock FROM inventory WHERE category=?",
            (category_name,),
        )
        self.items = db.cursor.fetchall()

        if not self.items:
            default_items = {
                "Cà Phê Đặc Sản": [
                    ("Cà Phê Phin Truyền Thống", 45000, 100),
                    ("Espresso Macchiato", 55000, 80),
                    ("Cappuccino Cốt Dừa", 65000, 60),
                ],
                "Trà Hoa Thượng Hạng": [
                    ("Trà Sen Tây Hồ", 75000, 50),
                    ("Trà Hoa Cúc Mật Ong", 60000, 70),
                    ("Trà Đào Cam Sả", 65000, 80),
                ],
                "Bánh Ngọt Pháp": [
                    ("Bánh Croissant Bơ Tỏi", 45000, 40),
                    ("Bánh Mousse Sô-cô-la", 55000, 30),
                    ("Bánh Macaron Sắc Màu", 65000, 50),
                ],
            }
            if category_name in default_items:
                for name, price, stock in default_items[category_name]:
                    db.cursor.execute(
                        "INSERT OR IGNORE INTO inventory (category, item_name, price, stock) VALUES (?,?,?,?)",
                        (category_name, name, price, stock),
                    )
                db.conn.commit()
                db.cursor.execute(
                    "SELECT item_name, price, stock FROM inventory WHERE category=?",
                    (category_name,),
                )
                self.items = db.cursor.fetchall()

        self.quantities = {}
        for item in self.items:
            var = ctk.IntVar(value=0)
            var.trace_add("write", lambda *args: self.update_total())
            self.quantities[item[0]] = var

        ctk.CTkLabel(
            self, text=category_name.upper(), font=FONT_LABEL, text_color=COLOR_GOLD
        ).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=350)
        self.scroll.pack(fill="both", expand=True, padx=20)

        app = parent.winfo_toplevel()
        user_role = getattr(app, "current_role", None)

        for name, price, stock in self.items:
            f = ctk.CTkFrame(self.scroll, fg_color=COLOR_WHITE, corner_radius=10)
            f.pack(fill="x", pady=5)

            if user_role in ["manager", "staff"]:
                display_name = f"{name}\n(Còn {stock})"
            else:
                status_text = "Còn" if stock > 0 else "Hết"
                display_name = f"{name}\n({status_text})"

            ctk.CTkLabel(
                f,
                text=display_name,
                font=FONT_BODY_BOLD,
                text_color=COLOR_TEXT,
                justify="left",
            ).pack(side="left", padx=15, pady=5)

            qty_f = ctk.CTkFrame(f, fg_color="transparent")
            qty_f.pack(side="right", padx=10)

            ctk.CTkButton(
                qty_f,
                text="-",
                width=30,
                height=30,
                fg_color="#e74c3c",
                command=lambda n=name: self.change_qty(n, -1),
            ).pack(side="left", padx=2)

            ctk.CTkEntry(
                qty_f,
                textvariable=self.quantities[name],
                width=40,
                height=30,
                justify="center",
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                qty_f,
                text="+",
                width=30,
                height=30,
                fg_color="#27ae60",
                command=lambda n=name: self.change_qty(n, 1),
            ).pack(side="left", padx=2)

            ctk.CTkLabel(
                f,
                text=f"{int(price):,}".replace(",", ".") + "đ",
                font=FONT_BODY,
                text_color=COLOR_GOLD,
                width=80,
            ).pack(side="right", padx=10)

        bottom_f = ctk.CTkFrame(self, fg_color=COLOR_NAVY, corner_radius=0)
        bottom_f.pack(fill="x", side="bottom", pady=0)

        room_f = ctk.CTkFrame(bottom_f, fg_color="transparent")
        room_f.pack(fill="x", padx=30, pady=15)

        ctk.CTkLabel(
            room_f, text="Giao đến phòng:", font=FONT_BODY_BOLD, text_color=COLOR_TEXT
        ).pack(side="left")

        db.cursor.execute("SELECT room_id FROM rooms WHERE status='Đã đặt'")
        occupied_rooms = [r[0] for r in db.cursor.fetchall()]
        if not occupied_rooms:
            occupied_rooms = ["Không có phòng trống"]

        self.room_cb = ctk.CTkOptionMenu(
            room_f,
            values=occupied_rooms,
            fg_color=COLOR_WHITE,
            text_color=COLOR_TEXT,
            button_color=COLOR_GOLD,
            button_hover_color=COLOR_GOLD_HOVER,
            dropdown_fg_color=COLOR_NAVY,
            dropdown_text_color=COLOR_TEXT,
        )
        self.room_cb.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.total_lbl = ctk.CTkLabel(
            bottom_f, text="TỔNG CỘNG: 0 VNĐ", font=FONT_LABEL, text_color=COLOR_GOLD
        )
        self.total_lbl.pack(pady=10)

        ctk.CTkButton(
            bottom_f,
            text="XÁC NHẬN ĐƠN HÀNG",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            height=45,
            font=FONT_LABEL,
            command=self.confirm,
        ).pack(pady=(0, 20), padx=30, fill="x")

    def change_qty(self, name, delta):
        val = self.quantities[name].get() + delta
        if val < 0:
            val = 0
        self.quantities[name].set(val)
        self.update_total()

    def update_total(self):
        total = 0
        for name, price in self.items:
            total += self.quantities[name].get() * price
        self.total_lbl.configure(text=f"TỔNG CỘNG: {total:,.0f} VNĐ")

    def confirm(self):
        room = self.room_cb.get()
        if room == "Không có phòng trống":
            return messagebox.showerror(
                "Lỗi", "Hiện tại không có phòng nào đang có khách lưu trú!"
            )

        total = 0
        order_details = []
        updates = []

        for name, price, stock in self.items:
            q = self.quantities[name].get()
            if q > 0:
                if q > stock:
                    return messagebox.showerror(
                        "Hết hàng",
                        f"Món '{name}' trong kho chỉ còn {stock} phần, không đủ để giao!",
                    )
                total += q * price
                order_details.append(f"{name} (x{q})")
                updates.append((q, name))

        if total == 0:
            return messagebox.showwarning("Chú ý", "Vui lòng chọn ít nhất một món đồ!")

        items_str = ", ".join(order_details)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            for qty, name in updates:
                db.cursor.execute(
                    "UPDATE inventory SET stock = stock - ? WHERE item_name = ? AND stock >= ?",
                    (qty, name, qty),
                )
                if db.cursor.rowcount == 0:
                    raise ValueError(
                        f"Sản phẩm '{name}' vừa mới hết hàng hoặc không đủ tồn kho để cung cấp!"
                    )

            db.cursor.execute(
                """
                INSERT INTO service_orders (room_id, items_detail, total_price, order_date, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (room, items_str, total, now_str, "Chờ xử lý"),
            )
            db.conn.commit()

            total_f = f"{int(total):,}".replace(",", ".")
            messagebox.showinfo(
                "Thành công",
                f"Đơn hàng đã được tiếp nhận!\nPhòng: {room}\nTổng: {total_f} VNĐ",
            )
            self.destroy()
        except Exception as e:
            db.conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể lưu đơn: {str(e)}")


class ServiceFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        ctk.CTkScrollableFrame.__init__(
            self, master, fg_color=COLOR_CREAM, corner_radius=0
        )
        ctk.CTkLabel(
            self, text="Dịch Vụ Đồ Uống & F&B", font=FONT_HEADER, text_color=COLOR_TEXT
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
            ("Phân loại", ["Mọi phân loại", "Đồ ăn", "Đồ uống"]),
            ("Mức giá", ["Mọi mức giá", "Dưới 50k", "50k - 100k", "Trên 100k"]),
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
            text="LỌC DỊCH VỤ",
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
            "category": self.filter_vars["Phân loại"].get(),
            "price_range": self.filter_vars["Mức giá"].get(),
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
        img_h = int(img_w * 0.65)

        logical_img_w = int(img_w / scale)
        logical_img_h = int(img_h / scale)

        services = [
            (
                "Rượu Vang Đỏ Cao Cấp",
                "Hương vị nồng nàn từ những vùng nho nổi tiếng thế giới.",
                "service-wine.png",
                "Đồ uống",
                "Trên 100k",
            ),
            (
                "Bia Nhập Khẩu",
                "Tiger, Heineken và các dòng bia thủ công mát lạnh.",
                "service-beer.png",
                "Đồ uống",
                "Dưới 50k",
            ),
            (
                "Nước Ngọt & Soda",
                "Coca-Cola, Pepsi và các loại nước giải khát đa dạng.",
                "service-softdrink.png",
                "Đồ uống",
                "Dưới 50k",
            ),
            (
                "Champagne Sang Trọng",
                "Dành cho những khoảnh khắc kỷ niệm đặc biệt.",
                "service-champagne.png",
                "Đồ uống",
                "Trên 100k",
            ),
            (
                "Nước Ép Trái Cây",
                "Nguồn vitamin tự nhiên từ trái cây tươi trong ngày.",
                "service-juice.png",
                "Đồ uống",
                "50k - 100k",
            ),
            (
                "Nước Khoáng Tinh Khiết",
                "Sự lựa chọn thanh khiết và đảm bảo sức khỏe.",
                "service-water.png",
                "Đồ uống",
                "Dưới 50k",
            ),
            (
                "Cà Phê Đặc Sản",
                "Pha phin truyền thống hoặc Espresso thơm nồng đánh thức mọi giác quan buổi sáng.",
                "service-coffee.png",
                "Đồ uống",
                "50k - 100k",
            ),
            (
                "Trà Hoa Thượng Hạng",
                "Trà sen Tây Hồ, trà đào cam sả thanh khiết mang lại sự tĩnh tâm tinh tế.",
                "service-tea.png",
                "Đồ uống",
                "50k - 100k",
            ),
            (
                "Bánh Ngọt Pháp",
                "Bánh sừng bò croissant bơ tỏi, bánh mousse mềm mịn chuẩn vị Âu.",
                "service-pastry.png",
                "Đồ ăn",
                "50k - 100k",
            ),
        ]

        search_text = (
            self.search_var.get().lower() if hasattr(self, "search_var") else ""
        )
        cat_filter = filters["category"] if filters else "Mọi phân loại"
        price_filter = filters["price_range"] if filters else "Mọi mức giá"

        filtered_services = []
        for item in services:
            name, desc, img, cat, prc_cat = item

            if (
                search_text
                and search_text not in name.lower()
                and search_text not in desc.lower()
            ):
                continue
            if cat_filter != "Mọi phân loại" and cat != cat_filter:
                continue
            if price_filter != "Mọi mức giá" and prc_cat != price_filter:
                continue

            filtered_services.append(item)

        for i, (name, desc, img_name, _, _) in enumerate(filtered_services):
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
                    img_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                    img_lbl.pack(pady=10, padx=10, fill="x")

                    in_f, out_f = make_zoom_handler(
                        img_lbl, pil_img, ctk_img, img_w, img_h
                    )
                    img_lbl.bind("<Enter>", in_f)
                    img_lbl.bind("<Leave>", out_f)
                except:
                    ctk.CTkLabel(
                        card, text="[ Lỗi tải ảnh ]", width=img_w, height=img_h
                    ).pack()
            else:
                ctk.CTkLabel(
                    card, text="[ Ảnh dịch vụ ]", width=img_w, height=img_h
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

            btn_f = ctk.CTkFrame(card, fg_color="transparent")
            btn_f.pack(pady=(0, 20), padx=20, fill="x")

            ctk.CTkButton(
                btn_f,
                text="CHI TIẾT",
                fg_color="#3a3a50",
                text_color="white",
                font=FONT_BODY_BOLD,
                height=35,
                width=80,
                command=lambda n=name, d=desc, p=img_path: self.show_details(n, d, p),
            ).pack(side="left", padx=(0, 5), expand=True, fill="x")

            ctk.CTkButton(
                btn_f,
                text="ĐẶT HÀNG",
                fg_color=COLOR_GOLD,
                text_color="white",
                font=FONT_BODY_BOLD,
                height=35,
                width=80,
                command=lambda n=name: self.open_order_modal(n),
            ).pack(side="left", padx=(5, 0), expand=True, fill="x")

    def show_details(self, name, desc, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết dịch vụ" in pages:
            detail_page = pages["Chi tiết dịch vụ"]
            if hasattr(detail_page, "set_service"):
                detail_page.set_service(name, desc, img_path)
            sf = getattr(app, "switch_page", None)
            if callable(sf):
                sf("Chi tiết dịch vụ")

    def open_order_modal(self, category_name):
        OrderModal(self, category_name)
