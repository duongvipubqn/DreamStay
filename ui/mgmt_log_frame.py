import customtkinter as ctk
from tkinter import ttk
from config import (
    COLOR_WHITE,
    COLOR_NAVY,
    COLOR_TEXT,
    COLOR_BORDER,
    COLOR_GOLD,
    FONT_TITLE,
    FONT_BODY_BOLD,
)
from database import db
from datetime import datetime


class MgmtLogFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header,
            text="Nhật Ký Doanh Thu & Giao Dịch",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
        ).pack(side="left")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pms_frame = ctk.CTkFrame(
            container,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.pms_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        ctk.CTkLabel(
            self.pms_frame,
            text="LỊCH SỬ NHẬN / TRẢ PHÒNG (PMS)",
            font=FONT_BODY_BOLD,
            text_color=COLOR_GOLD,
        ).pack(anchor="w", padx=20, pady=10)

        self.pms_tree = self.create_treeview(
            self.pms_frame,
            (
                "ID Đặt",
                "Khách Hàng",
                "Phòng",
                "Ngày Nhận",
                "Ngày Trả",
                "Tổng Thanh Toán",
            ),
        )

        self.fb_frame = ctk.CTkFrame(
            container,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.fb_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        ctk.CTkLabel(
            self.fb_frame,
            text="LỊCH SỬ ĐƠN HÀNG DỊCH VỤ (F&B)",
            font=FONT_BODY_BOLD,
            text_color=COLOR_GOLD,
        ).pack(anchor="w", padx=20, pady=10)

        self.fb_tree = self.create_treeview(
            self.fb_frame,
            ("ID Đơn", "Phòng", "Chi Tiết Món Ăn", "Thời Gian", "Thành Tiền"),
        )

    def create_treeview(self, parent, columns):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Log.Treeview",
            background=COLOR_NAVY,
            foreground=COLOR_TEXT,
            rowheight=30,
            fieldbackground=COLOR_NAVY,
            borderwidth=0,
        )
        style.map("Log.Treeview", background=[("selected", COLOR_GOLD)])
        style.configure(
            "Log.Treeview.Heading",
            background=COLOR_WHITE,
            foreground=COLOR_GOLD,
            font=FONT_BODY_BOLD,
        )

        t = ttk.Treeview(parent, columns=columns, show="headings", style="Log.Treeview")
        for col in columns:
            t.heading(col, text=col.upper())
            t.column(col, anchor="center", width=120)
        t.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        return t

    def load_data(self):
        for r in self.pms_tree.get_children():
            self.pms_tree.delete(r)
        pms_data = db.execute_query(
            """
            SELECT b.id, c.full_name, b.room_id, b.checkin_date, b.checkout_date, b.total_price 
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            WHERE b.status='Completed' 
            ORDER BY b.id DESC
            """,
            fetch=True,
        )
        for row in pms_data:
            b_id, cus, rm, cin, cout, price = row
            cin_f = datetime.strptime(cin, "%Y-%m-%d").strftime("%d/%m/%Y")
            cout_f = datetime.strptime(cout, "%Y-%m-%d").strftime("%d/%m/%Y")
            price_f = f"{int(price):,}".replace(",", ".") + " VNĐ"
            self.pms_tree.insert(
                "", "end", values=(b_id, cus, rm, cin_f, cout_f, price_f)
            )

        for r in self.fb_tree.get_children():
            self.fb_tree.delete(r)
        fb_data = db.execute_query(
            "SELECT id, room_id, items_detail, order_date, total_price FROM service_orders WHERE status='Completed' ORDER BY id DESC",
            fetch=True,
        )
        for row in fb_data:
            o_id, rm, detail, date, price = row
            date_f = datetime.strptime(date, "%Y-%m-%d %H:%M").strftime(
                "%d/%m/%Y %H:%M"
            )
            price_f = f"{int(price):,}".replace(",", ".") + " VNĐ"
            self.fb_tree.insert("", "end", values=(o_id, rm, detail, date_f, price_f))
