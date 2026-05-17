import os
from config import *
from PIL import Image
from tkinter import messagebox
from database import db

SUB_SERVICES = {
    "Rượu Vang Đỏ Cao Cấp": [("Chateau Margaux 2015", 5500000), ("Penfolds Bin 389", 2800000), ("Casillero del Diablo", 850000)],
    "Bia Nhập Khẩu": [("Heineken Silver", 45000), ("Tiger Crystal", 40000), ("Bia Thủ Công IPA", 95000), ("Corona Extra", 55000)],
    "Nước Ngọt & Soda": [("Coca Cola Classic", 25000), ("Pepsi Black", 25000), ("7Up Lemon", 25000), ("Sprite", 25000), ("Schweppes Soda", 30000)],
    "Champagne Sang Trọng": [("Moët & Chandon", 3500000), ("Dom Pérignon", 8200000), ("Veuve Clicquot", 4100000)],
    "Nước Ép Trái Cây": [("Nước Ép Cam Tươi", 65000), ("Nước Ép Dưa Hấu", 60000), ("Nước Ép Thơm", 60000), ("Sinh Tố Bơ", 85000)],
    "Nước Khoáng Tinh Khiết": [("Lavie 500ml", 15000), ("Aquafina 500ml", 15000), ("Evian Glass Bottle", 110000), ("Perrier Sparkling", 95000)]
}

class OrderModal(ctk.CTkToplevel):
    def __init__(self, parent, category_name):
        super().__init__(parent)
        self.title(f"Đặt hàng: {category_name}")
        self.geometry("500x700")
        self.configure(fg_color=COLOR_CREAM)
        self.grab_set()
        
        self.items = SUB_SERVICES.get(category_name, [])
        self.quantities = {item[0]: ctk.IntVar(value=0) for item in self.items}
        
        ctk.CTkLabel(self, text=category_name.upper(), font=("Segoe UI", 20, "bold"), text_color=COLOR_GOLD).pack(pady=20)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=350)
        self.scroll.pack(fill="both", expand=True, padx=20)
        
        for name, price in self.items:
            f = ctk.CTkFrame(self.scroll, fg_color=COLOR_WHITE, corner_radius=10)
            f.pack(fill="x", pady=5)
            
            ctk.CTkLabel(f, text=name, font=("Segoe UI", 13, "bold"), text_color=COLOR_NAVY).pack(side="left", padx=15, pady=10)
            
            qty_f = ctk.CTkFrame(f, fg_color="transparent")
            qty_f.pack(side="right", padx=10)
            
            ctk.CTkButton(qty_f, text="-", width=30, height=30, fg_color="#e74c3c", 
                          command=lambda n=name: self.change_qty(n, -1)).pack(side="left", padx=2)
            
            ctk.CTkEntry(qty_f, textvariable=self.quantities[name], width=40, height=30, 
                         justify="center").pack(side="left", padx=2)
            
            ctk.CTkButton(qty_f, text="+", width=30, height=30, fg_color="#27ae60", 
                          command=lambda n=name: self.change_qty(n, 1)).pack(side="left", padx=2)
            
            ctk.CTkLabel(f, text=f"{price:,.0f}đ", font=("Segoe UI", 12), text_color=COLOR_GOLD, 
                         width=80).pack(side="right", padx=10)

        bottom_f = ctk.CTkFrame(self, fg_color=COLOR_NAVY, corner_radius=0)
        bottom_f.pack(fill="x", side="bottom", pady=0)
        
        room_f = ctk.CTkFrame(bottom_f, fg_color="transparent")
        room_f.pack(fill="x", padx=30, pady=15)
        
        ctk.CTkLabel(room_f, text="Giao đến phòng:", font=("Segoe UI", 12, "bold")).pack(side="left")
        
        db.cursor.execute("SELECT room_id FROM rooms WHERE status='Đã đặt'")
        occupied_rooms = [r[0] for r in db.cursor.fetchall()]
        if not occupied_rooms: occupied_rooms = ["Không có phòng trống"]
        
        self.room_cb = ctk.CTkOptionMenu(room_f, values=occupied_rooms, fg_color=COLOR_WHITE, 
                                         text_color=COLOR_NAVY, button_color=COLOR_GOLD)
        self.room_cb.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        self.total_lbl = ctk.CTkLabel(bottom_f, text="TỔNG CỘNG: 0 VNĐ", font=("Segoe UI", 18, "bold"), text_color=COLOR_GOLD)
        self.total_lbl.pack(pady=10)
        
        ctk.CTkButton(bottom_f, text="XÁC NHẬN ĐƠN HÀNG", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      height=45, font=("Segoe UI", 14, "bold"), command=self.confirm).pack(pady=(0, 20), padx=30, fill="x")

    def change_qty(self, name, delta):
        val = self.quantities[name].get() + delta
        if val < 0: val = 0
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
            return messagebox.showerror("Lỗi", "Hiện tại không có phòng nào đang có khách lưu trú!")
        
        total = 0
        order_details = []
        for name, price in self.items:
            q = self.quantities[name].get()
            if q > 0:
                total += q * price
                order_details.append(f"- {name} (x{q})")
        
        if total == 0:
            return messagebox.showwarning("Chú ý", "Vui lòng chọn ít nhất một món đồ!")
            
        msg = f"Xác nhận đơn hàng giao tới phòng {room}:\n" + "\n".join(order_details) + f"\n\nTổng thanh toán: {total:,.0f} VNĐ"
        if messagebox.askyesno("Xác nhận", msg):
            messagebox.showinfo("Thành công", f"Đơn hàng đang được chuẩn bị và sẽ giao tới phòng {room} sau ít phút!")
            self.destroy()

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
            
            btn_f = ctk.CTkFrame(card, fg_color="transparent")
            btn_f.pack(pady=(0, 20), padx=20, fill="x")
            
            ctk.CTkButton(btn_f, text="CHI TIẾT", fg_color="#3a3a50", text_color="white", 
                          font=("Segoe UI", 11, "bold"), height=35, width=80,
                          command=lambda n=name, d=desc, p=img_path: self.show_details(n, d, p)).pack(side="left", padx=5, expand=True, fill="x")
            
            ctk.CTkButton(btn_f, text="ĐẶT HÀNG", fg_color=COLOR_GOLD, text_color="white", 
                          font=("Segoe UI", 11, "bold"), height=35, width=80,
                          command=lambda n=name: self.open_order_modal(n)).pack(side="left", padx=5, expand=True, fill="x")

    def show_details(self, name, desc, img_path):
        app = self.winfo_toplevel()
        pages = getattr(app, "pages", {})
        if "Chi tiết dịch vụ" in pages:
            detail_page = pages["Chi tiết dịch vụ"]
            if hasattr(detail_page, "set_service"):
                detail_page.set_service(name, desc, img_path)
            sf = getattr(app, "switch_page", None)
            if callable(sf): sf("Chi tiết dịch vụ")

    def open_order_modal(self, category_name):
        OrderModal(self, category_name)