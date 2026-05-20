import csv
from tkinter import filedialog, ttk, messagebox
from datetime import datetime
from config import *
from database import db


class FormModal(ctk.CTkToplevel):
    def __init__(self, parent, title, columns, table_name, callback, initial_data=None):
        super().__init__(parent)
        self.title(title)
        w, h = 500, 700
        self.update_idletasks()
        main_win = parent.winfo_toplevel()
        x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
        y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
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

            ctk.CTkLabel(f, text=col, font=FONT_BODY_BOLD, text_color=COLOR_TEXT).pack(
                anchor="w"
            )

            if any(
                x in col
                for x in [
                    "Địa điểm",
                    "Thành phố",
                    "Loại",
                    "Trạng thái",
                    "Sức Chứa",
                    "Chức vụ",
                    "Tình Trạng",
                ]
            ):
                vals = (
                    LOCATIONS
                    if "Địa" in col or "Thành" in col
                    else (
                        ROOM_TYPES
                        if "Loại" in col
                        else (
                            ROOM_STATUSES
                            if self.table_name == "rooms"
                            else EMPLOYEE_STATUSES
                        )
                    )
                )
                if "Sức Chứa" in col:
                    vals = CAPACITIES
                if "Chức vụ" in col:
                    vals = POSITIONS

                entry = ctk.CTkOptionMenu(
                    f,
                    values=vals,
                    fg_color=COLOR_WHITE,
                    text_color=COLOR_TEXT,
                    button_color=COLOR_GOLD,
                    button_hover_color=COLOR_GOLD_HOVER,
                    dropdown_fg_color=COLOR_NAVY,
                    dropdown_text_color=COLOR_TEXT,
                    dynamic_resizing=False,
                    height=45,
                )
            else:
                entry = ctk.CTkEntry(
                    f,
                    fg_color=COLOR_WHITE,
                    border_color=COLOR_BORDER,
                    text_color=COLOR_TEXT,
                    height=45,
                )

            entry.pack(fill="x", pady=(5, 0))
            self.entries[col] = entry

        if initial_data:
            for i, col in enumerate(columns):
                entry = self.entries[col]
                if isinstance(entry, ctk.CTkOptionMenu):
                    entry.set(initial_data[i])
                else:
                    entry.insert(0, initial_data[i])

        ctk.CTkButton(
            scroll_f,
            text="LƯU THAY ĐỔI",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_LABEL,
            height=50,
            command=self.submit,
        ).pack(fill="x", pady=30, padx=20)

    def submit(self):
        vals = [self.entries[col].get().strip() for col in self.columns]
        if any(v == "" for v in vals):
            messagebox.showwarning(
                "Chú ý",
                "Mời sếp nhập đầy đủ thông tin, không được để trống trường nào!",
            )
            return

        if self.table_name == "rooms":
            price_val = vals[5]
            try:
                price_f = float(price_val)
                if price_f <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại mức giá hợp lệ (phải là số dương lớn hơn 0)!",
                )
                return

        elif self.table_name == "employees":
            phone_val = vals[4]
            salary_val = vals[5]
            if not phone_val.isdigit():
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại số điện thoại hợp lệ (chỉ bao gồm các chữ số)!",
                )
                return
            try:
                salary_f = float(salary_val)
                if salary_f <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại mức lương hợp lệ (phải là số dương lớn hơn 0)!",
                )
                return

        elif self.table_name == "customers":
            email_val = vals[2]
            phone_val = vals[3]
            spending_val = vals[5]
            if "@" not in email_val or "." not in email_val:
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại địa chỉ email hợp lệ (phải có định dạng chứa ký tự @ và dấu chấm)!",
                )
                return
            if not phone_val.isdigit():
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại số điện thoại hợp lệ (chỉ chứa chữ số)!",
                )
                return
            try:
                spending_f = float(spending_val)
                if spending_f < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Sai kiểu dữ liệu",
                    "Mời sếp nhập lại tổng chi tiêu hợp lệ (phải là số không âm)!",
                )
                return

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
        ctk.CTkLabel(header, text=title, font=FONT_TITLE, text_color=COLOR_TEXT).pack(
            side="left"
        )

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
            text="+ THÊM",
            fg_color="#27ae60",
            hover_color="#219150",
            width=90,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.open_add_modal,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="✎ SỬA",
            fg_color="#3498db",
            hover_color="#2980b9",
            width=90,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.open_edit_modal,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="🗑 XÓA",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=90,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.delete,
        ).pack(side="left", padx=5)

        ctk.CTkLabel(btn_f, text="|", text_color=COLOR_BORDER).pack(
            side="left", padx=10
        )

        ctk.CTkButton(
            btn_f,
            text="NHẬP CSV",
            fg_color="#8e44ad",
            hover_color="#732d91",
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.import_csv,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="XUẤT CSV",
            fg_color="#f39c12",
            hover_color="#d35400",
            width=100,
            height=35,
            font=FONT_BODY_BOLD,
            command=self.export_csv,
        ).pack(side="left", padx=5)

        self.tree = self.setup_treeview()

    def setup_treeview(self):
        f = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        f.pack(fill="both", expand=True)
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

        t = ttk.Treeview(f, columns=self.columns, show="headings")
        for col in self.columns:
            t.heading(col, text=col.upper())
            t.column(col, anchor="center", width=120)
        t.pack(fill="both", expand=True, padx=2, pady=2)
        return t

    def open_add_modal(self):
        title = "Thêm phòng mới" if self.table_name == "rooms" else "Thêm mới dữ liệu"
        FormModal(
            self.winfo_toplevel(), title, self.columns, self.table_name, self.save_to_db
        )

    def open_edit_modal(self):
        items = self.tree.selection()
        if not items:
            return messagebox.showwarning("Chú ý", "Hãy chọn dòng cần sửa!")
        if len(items) > 1:
            return messagebox.showwarning(
                "Chú ý", "Chỉ được chọn duy nhất một dòng để sửa thông tin!"
            )
        vals = self.tree.item(items[0], "values")
        title = "Cập nhật phòng" if self.table_name == "rooms" else "Cập nhật dữ liệu"
        FormModal(
            self.winfo_toplevel(),
            title,
            self.columns,
            self.table_name,
            self.save_to_db,
            initial_data=vals,
        )
        return None

    def save_to_db(self, vals):
        try:
            db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
            col_names = [d[0] for d in db.cursor.description]
            db.cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE {col_names[0]}=?", (vals[0],)
            )
            if db.cursor.fetchone():
                set_str = ", ".join([f"{n}=?" for n in col_names])
                db.cursor.execute(
                    f"UPDATE {self.table_name} SET {set_str} WHERE {col_names[0]}=?",
                    (*vals, vals[0]),
                )
            else:
                db.cursor.execute(
                    f"INSERT INTO {self.table_name} VALUES ({', '.join(['?'] * len(vals))})",
                    vals,
                )
            db.conn.commit()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def filter_data(self, *_args):
        search_text = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for data in self.all_data:
            if any(search_text in str(val).lower() for val in data):
                self.tree.insert("", "end", values=data)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        db.cursor.execute(f"SELECT * FROM {self.table_name}")
        self.all_data = db.cursor.fetchall()

        for row in self.all_data:
            formatted_row = []
            for i, val in enumerate(row):
                col_name = self.columns[i]
                if any(x in col_name for x in ["Giá", "Tiền", "Lương", "chi tiêu"]):
                    try:
                        formatted_row.append(f"{int(float(val)):,}".replace(",", "."))
                    except:
                        formatted_row.append(val)
                elif (
                    any(x in col_name for x in ["Ngày", "Thời Gian"])
                    and isinstance(val, str)
                    and "-" in val
                ):
                    try:
                        if len(val) == 10:
                            formatted_row.append(
                                datetime.strptime(val, "%Y-%m-%d").strftime("%d/%m/%Y")
                            )
                        elif len(val) > 10:
                            formatted_row.append(
                                datetime.strptime(val, "%Y-%m-%d %H:%M").strftime(
                                    "%d/%m/%Y %H:%M"
                                )
                            )
                        else:
                            formatted_row.append(val)
                    except:
                        formatted_row.append(val)
                else:
                    formatted_row.append(val)
            self.tree.insert("", "end", values=formatted_row)

    def delete(self):
        item = self.tree.selection()
        if not item:
            return messagebox.showwarning("Chú ý", "Hãy chọn dòng cần xóa!")
        row_id = self.tree.item(item[0], "values")[0]
        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
        id_col = db.cursor.description[0][0]
        if messagebox.askyesno(
            "Xác nhận", "Sếp có chắc muốn xóa vĩnh viễn dòng này không?"
        ):
            db.cursor.execute(
                f"DELETE FROM {self.table_name} WHERE {id_col}=?", (row_id,)
            )
            db.conn.commit()
            self.load_data()
        return None

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
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
        if not path:
            return
        try:
            with open(path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader)
                count = 0
                for row in reader:
                    if len(row) == len(self.columns):
                        db.cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 1")
                        id_col = db.cursor.description[0][0]
                        db.cursor.execute(
                            f"SELECT 1 FROM {self.table_name} WHERE {id_col}=?",
                            (row[0],),
                        )
                        if not db.cursor.fetchone():
                            db.cursor.execute(
                                f"INSERT INTO {self.table_name} VALUES ({','.join(['?'] * len(row))})",
                                row,
                            )
                            count += 1
                db.conn.commit()
                self.load_data()
                messagebox.showinfo(
                    "Thành công", f"Đã nhập thành công {count} dòng dữ liệu mới!"
                )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
