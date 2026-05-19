from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db


class ReceptionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.tree = None

        # 1. Header giống CRUD: Tiêu đề nằm bên trái
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header,
            text="Hệ Thống Quản Lý Lễ Tân",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
        ).pack(side="left")

        # 2. Toolbar giống CRUD: Bo góc, có viền, chứa các nút bấm
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

        # Cụm nút bấm nằm bên phải Toolbar cho giống CRUD
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
            command=self.confirm_booking,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="NHẬN PHÒNG",
            fg_color="#27ae60",
            hover_color="#219150",
            width=120,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.check_in,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="THANH TOÁN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            width=120,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.check_out,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="🗑 HỦY ĐƠN",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.cancel_booking,
        ).pack(side="left", padx=5)

        # 3. Khu vực bảng dữ liệu
        self.setup_treeview()

    def setup_treeview(self):
        # Frame bao quanh Treeview có bo góc và viền giống CRUD
        f = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        f.pack(fill="both", expand=True)

        cols = (
            "ID",
            "Khách Hàng",
            "Phòng",
            "Ngày Nhận",
            "Ngày Trả",
            "Tổng Tiền",
            "Trạng Thái",
        )

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
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        db.cursor.execute(
            "SELECT id, customer_name, room_id, checkin_date, checkout_date, total_price, status FROM bookings WHERE status NOT IN ('Completed', 'Cancelled')"
        )
        for row in db.cursor.fetchall():
            b_id, cus, rm, cin, cout, price, status = row
            # Format chuẩn Việt Nam
            cin_f = datetime.strptime(cin, "%Y-%m-%d").strftime("%d/%m/%Y")
            cout_f = datetime.strptime(cout, "%Y-%m-%d").strftime("%d/%m/%Y")
            price_f = f"{int(price):,}".replace(",", ".")
            self.tree.insert(
                "", "end", values=(b_id, cus, rm, cin_f, cout_f, price_f, status)
            )

    def confirm_booking(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần xác nhận!")
        b_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[6]

        if status != "Pending":
            return messagebox.showerror("Lỗi", "Đơn này đã được xử lý rồi!")

        if messagebox.askyesno("Xác nhận", "Sếp đồng ý giữ chỗ cho khách này?"):
            db.cursor.execute(
                "UPDATE bookings SET status='Confirmed' WHERE id=?", (b_id,)
            )
            db.conn.commit()
            self.load_data()

    def check_in(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn khách đến nhận phòng!")
        b_id, _, rm_id, _, _, _, status = self.tree.item(item, "values")

        if status == "Stay-in":
            return messagebox.showerror("Lỗi", "Khách này đã nhận phòng rồi!")
        if status == "Pending":
            return messagebox.showerror(
                "Lỗi", "Đơn chưa XÁC NHẬN, không thể nhận phòng!"
            )

        if messagebox.askyesno("Xác nhận", f"Cho khách nhận phòng {rm_id}?"):
            db.cursor.execute(
                "UPDATE bookings SET status='Stay-in' WHERE id=?", (b_id,)
            )
            db.cursor.execute(
                "UPDATE rooms SET status='Đã đặt' WHERE room_id=?", (rm_id,)
            )
            db.conn.commit()
            self.load_data()

    def check_out(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn lượt cần thanh toán!")
        b_id, cus, rm_id, _, _, price, status = self.tree.item(item, "values")

        if status != "Stay-in":
            return messagebox.showerror(
                "Lỗi", "Chỉ khách đang ở mới có thể thanh toán!"
            )

        if messagebox.askyesno(
            "Thanh toán", f"Khách {cus} trả phòng {rm_id}. Xong chưa sếp?"
        ):
            try:
                real_price = float(price.replace(".", ""))
                db.cursor.execute(
                    "SELECT location FROM rooms WHERE room_id=?", (rm_id,)
                )
                loc = db.cursor.fetchone()[0]
                db.cursor.execute(
                    "INSERT INTO revenue_history (date, amount, location) VALUES (?,?,?)",
                    (datetime.now().strftime("%Y-%m-%d"), real_price, loc),
                )
                db.cursor.execute(
                    "UPDATE customers SET total_spending = total_spending + ? WHERE full_name=?",
                    (real_price, cus),
                )
                db.cursor.execute(
                    "UPDATE bookings SET status='Completed' WHERE id=?", (b_id,)
                )
                db.cursor.execute(
                    "UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,)
                )
                db.conn.commit()
                messagebox.showinfo("Thành công", "Đã thanh toán xong!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def cancel_booking(self):
        item = self.tree.selection()
        if not item:
            return
        b_id, _, rm_id, _, _, _, _ = self.tree.item(item, "values")
        if messagebox.askyesno("Hủy đơn", "Sếp chắc chắn muốn hủy đơn này?"):
            db.cursor.execute(
                "UPDATE bookings SET status='Cancelled' WHERE id=?", (b_id,)
            )
            db.cursor.execute(
                "UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,)
            )
            db.conn.commit()
            self.load_data()
