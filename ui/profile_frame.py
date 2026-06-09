import os
from PIL import Image, ImageOps
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
from config import *
from database import db


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.app = master.master
        self.info_label = None
        self.email_label = None
        self.phone_label = None
        self.tree = None
        self.coupon_scroll = None

        self.panel = ctk.CTkFrame(
            self,
            width=900,
            height=700,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.panel.place(relx=0.5, rely=0.5, anchor="center")
        self.panel.pack_propagate(False)

        self.tabview = ctk.CTkTabview(
            self.panel,
            fg_color="transparent",
            segmented_button_selected_color=COLOR_GOLD,
            segmented_button_selected_hover_color=COLOR_GOLD_HOVER,
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        self.tabview._segmented_button.configure(
            font=("Segoe UI", 14, "bold"), height=38
        )

        self.tab_info = self.tabview.add("👤 THÔNG TIN")
        self.tab_history = self.tabview.add("📜 LỊCH SỬ ĐẶT")
        self.tab_coupons = self.tabview.add("🎁 KHO VOUCHER")

        self.setup_info_tab()
        self.setup_history_tab()
        self.setup_coupons_tab()

    def setup_info_tab(self):
        container = ctk.CTkFrame(self.tab_info, fg_color="transparent")
        container.pack(expand=True)

        self.avatar_border_frame = ctk.CTkFrame(
            container,
            fg_color="transparent",
            corner_radius=10,
            border_width=2,
            border_color=COLOR_GOLD,
        )
        self.avatar_border_frame.pack(pady=(10, 5))

        self.avatar_label = ctk.CTkLabel(
            self.avatar_border_frame, text="👤", font=FONT_ICON
        )
        self.avatar_label.pack(padx=2, pady=2)

        self.btn_change_avatar = ctk.CTkButton(
            container,
            text="ĐỔI ẢNH",
            width=120,
            height=32,
            font=("Segoe UI", 14, "bold"),
            fg_color="#3a3a50",
            text_color="white",
            hover_color=COLOR_GOLD_HOVER,
            command=self.change_avatar,
        )
        self.btn_change_avatar.pack(pady=(0, 10))

        self.info_label = ctk.CTkLabel(
            container, text="Sếp: ...", font=FONT_TITLE, text_color=COLOR_GOLD
        )
        self.info_label.pack(pady=10)

        self.email_label = ctk.CTkLabel(
            container, text="Email: ...", font=FONT_BODY, text_color="#aaa"
        )
        self.email_label.pack()

        self.phone_label = ctk.CTkLabel(
            container, text="SĐT: ...", font=FONT_BODY, text_color="#aaa"
        )
        self.phone_label.pack(pady=5)

        btn_f = ctk.CTkFrame(container, fg_color="transparent")
        btn_f.pack(pady=30)

        ctk.CTkButton(
            btn_f,
            text="CHỈNH SỬA HỒ SƠ",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_BODY_BOLD,
            width=180,
            height=40,
            command=self.open_edit_modal,
        ).pack(side="left", padx=10)

        def do_logout():
            func = getattr(self.app, "logout", None)
            if callable(func):
                func()

        ctk.CTkButton(
            btn_f,
            text="ĐĂNG XUẤT",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white",
            font=FONT_BODY_BOLD,
            width=180,
            height=40,
            command=do_logout,
        ).pack(side="left", padx=10)

    def setup_history_tab(self):
        cols = ("Mã", "Phòng", "Ngày Nhận", "Ngày Trả", "Tổng Tiền", "Trạng Thái")
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Treeview",
            background=COLOR_NAVY,
            foreground="white",
            fieldbackground=COLOR_NAVY,
            rowheight=35,
            borderwidth=0,
        )
        style.map("Custom.Treeview", background=[("selected", COLOR_GOLD)])

        self.tree = ttk.Treeview(
            self.tab_history, columns=cols, show="headings", style="Custom.Treeview"
        )
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_coupons_tab(self):
        self.coupon_scroll = ctk.CTkScrollableFrame(
            self.tab_coupons, fg_color="transparent"
        )
        self.coupon_scroll.pack(fill="both", expand=True)

    def load_data(self):
        if not hasattr(self.app, "current_username") or not self.app.current_username:
            return

        user_res = db.execute_query(
            "SELECT full_name, email, phone, username FROM users WHERE username=?",
            (self.app.current_username,),
            fetchone=True,
        )
        if user_res:
            self.info_label.configure(text=f"Tài khoản: {user_res[0].upper()}")
            self.email_label.configure(text=f"Email: {user_res[1]}")
            self.phone_label.configure(text=f"Số điện thoại: {user_res[2]}")
            username = user_res[3]

            self.load_avatar_image()

            for i in self.tree.get_children():
                self.tree.delete(i)
            bookings_res = db.execute_query(
                "SELECT id, room_id, checkin_date, checkout_date, total_price, status FROM bookings WHERE customer_id=?",
                (self.app.current_username,),
                fetch=True,
            )
            if bookings_res:
                for row in bookings_res:
                    rid, r_id, cin, cout, prc, stt = row
                    cin_f = datetime.strptime(cin, "%Y-%m-%d").strftime("%d/%m/%Y")
                    cout_f = datetime.strptime(cout, "%Y-%m-%d").strftime("%d/%m/%Y")
                    prc_f = f"{int(prc):,}".replace(",", ".")
                    self.tree.insert(
                        "", "end", values=(rid, r_id, cin_f, cout_f, prc_f, stt)
                    )

            for w in self.coupon_scroll.winfo_children():
                w.destroy()
            coupons = db.execute_query(
                "SELECT code, description, discount_percent FROM user_coupons WHERE username=?",
                (username,),
                fetch=True,
            )
            if not coupons:
                ctk.CTkLabel(
                    self.coupon_scroll,
                    text="Bạn chưa có voucher nào. Hãy tham gia sự kiện để nhận quà!",
                    font=FONT_BODY,
                    text_color="#888",
                ).pack(pady=50)
            else:
                for code, desc, disc in coupons:
                    f = ctk.CTkFrame(
                        self.coupon_scroll, fg_color=COLOR_NAVY, corner_radius=10
                    )
                    f.pack(fill="x", pady=5, padx=10)
                    ctk.CTkLabel(f, text="🎟️", font=("Segoe UI", 30)).pack(
                        side="left", padx=20
                    )
                    txt_f = ctk.CTkFrame(f, fg_color="transparent")
                    txt_f.pack(side="left", fill="both", expand=True, pady=10)
                    ctk.CTkLabel(
                        txt_f,
                        text=f"Code: {code} (-{disc}%)",
                        font=FONT_BODY,
                        text_color=COLOR_GOLD,
                    ).pack(anchor="w")
                    ctk.CTkLabel(
                        txt_f, text=desc, font=FONT_BODY, text_color="#ccc"
                    ).pack(anchor="w")

                    def use_coupon(c_code=code, c_disc=disc):
                        self.app.active_coupon = (c_code, c_disc)
                        messagebox.showinfo(
                            "Kích hoạt thành công",
                            f"Đã kích hoạt mã giảm giá {c_code} (-{c_disc}%)!\n"
                            f"Hệ thống đang chuyển sếp sang trang Phòng Nghỉ để đặt phòng với giá ưu đãi.",
                            parent=self.winfo_toplevel(),
                        )
                        func = getattr(self.app, "switch_page", None)
                        if callable(func):
                            func("Phòng nghỉ")

                    ctk.CTkButton(
                        f,
                        text="DÙNG NGAY",
                        width=100,
                        fg_color="transparent",
                        border_width=1,
                        border_color=COLOR_GOLD,
                        text_color=COLOR_GOLD,
                        command=use_coupon,
                    ).pack(side="right", padx=20)

    def open_edit_modal(self):
        data = db.execute_query(
            "SELECT full_name, email, phone, username FROM users WHERE username=?",
            (self.app.current_username,),
            fetchone=True,
        )
        if not data:
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Chỉnh sửa hồ sơ")
        w, h = 400, 650
        modal.update_idletasks()
        main_win = self.winfo_toplevel()
        x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
        y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
        modal.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        modal.configure(fg_color=COLOR_CREAM)
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal, text="CẬP NHẬT THÔNG TIN", font=FONT_LABEL, text_color=COLOR_GOLD
        ).pack(pady=15)

        entries = {}
        fields = [
            ("Họ và Tên", data[0], False),
            ("Email", data[1], False),
            ("Số điện thoại", data[2], False),
            ("Mật khẩu mới (để trống nếu không đổi)", "", True),
            ("Nhập lại mật khẩu mới", "", True),
        ]

        for label, val, is_password in fields:
            f = ctk.CTkFrame(modal, fg_color="transparent")
            f.pack(fill="x", padx=40, pady=5)
            ctk.CTkLabel(f, text=label, font=FONT_BODY, text_color=COLOR_TEXT).pack(
                anchor="w"
            )
            e = ctk.CTkEntry(
                f,
                fg_color=COLOR_WHITE,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
                height=40,
                show="*" if is_password else "",
            )
            e.insert(0, val)
            e.pack(fill="x", pady=5)
            entries[label] = e

        def save():
            new_name = entries["Họ và Tên"].get()
            new_email = entries["Email"].get()
            new_phone = entries["Số điện thoại"].get()
            new_pass = entries["Mật khẩu mới (để trống nếu không đổi)"].get()
            confirm_pass = entries["Nhập lại mật khẩu mới"].get()

            if not new_name or not new_email:
                return messagebox.showwarning(
                    "Lỗi", "Không được để trống Tên hoặc Email!"
                )

            if new_pass:
                if new_pass != confirm_pass:
                    return messagebox.showerror("Lỗi", "Mật khẩu mới không trùng khớp!")

            try:
                db.update_user_profile(
                    data[3],
                    getattr(self.app, "current_user", ""),
                    new_name,
                    new_email,
                    new_phone,
                    new_pass if new_pass else None
                )

                setattr(self.app, "current_user", new_name)
                self.load_data()

                pages = getattr(self.app, "pages", {})
                mgmt_page = pages.get("Quản lý")
                if mgmt_page and hasattr(mgmt_page, "update_user"):
                    curr_role = getattr(self.app, "current_role", None)
                    mgmt_page.update_user(new_name, curr_role)

                modal.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật hồ sơ sếp!")
            except Exception as err:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(err)}")

        ctk.CTkButton(
            modal,
            text="LƯU THAY ĐỔI",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_LABEL,
            height=45,
            command=save,
        ).pack(pady=30, padx=40, fill="x")

    def load_avatar_image(self):
        if not hasattr(self.app, "current_username") or not self.app.current_username:
            return

        avatar_path = os.path.join(
            IMAGE_DIR, "avatars", f"{self.app.current_username}.png"
        )
        if os.path.exists(avatar_path):
            try:
                pil_img = Image.open(avatar_path).convert("RGB")
                ctk_img = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=(300, 300)
                )
                self.avatar_label.configure(image=ctk_img, text="")
                self.avatar_img_ref = ctk_img
            except:
                self.avatar_label.configure(text="👤", font=FONT_ICON, image=None)
        else:
            self.avatar_label.configure(text="👤", font=FONT_ICON, image=None)

    def change_avatar(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp")],
        )
        if not file_path:
            return

        def on_crop_success(cropped_img):
            try:
                avatar_dir = os.path.join(IMAGE_DIR, "avatars")
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)

                avatar_path = os.path.join(
                    avatar_dir, f"{self.app.current_username}.png"
                )
                cropped_img.save(avatar_path, "PNG")

                self.load_avatar_image()

                app = self.winfo_toplevel()
                header = getattr(app, "header", None)
                if header and hasattr(header, "update_user_avatar"):
                    header.update_user_avatar(self.app.current_username)

                messagebox.showinfo("Thành công", "Đã cập nhật ảnh đại diện của sếp!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")

        AvatarCropModal(self, file_path, on_crop_success)


