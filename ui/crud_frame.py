import customtkinter as ctk
import csv
from tkinter import filedialog, ttk, messagebox
from config import *
from database import db

class FormModal(ctk.CTkToplevel):
    def __init__(self, parent, title, columns, table_name, callback, initial_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x700")
        self.configure(fg_color=COLOR_CREAM)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.table_name = table_name
        self.callback = callback
        self.columns = columns
        self.entries = {}

        scroll_f = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_f.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            f = ctk.CTkFrame(scroll_f, fg_color="transparent")
            f.pack(fill="x", pady=8, padx=20)

            ctk.CTkLabel(f, text=col, font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT).pack(anchor="w")

            if any(x in col for x in
                   ["Địa điểm", "Thành phố", "Loại", "Trạng thái", "Sức Chứa", "Chức vụ", "Tình Trạng"]):
                vals = LOCATIONS if "Địa" in col or "Thành" in col else (ROOM_TYPES if "Loại" in col else (
                    ROOM_STATUSES if self.table_name == "rooms" else EMPLOYEE_STATUSES))
                if "Sức Chứa" in col: vals = CAPACITIES
                if "Chức vụ" in col: vals = POSITIONS

                entry = ctk.CTkOptionMenu(f, values=vals, fg_color=COLOR_WHITE, text_color=COLOR_TEXT,
                                          button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER,
                                          dropdown_fg_color=COLOR_NAVY, dropdown_text_color=COLOR_TEXT,
                                          dynamic_resizing=False, height=45)
            else:
                entry = ctk.CTkEntry(f, fg_color=COLOR_WHITE, border_color=COLOR_BORDER, text_color=COLOR_TEXT,
                                     height=45)

            entry.pack(fill="x", pady=(5, 0))
            self.entries[col] = entry

        if initial_data:
            for i, col in enumerate(columns):
                entry = self.entries[col]
                if isinstance(entry, ctk.CTkOptionMenu):
                    entry.set(initial_data[i])
                else:
                    entry.insert(0, initial_data[i])

        ctk.CTkButton(scroll_f, text="LƯU THAY ĐỔI", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
                      text_color="white", font=("Segoe UI", 14, "bold"), height=50,
                      command=self.submit).pack(fill="x", pady=30, padx=20)

    def submit(self):
        vals = [self.entries[col].get() for col in self.columns]
        if "" in vals:
            return messagebox.showwarning("Chú ý", "Vui lòng nhập đủ tin!")
        self.callback(vals)
        self.destroy()


class CRUDFrame(ctk.CTkFrame):
    def __init__(self, master, title, table_name, columns):
        super().__init__(master, fg_color="transparent")
        self.table_name = table_name
        self.columns = columns
        self.all_data = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 28, "bold"), text_color=COLOR_TEXT).pack(side="left")

        toolbar = ctk.CTkFrame(self, fg_color=COLOR_WHITE, height=70, corner_radius=15, border_width=1,
                               border_color=COLOR_BORDER)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        search_f = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_f.pack(side="left", padx=15, fill="y")
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_data)
        ctk.CTkEntry(search_f, placeholder_text="Tìm kiếm nhanh...", width=250, textvariable=self.search_var,
                     fg_color=COLOR_NAVY, border_color=COLOR_BORDER, text_color=COLOR_TEXT).pack(pady=15)

        btn_f = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_f.pack(side="right", padx=15)

        ctk.CTkButton(btn_f, text="+ THÊM", fg_color="#27ae60", hover_color="#219150",
                      width=90, height=35, font=("Segoe UI", 11, "bold"),
                      command=self.open_add_modal).pack(side="left", padx=5)

        ctk.CTkButton(btn_f, text="✎ SỬA", fg_color="#3498db", hover_color="#2980b9",
                      width=90, height=35, font=("Segoe UI", 11, "bold"),
                      command=self.open_edit_modal).pack(side="left", padx=5)

        ctk.CTkButton(btn_f, text="🗑 XÓA", fg_color="#e74c3c", hover_color="#c0392b",
                      width=90, height=35, font=("Segoe UI", 11, "bold"),
                      command=self.delete).pack(side="left", padx=5)

        ctk.CTkLabel(btn_f, text="|", text_color=COLOR_BORDER).pack(side="left", padx=10)

        ctk.CTkButton(btn_f, text="NHẬP CSV", fg_color="#8e44ad", hover_color="#732d91",
                      width=100, height=35, font=("Segoe UI", 11, "bold"),
                      command=self.import_csv).pack(side="left", padx=5)

        ctk.CTkButton(btn_f, text="XUẤT CSV", fg_color="#f39c12", hover_color="#d35400",
                      width=100, height=35, font=("Segoe UI", 11, "bold"),
                      command=self.export_csv).pack(side="left", padx=5)

        self.tree = self.setup_treeview()

    def setup_treeview(self):
        f = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
        f.pack(fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=COLOR_NAVY, foreground=COLOR_TEXT, rowheight=35,
                        fieldbackground=COLOR_NAVY, borderwidth=0)
        style.map('Treeview', background=[('selected', COLOR_GOLD)])
        style.configure("Treeview.Heading", background=COLOR_WHITE, foreground=COLOR_GOLD,
                        font=("Segoe UI", 10, "bold"))

        t = ttk.Treeview(f, columns=self.columns, show="headings")
        for col in self.columns:
            t.heading(col, text=col.upper())
            t.column(col, anchor="center", width=120)
        t.pack(fill="both", expand=True, padx=2, pady=2)
        return t

    def open_add_modal(self):
        title = "Thêm phòng mới" if self.table_name == "rooms" else "Thêm mới dữ liệu"
        FormModal(self.winfo_toplevel(), title, self.columns, self.table_name, self.save_to_db)

    def open_edit_modal(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Chú ý", "Hãy chọn dòng cần sửa!")
        vals = self.tree.item(item, "values")
        title = "Cập nhật phòng" if self.table_name == "rooms" else "Cập nhật dữ liệu"
        FormModal(self.winfo_toplevel(), title, self.columns, self.table_name, self.save_to_db, initial_data=vals)

    def save_to_db(self, vals):
        try:
            db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
            col_names = [d[0] for d in db.cursor.description]
            db.cursor.execute(f"SELECT * FROM {self.table_name} WHERE {col_names[0]}=?", (vals[0],))
            if db.cursor.fetchone():
                set_str = ", ".join([f"{n}=?" for n in col_names])
                db.cursor.execute(f"UPDATE {self.table_name} SET {set_str} WHERE {col_names[0]}=?", (*vals, vals[0]))
            else:
                db.cursor.execute(f"INSERT INTO {self.table_name} VALUES ({', '.join(['?'] * len(vals))})", vals)
            db.conn.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

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

    def delete(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Chú ý", "Hãy chọn dòng cần xóa!")
        row_id = self.tree.item(item, "values")[0]
        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
        id_col = db.cursor.description[0][0]
        if messagebox.askyesno("Xác nhận", "Sếp có chắc muốn xóa vĩnh viễn dòng này không?"):
            db.cursor.execute(f"DELETE FROM {self.table_name} WHERE {id_col}=?", (row_id,))
            db.conn.commit()
            self.load_data()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            with open(path, mode="w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.all_data)
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra: {path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            with open(path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                header = next(reader)
                count = 0
                for row in reader:
                    if len(row) == len(self.columns):
                        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
                        id_col = db.cursor.description[0][0]
                        db.cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE {id_col}=?", (row[0],))
                        if not db.cursor.fetchone():
                            db.cursor.execute(f"INSERT INTO {self.table_name} VALUES ({','.join(['?'] * len(row))})",
                                              row)
                            count += 1
                db.conn.commit()
                self.load_data()
                messagebox.showinfo("Thành công", f"Đã nhập thành công {count} dòng dữ liệu mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")