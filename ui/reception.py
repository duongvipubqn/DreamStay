from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db


class ReceptionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.tree = None
        self.all_data = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header,
            text="Quản Lý Lễ Tân (FOS)",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
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

        ctk.CTkLabel(
            toolbar, text="🔍 Tìm kiếm:", font=FONT_BODY_BOLD, text_color=COLOR_GOLD
        ).pack(side="left", padx=(20, 5), pady=15)

        ctk.CTkEntry(
            toolbar,
            placeholder_text="Nhập từ khóa cần tìm...",
            width=220,
            textvariable=self.search_var,
            fg_color=COLOR_NAVY,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
        ).pack(side="left", padx=(0, 20), pady=15)

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
        from controller import Controller
        self.all_data = Controller.get_active_bookings()
        self.display_data(self.all_data)

    def display_data(self, data_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data_list:
            b_id, cus, rm, cin, cout, price, status = row
            cin_f = datetime.strptime(cin, "%Y-%m-%d").strftime("%d/%m/%Y")
            cout_f = datetime.strptime(cout, "%Y-%m-%d").strftime("%d/%m/%Y")
            price_f = f"{int(price):,}".replace(",", ".")
            self.tree.insert(
                "", "end", values=(b_id, cus, rm, cin_f, cout_f, price_f, status)
            )

    def filter_data(self, *args):
        if not hasattr(self, "all_data") or not self.all_data:
            return
        search_text = self.search_var.get().lower()
        filtered = []
        for row in self.all_data:
            if any(search_text in str(val).lower() for val in row):
                filtered.append(row)
        self.display_data(filtered)

    def confirm_booking(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn đơn cần xác nhận!")
        b_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[6]

        if status != "Pending":
            return messagebox.showerror("Lỗi", "Đơn này đã được xử lý rồi!")

        pronoun = get_pronoun(self)
        if messagebox.askyesno("Xác nhận", f"{pronoun.capitalize()} đồng ý giữ chỗ cho khách này?"):
            from controller import Controller

            Controller.pms_confirm_booking(b_id)
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
            from controller import Controller

            Controller.pms_check_in(b_id, rm_id)
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

        try:
            from controller import Controller

            success = Controller.pms_check_out(
                b_id, rm_id, cus, price
            )
            if success:
                self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def cancel_booking(self):
        item = self.tree.selection()
        if not item:
            return
        b_id, _, rm_id, _, _, _, _ = self.tree.item(item, "values")
        pronoun = get_pronoun(self)
        if messagebox.askyesno("Hủy đơn", f"{pronoun.capitalize()} chắc chắn muốn hủy đơn này?"):
            from controller import Controller

            Controller.pms_cancel_booking(b_id, rm_id)
            self.load_data()

    def on_hide(self):
        if hasattr(self, "search_var"):
            self.search_var.set("")