class AvatarCropModal(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback):
        super().__init__(parent)
        self.title("Điều chỉnh ảnh đại diện")
        self.configure(fg_color=COLOR_CREAM)
        self.transient(parent)
        self.grab_set()

        w, h = 500, 680
        self.update_idletasks()
        main_win = parent.winfo_toplevel()
        x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
        y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        self.resizable(False, False)

        self.callback = callback
        self.original_image = Image.open(image_path)

        orig_w, orig_h = self.original_image.size
        if orig_w < orig_h:
            new_w = 200
            new_h = int(orig_h * (200 / orig_w))
        else:
            new_h = 200
            new_w = int(orig_w * (200 / orig_h))

        self.base_image = self.original_image.resize(
            (new_w, new_h), Image.Resampling.LANCZOS
        )

        self.zoom_factor = 1.0
        self.img_x = (300 - new_w) // 2
        self.img_y = (300 - new_h) // 2
        self.clamp_offsets()

        self.drag_start_x = 0
        self.drag_start_y = 0

        ctk.CTkLabel(
            self,
            text="KÉO ĐỂ DI CHUYỂN / THAY ĐỔI KÍCH CỠ",
            font=FONT_LABEL,
            text_color=COLOR_GOLD,
        ).pack(pady=20)

        self.canvas = ctk.CTkCanvas(
            self, width=300, height=300, bg=COLOR_WHITE, highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=30)

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_image)

        slider_f = ctk.CTkFrame(self, fg_color="transparent")
        slider_f.pack(fill="x", padx=40, pady=15)
        ctk.CTkLabel(slider_f, text="Phóng to:", font=FONT_BODY).pack(side="left")

        self.zoom_slider = ctk.CTkSlider(
            slider_f,
            from_=1.0,
            to=5.0,
            number_of_steps=100,
            button_color=COLOR_GOLD,
            button_hover_color=COLOR_GOLD_HOVER,
            progress_color=COLOR_GOLD,
            command=self.on_zoom,
        )
        self.zoom_slider.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.zoom_slider.set(1.0)

        ctk.CTkButton(
            self,
            text="CẮT & LƯU LÀM AVATAR",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            font=FONT_BODY_BOLD,
            height=45,
            command=self.confirm_crop,
        ).pack(pady=25, padx=40, fill="x")

        self.update_canvas()

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def drag_image(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.img_x += dx
        self.img_y += dy
        self.clamp_offsets()

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self.update_canvas()

    def on_zoom(self, val):
        old_zoom = self.zoom_factor
        self.zoom_factor = float(val)

        center_x, center_y = 150, 150
        self.img_x = int(
            center_x - (center_x - self.img_x) * (self.zoom_factor / old_zoom)
        )
        self.img_y = int(
            center_y - (center_y - self.img_y) * (self.zoom_factor / old_zoom)
        )
        self.clamp_offsets()

        self.update_canvas()

    def clamp_offsets(self):
        w = int(self.base_image.width * self.zoom_factor)
        h = int(self.base_image.height * self.zoom_factor)

        if w >= 200:
            self.img_x = max(250 - w, min(50, self.img_x))
        else:
            self.img_x = (300 - w) // 2

        if h >= 200:
            self.img_y = max(250 - h, min(50, self.img_y))
        else:
            self.img_y = (300 - h) // 2

    def update_canvas(self):
        self.canvas.delete("all")

        w = int(self.base_image.width * self.zoom_factor)
        h = int(self.base_image.height * self.zoom_factor)
        resized = self.base_image.resize((w, h), Image.Resampling.LANCZOS)

        from PIL import ImageTk

        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.create_image(
            self.img_x, self.img_y, anchor="nw", image=self.tk_image
        )

        self.canvas.create_rectangle(49, 49, 251, 251, outline="#131324", width=3)
        self.canvas.create_rectangle(
            50, 50, 250, 250, outline=COLOR_GOLD, width=2, dash=(5, 3)
        )

    def confirm_crop(self):
        zoom_w = int(self.base_image.width * self.zoom_factor)

        crop_x1 = 50 - self.img_x
        crop_y1 = 50 - self.img_y
        crop_x2 = 250 - self.img_x
        crop_y2 = 250 - self.img_y

        scale_factor = self.original_image.width / zoom_w

        orig_crop_x1 = int(crop_x1 * scale_factor)
        orig_crop_y1 = int(crop_y1 * scale_factor)
        orig_crop_x2 = int(crop_x2 * scale_factor)
        orig_crop_y2 = int(crop_y2 * scale_factor)

        try:
            cropped = self.original_image.crop(
                (orig_crop_x1, orig_crop_y1, orig_crop_x2, orig_crop_y2)
            )
            final_avatar = cropped.resize((350, 350), Image.Resampling.LANCZOS)
            self.callback(final_avatar)
            self.destroy()
        except:
            messagebox.showerror(
                "Lỗi",
                "Vùng cắt nằm ngoài phạm vi ảnh hoặc không hợp lệ. Vui lòng kéo ảnh nằm trong khung nét đứt!",
            )
