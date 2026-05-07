from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db

class ReceptionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.tree = None

        ctk.CTkLabel(self, text="Hệ Thống Quản Lý Lễ Tân", font=("Segoe UI", 24, "bold"),
                     text_color=COLOR_TEXT).pack(pady=15)

        self.tool_f = ctk.CTkFrame(self, fg_color="transparent")
        self.tool_f.pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(self.tool_f, text="XÁC NHẬN ĐƠN", fg_color="#3498db", hover_color="#2980b9",
                      font=("Segoe UI", 12, "bold"), width=140, height=40,
                      command=self.confirm_booking).pack(side="left", padx=5)

        ctk.CTkButton(self.tool_f, text="NHẬN PHÒNG (CHECK-IN)", fg_color="#27ae60", hover_color="#219150",
                      font=("Segoe UI", 12, "bold"), width=160, height=40,
                      command=self.check_in).pack(side="left", padx=5)

        ctk.CTkButton(self.tool_f, text="THANH TOÁN (CHECK-OUT)", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      font=("Segoe UI", 12, "bold"), width=170, height=40,
                      command=self.check_out).pack(side="left", padx=5)

        ctk.CTkButton(self.tool_f, text="HỦY ĐƠN", fg_color="#e74c3c", hover_color="#c0392b",
                      font=("Segoe UI", 12, "bold"), width=100, height=40,
                      command=self.cancel_booking).pack(side="right", padx=5)

        self.setup_treeview()

    def setup_treeview(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=20, pady=20)
        cols = ("ID", "Khách Hàng", "Phòng", "Ngày Nhận", "Ngày Trả", "Tổng Tiền", "Trạng Thái")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=COLOR_NAVY, foreground=COLOR_TEXT, rowheight=35,
                        fieldbackground=COLOR_NAVY, bordercolor=COLOR_BORDER, borderwidth=1)
        style.map('Treeview', background=[('selected', COLOR_GOLD)], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading", background=COLOR_WHITE, foreground=COLOR_GOLD,
                        font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        db.cursor.execute(
            "SELECT id, customer_name, room_id, checkin_date, checkout_date, total_price, status FROM bookings WHERE status NOT IN ('Completed', 'Cancelled')")
        for row in db.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def confirm_booking(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần xác nhận!")
        b_id, _, _, _, _, _, status = self.tree.item(item, "values")

        if status != "Pending":
            return messagebox.showerror("Lỗi", "Đơn này đã được xác nhận từ trước!")

        if messagebox.askyesno("Xác nhận", "Sếp đồng ý giữ chỗ cho khách này?"):
            db.cursor.execute("UPDATE bookings SET status='Confirmed' WHERE id=?", (b_id,))
            db.conn.commit()
            self.load_data()
        return None

    def check_in(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Chú ý", "Hãy chọn đơn khách đến nhận phòng!")
        b_id, _, rm_id, _, _, _, status = self.tree.item(item, "values")

        if status == "Stay-in":
            return messagebox.showerror("Lỗi", "Khách này đã ở trong phòng rồi!")
        if status == "Pending":
            return messagebox.showerror("Lỗi", "Đơn này chưa được XÁC NHẬN, không thể Check-in!")

        if messagebox.askyesno("Check-in", f"Xác nhận cho khách nhận phòng {rm_id}?"):
            db.cursor.execute("UPDATE bookings SET status='Stay-in' WHERE id=?", (b_id,))
            db.cursor.execute("UPDATE rooms SET status='Đã đặt' WHERE room_id=?", (rm_id,))
            db.conn.commit()
            self.load_data()
        return None

    def check_out(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Chú ý", "Hãy chọn lượt cần thanh toán!")
        b_id, cus, rm_id, _, _, price, status = self.tree.item(item, "values")

        if status != "Stay-in":
            return messagebox.showerror("Lỗi", "Chỉ khách đang ở mới có thể thanh toán!")

        if messagebox.askyesno("Thanh toán", f"Khách {cus} trả phòng {rm_id}. Tổng thu: {float(price):,.0f} VNĐ?"):
            try:
                db.cursor.execute("SELECT location FROM rooms WHERE room_id=?", (rm_id,))
                loc = db.cursor.fetchone()[0]
                db.cursor.execute("INSERT INTO revenue_history (date, amount, location) VALUES (?,?,?)",
                                  (datetime.now().strftime("%Y-%m-%d"), float(price), loc))

                db.cursor.execute("UPDATE customers SET total_spending = total_spending + ? WHERE full_name=?",
                                  (float(price), cus))

                db.cursor.execute("UPDATE bookings SET status='Completed' WHERE id=?", (b_id,))
                db.cursor.execute("UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,))

                db.conn.commit()
                messagebox.showinfo("Thành công", "Đã thanh toán và trả phòng thành công!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        return None

    def cancel_booking(self):
        item = self.tree.selection()
        if not item: return
        b_id, _, rm_id, _, _, _, _ = self.tree.item(item, "values")

        if messagebox.askyesno("Hủy đơn", "Sếp chắc chắn muốn hủy đơn đặt phòng này?"):
            db.cursor.execute("UPDATE bookings SET status='Cancelled' WHERE id=?", (b_id,))
            db.cursor.execute("UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,))
            db.conn.commit()
            self.load_data()