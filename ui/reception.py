import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db


class ReceptionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color=COLOR_BORDER)

        ctk.CTkLabel(self, text="Quầy Lễ Tân (Check-in/out)", font=("Georgia", 24, "bold"),
                     text_color=COLOR_NAVY).pack(pady=15)

        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=10, fill="x", padx=20)

        # Dropdown chọn khách và phòng
        self.combo_customer = ctk.CTkOptionMenu(self.control_frame, values=["Trống"], fg_color=COLOR_WHITE,
                                                text_color=COLOR_TEXT, button_color=COLOR_GOLD,
                                                button_hover_color=COLOR_GOLD_HOVER, dynamic_resizing=False)
        self.combo_customer.grid(row=0, column=0, padx=10, pady=5)

        self.combo_room = ctk.CTkOptionMenu(self.control_frame, values=["Trống"], fg_color=COLOR_WHITE,
                                            text_color=COLOR_TEXT, button_color=COLOR_GOLD,
                                            button_hover_color=COLOR_GOLD_HOVER, dynamic_resizing=False)
        self.combo_room.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkButton(self.control_frame, text="NHẬN PHÒNG", fg_color=COLOR_GOLD, font=("Segoe UI", 12, "bold"),
                      command=self.check_in).grid(row=0, column=2, padx=10)

        ctk.CTkButton(self.control_frame, text="THANH TOÁN", fg_color=COLOR_NAVY, font=("Segoe UI", 12, "bold"),
                      command=self.check_out).grid(row=0, column=3, padx=10)

        # Bảng Treeview
        self.setup_treeview()

    def setup_treeview(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=20, pady=20)
        cols = ("ID", "Khách Hàng", "Số Phòng", "Ngày Nhận", "Giá/Đêm")
        self.tree = ttk.Treeview(f, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        db.cursor.execute("SELECT full_name FROM customers")
        c_list = [r[0] for r in db.cursor.fetchall()]
        self.combo_customer.configure(values=c_list if c_list else ["Trống"])

        db.cursor.execute("SELECT room_id FROM rooms WHERE status='Trống'")
        r_list = [r[0] for r in db.cursor.fetchall()]
        self.combo_room.configure(values=r_list if r_list else ["Trống"])

        for row in self.tree.get_children(): self.tree.delete(row)
        db.cursor.execute("SELECT * FROM bookings")
        for row in db.cursor.fetchall(): self.tree.insert("", "end", values=row)

    def check_in(self):
        cus, rm = self.combo_customer.get(), self.combo_room.get()
        if cus == "Trống" or rm == "Trống": return
        db.cursor.execute("SELECT price FROM rooms WHERE room_id=?", (rm,))
        res = db.cursor.fetchone()
        if res:
            price = res[0]
            date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
            db.cursor.execute(
                "INSERT INTO bookings (customer_name, room_id, checkin_date, price_per_night) VALUES (?,?,?,?)",
                (cus, rm, date_now, price))
            db.cursor.execute("UPDATE rooms SET status='Đã đặt' WHERE room_id=?", (rm,))
            db.conn.commit()
            self.load_data()

    def check_out(self):
        item = self.tree.selection()
        if not item: return
        b_id, cus, rm, date, price = self.tree.item(item, "values")
        db.cursor.execute("DELETE FROM bookings WHERE id=?", (b_id,))
        db.cursor.execute("UPDATE rooms SET status='Trống' WHERE room_id=?", (rm,))
        db.conn.commit()
        messagebox.showinfo("Thành công", f"Đã trả phòng {rm}!")
        self.load_data()