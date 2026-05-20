from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db

class OrderMgmtFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.tree = None

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header, text="Quản Lý Đơn Hàng (F&B)", font=FONT_TITLE, text_color=COLOR_TEXT
        ).pack(side="left")

        toolbar = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            height=70,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_data)
        
        ctk.CTkEntry(
            toolbar,
            placeholder_text="Tìm kiếm nhanh...",
            width=250,
            textvariable=self.search_var,
            fg_color=COLOR_NAVY,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
        ).pack(side="left", padx=20, pady=15)

        btn_f = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_f.pack(side="right", padx=15)

        ctk.CTkButton(
            btn_f,
            text="XÁC NHẬN ĐƠN",
            fg_color="#3498db",
            hover_color="#2980b9",
            width=120,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.confirm_order,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="ĐANG GIAO",
            fg_color="#27ae60",
            hover_color="#219150",
            width=120,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.deliver_order,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="THANH TOÁN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            width=120,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.pay_order,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="🗑 HỦY ĐƠN",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.cancel_order,
        ).pack(side="left", padx=5)

        self.setup_treeview()

    def setup_treeview(self):
        f = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        f.pack(fill="both", expand=True)

        cols = ("ID", "Mã Phòng", "Chi Tiết Món", "Tổng Tiền", "Thời Gian", "Trạng Thái")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=COLOR_NAVY,
            foreground=COLOR_TEXT,
            rowheight=35,
            fieldbackground=COLOR_NAVY,
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", COLOR_GOLD)])
        style.configure(
            "Treeview.Heading",
            background=COLOR_WHITE,
            foreground=COLOR_GOLD,
            font=FONT_BODY_BOLD,
        )

        self.tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.upper())
            if c == "Chi Tiết Món":
                self.tree.column(c, width=300, anchor="w")
            else:
                self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        db.cursor.execute(
            "SELECT id, room_id, items_detail, total_price, order_date, status FROM service_orders WHERE status NOT IN ('Completed', 'Cancelled') ORDER BY order_date DESC"
        )
        self.all_data = db.cursor.fetchall()
        self.display_data(self.all_data)

    def display_data(self, data_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data_list:
            o_id, rm, detail, total, date, status = row
            date_f = datetime.strptime(date, "%Y-%m-%d %H:%M").strftime("%d/%m/%Y %H:%M")
            total_f = f"{int(total):,}".replace(",", ".")
            self.tree.insert("", "end", values=(o_id, rm, detail, total_f, date_f, status))

    def filter_data(self, *args):
        search_text = self.search_var.get().lower()
        filtered = []
        for row in self.all_data:
            if any(search_text in str(val).lower() for val in row):
                filtered.append(row)
        self.display_data(filtered)

    def confirm_order(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần xác nhận!")
        o_id, _, _, _, _, status = self.tree.item(item, "values")

        if status != "Chờ xử lý":
            return messagebox.showerror("Lỗi", "Đơn hàng này đã được xác nhận trước đó!")

        if messagebox.askyesno("Xác nhận", "Sếp duyệt chuẩn bị làm món cho đơn này?"):
            db.cursor.execute("UPDATE service_orders SET status='Đã xác nhận' WHERE id=?", (o_id,))
            db.conn.commit()
            self.load_data()

    def deliver_order(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần đi giao!")
        o_id, _, _, _, _, status = self.tree.item(item, "values")

        if status == "Đang giao":
            return messagebox.showerror("Lỗi", "Đơn hàng này đang trên đường giao rồi!")
        if status == "Chờ xử lý":
            return messagebox.showerror("Lỗi", "Đơn chưa được XÁC NHẬN, không thể đi giao!")

        if messagebox.askyesno("Xác nhận", "Xác nhận nhân viên bắt đầu đi giao món?"):
            db.cursor.execute("UPDATE service_orders SET status='Đang giao' WHERE id=?", (o_id,))
            db.conn.commit()
            self.load_data()

    def pay_order(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần thanh toán!")
        o_id, rm_id, _, total, _, status = self.tree.item(item, "values")

        if status != "Đang giao":
            return messagebox.showerror("Lỗi", "Chỉ đơn hàng đang đi giao mới có thể thanh toán!")

        if messagebox.askyesno("Thanh toán", f"Xác nhận đã thu {total} VNĐ từ phòng {rm_id}?"):
            try:
                real_price = float(total.replace(".", ""))
                
                db.cursor.execute("SELECT location FROM rooms WHERE room_id=?", (rm_id,))
                loc = db.cursor.fetchone()[0]
                db.cursor.execute("INSERT INTO revenue_history (date, amount, location) VALUES (?,?,?)",
                                  (datetime.now().strftime("%Y-%m-%d"), real_price, loc))
                
                db.cursor.execute("SELECT customer_name FROM bookings WHERE room_id=? AND status='Stay-in'", (rm_id,))
                res = db.cursor.fetchone()
                guest_name = res[0] if res else "Khách vãng lai"
                
                if guest_name != "Khách vãng lai":
                    db.cursor.execute("UPDATE customers SET total_spending = total_spending + ? WHERE full_name=?", (real_price, guest_name))
                
                db.cursor.execute("UPDATE service_orders SET status='Completed' WHERE id=?", (o_id,))
                db.conn.commit()
                messagebox.showinfo("Thành công", "Đã thanh toán đơn hàng thành công!")
                self.load_data()
            except Exception as e:
                db.conn.rollback()
                messagebox.showerror("Lỗi", str(e))

    def cancel_order(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần hủy!")
        o_id, _, detail, _, _, _ = self.tree.item(item, "values")

        if messagebox.askyesno("Hủy đơn", "Sếp chắc chắn muốn hủy đơn và hoàn trả kho?"):
            try:
                items = detail.split(", ")
                for item_str in items:
                    name = item_str.split(" (x")[0]
                    qty = int(item_str.split(" (x")[1].replace(")", ""))
                    db.cursor.execute(
                        "UPDATE inventory SET stock = stock + ? WHERE item_name = ?",
                        (qty, name)
                    )
                
                db.cursor.execute("UPDATE service_orders SET status='Cancelled' WHERE id=?", (o_id,))
                db.conn.commit()
                messagebox.showinfo("Thành công", "Đã hủy đơn hàng và hoàn lại tồn kho!")
                self.load_data()
            except Exception as e:
                db.conn.rollback()
                messagebox.showerror("Lỗi", f"Không thể hủy đơn: {str(e)}")