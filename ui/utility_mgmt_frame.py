from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from database import db


class UtilityMgmtFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.tree = None
        self.all_data = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header,
            text="Quản Lý Tiện Ích",
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
            text="HOÀN THÀNH",
            fg_color="#27ae60",
            hover_color="#219150",
            width=110,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.complete_booking,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="HỦY ĐƠN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.cancel_booking,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="🗑 XÓA LỊCH",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.delete_booking,
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
            "Mã Khách",
            "Tên Tiện Ích",
            "Ngày Đặt",
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
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def load_data(self):
        from controller import Controller
        self.all_data = Controller.get_utility_bookings()
        self.display_data(self.all_data)

    def display_data(self, data_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data_list:
            b_id, cus, name, date, status = row
            try:
                date_f = datetime.strptime(date, "%Y-%m-%d %H:%M").strftime("%d/%m/%Y %H:%M")
            except:
                date_f = date
            self.tree.insert(
                "", "end", values=(b_id, cus, name, date_f, status)
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
            return messagebox.showwarning("Chú ý", f"Hãy chọn đơn cần xác nhận!")
        b_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[4]

        if status != "Pending":
            return messagebox.showerror("Lỗi", "Đơn này đã được xử lý rồi!")

        pronoun = get_pronoun(self)
        if messagebox.askyesno("Xác nhận", f"{pronoun.capitalize()} đồng ý phê duyệt lịch đặt tiện ích này?"):
            from controller import Controller
            Controller.pms_confirm_utility(b_id)
            self.load_data()

    def complete_booking(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", f"Hãy chọn đơn cần hoàn thành!")
        b_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[4]

        if status == "Completed":
            return messagebox.showerror("Lỗi", "Lịch này đã hoàn thành rồi!")
        if status == "Pending":
            return messagebox.showerror("Lỗi", "Lịch này chưa được XÁC NHẬN!")
        if status == "Cancelled":
            return messagebox.showerror("Lỗi", "Lịch này đã bị hủy!")

        pronoun = get_pronoun(self)
        if messagebox.askyesno("Xác nhận", f"Xác nhận khách đã sử dụng xong tiện ích này?"):
            from controller import Controller
            Controller.pms_complete_utility(b_id)
            self.load_data()

    def cancel_booking(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", f"Hãy chọn đơn cần hủy!")
        b_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[4]

        if status == "Cancelled":
            return messagebox.showerror("Lỗi", "Lịch này đã hủy rồi!")
        if status == "Completed":
            return messagebox.showerror("Lỗi", "Lịch đã hoàn thành, không thể hủy!")

        pronoun = get_pronoun(self)
        if messagebox.askyesno("Hủy lịch", f"{pronoun.capitalize()} chắc chắn muốn hủy lịch đặt này?"):
            from controller import Controller
            Controller.pms_cancel_utility(b_id)
            self.load_data()

    def delete_booking(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", f"Hãy chọn lịch đặt cần xóa khỏi hệ thống!")
        b_id = self.tree.item(item, "values")[0]

        pronoun = get_pronoun(self)
        if messagebox.askyesno("Xóa lịch đặt", f"{pronoun.capitalize()} chắc chắn muốn xóa vĩnh viễn lịch đặt này khỏi cơ sở dữ liệu?"):
            from controller import Controller
            Controller.pms_delete_utility(b_id)
            self.load_data()

    def on_hide(self):
        if hasattr(self, "search_var"):
            self.search_var.set("")
