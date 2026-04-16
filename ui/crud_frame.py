import customtkinter as ctk
from tkinter import ttk, messagebox
from config import *
from database import db

class CRUDFrame(ctk.CTkFrame):
    def __init__(self, master, title, table_name, columns):
        super().__init__(master, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        self.table_name = table_name
        self.columns = columns
        self.all_data = []
        self.entries = {}

        ctk.CTkLabel(self, text=title, font=("Georgia", 24, "bold"), text_color=COLOR_NAVY).pack(pady=(15, 5))

        # Toolbar tìm kiếm
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.pack(fill="x", padx=20, pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_data)
        ctk.CTkEntry(self.toolbar, placeholder_text="Tìm kiếm nhanh...", width=250, textvariable=self.search_var).pack(side="left")

        # Form nhập liệu
        self.form_frame = ctk.CTkFrame(self, fg_color="#fcfcfc", border_width=1, border_color=COLOR_BORDER)
        self.form_frame.pack(pady=10, fill="x", padx=20)

        for i, col in enumerate(columns):
            row, col_idx = i // 3, i % 3
            ctk.CTkLabel(self.form_frame, text=col, font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT).grid(row=row*2, column=col_idx, padx=10, sticky="w")
            entry = self.create_input(col)
            entry.grid(row=row*2 + 1, column=col_idx, padx=10, pady=(0, 10), sticky="ew")
            self.entries[col] = entry

        # Nút bấm
        self.btn_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_panel.pack(pady=10)
        ctk.CTkButton(self.btn_panel, text="LƯU / CẬP NHẬT", fg_color=COLOR_GOLD, text_color="white", command=self.update).pack(side="left", padx=5)
        ctk.CTkButton(self.btn_panel, text="XÓA", fg_color="#e74c3c", text_color="white", command=self.delete).pack(side="left", padx=5)

        self.tree = self.setup_treeview()

    def create_input(self, col_name):
        if any(x in col_name for x in ["Địa điểm", "Thành phố", "Loại", "Trạng thái", "Sức Chứa", "Chức vụ"]):
            vals = LOCATIONS if "Địa" in col_name or "Thành" in col_name else (ROOM_TYPES if "Loại" in col_name else (ROOM_STATUSES if self.table_name == "rooms" else EMPLOYEE_STATUSES))
            if "Sức Chứa" in col_name: vals = CAPACITIES
            if "Chức vụ" in col_name: vals = POSITIONS
            return ctk.CTkOptionMenu(self.form_frame, values=vals, fg_color=COLOR_WHITE, text_color=COLOR_TEXT, button_color=COLOR_GOLD, dynamic_resizing=False)
        return ctk.CTkEntry(self.form_frame, fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color=COLOR_TEXT)

    def setup_treeview(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=20, pady=10)
        t = ttk.Treeview(f, columns=self.columns, show="headings")
        for col in self.columns:
            t.heading(col, text=col.upper())
            t.column(col, width=100, anchor="center")
        t.pack(fill="both", expand=True)
        t.bind("<ButtonRelease-1>", self.on_select)
        return t

    def filter_data(self, *args):
        search_text = self.search_var.get().lower()
        for row in self.tree.get_children(): self.tree.delete(row)
        for data in self.all_data:
            if any(search_text in str(val).lower() for val in data):
                self.tree.insert("", "end", values=data)

    def load_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        db.cursor.execute(f"SELECT * FROM {self.table_name}")
        self.all_data = db.cursor.fetchall()
        for row in self.all_data: self.tree.insert("", "end", values=row)

    def on_select(self, event):
        item = self.tree.selection()
        if not item: return
        vals = self.tree.item(item, "values")
        for i, col in enumerate(self.columns):
            entry = self.entries[col]
            if isinstance(entry, ctk.CTkOptionMenu): entry.set(vals[i])
            else: entry.delete(0, 'end'); entry.insert(0, vals[i])

    def update(self):
        item = self.tree.selection()
        if not item: return
        old_id = self.tree.item(item, "values")[0]
        vals = [self.entries[col].get() for col in self.columns]
        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
        col_names = [d[0] for d in db.cursor.description]
        set_str = ", ".join([f"{n}=?" for n in col_names])
        db.cursor.execute(f"UPDATE {self.table_name} SET {set_str} WHERE {col_names[0]}=?", (*vals, old_id))
        db.conn.commit(); self.load_data()

    def delete(self):
        item = self.tree.selection()
        if not item: return
        row_id = self.tree.item(item, "values")[0]
        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
        id_col = db.cursor.description[0][0]
        if messagebox.askyesno("Xác nhận", "Xóa dòng này?"):
            db.cursor.execute(f"DELETE FROM {self.table_name} WHERE {id_col}=?", (row_id,))
            db.conn.commit(); self.load_data()