import customtkinter as ctk
import json
from tkinter import ttk, messagebox
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


class LogFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_data = []

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(
            header,
            text="Nhật Ký & Giám Sát Hệ Thống",
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

        ctk.CTkEntry(
            toolbar,
            placeholder_text="Tìm kiếm nhanh nhật ký...",
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
            text="↩ KHÔI PHỤC THAO TÁC",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=35,
            font=FONT_BODY_BOLD,
            command=self.restore_action,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_f,
            text="🗑 XÓA NHẬT KÝ",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            height=35,
            font=FONT_BODY_BOLD,
            command=self.clear_logs,
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

        self.columns = (
            "ID",
            "Thời Gian",
            "Tài Khoản",
            "Thao Tác",
            "Bảng",
            "ID Bản Ghi",
        )
        self.tree = ttk.Treeview(f, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.all_data = db.execute_query(
            "SELECT id, timestamp, username, action_type, table_name, record_id FROM system_logs ORDER BY id DESC",
            fetch=True,
        )
        for row in self.all_data:
            self.tree.insert("", "end", values=row)

    def filter_data(self, *_args):
        search_text = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for data in self.all_data:
            if any(search_text in str(val).lower() for val in data):
                self.tree.insert("", "end", values=data)

    def restore_action(self):
        items = self.tree.selection()
        if not items:
            return messagebox.showwarning(
                "Chú ý", "Vui lòng chọn dòng nhật ký để khôi phục!"
            )

        log_id = self.tree.item(items[0], "values")[0]
        log_detail = db.execute_query(
            "SELECT action_type, table_name, record_id, old_data, new_data FROM system_logs WHERE id=?",
            (log_id,),
            fetchone=True,
        )
        if not log_detail:
            return

        action_type, table_name, record_id, old_data, new_data = log_detail
        if action_type == "LOGIN":
            return messagebox.showinfo(
                "Thông báo",
                "Thao tác đăng nhập hệ thống không thể và không cần khôi phục dữ liệu!",
            )

        msg = f"Sếp có chắc chắn muốn khôi phục (Rollback) thao tác '{action_type}' này không?"
        if not messagebox.askyesno("Xác nhận", msg):
            return

        try:
            col_names = db.get_column_names(table_name)
            id_col = col_names[0]
            app = self.winfo_toplevel()
            username = getattr(app, "current_username", "system")

            if action_type == "DELETE":
                vals = json.loads(old_data)
                db.insert_record(table_name, vals)
                db.log_action(
                    username, "RESTORE_INSERT", table_name, record_id, None, old_data
                )

            elif action_type in ["UPDATE", "UPDATE_CSV"]:
                vals = json.loads(old_data)
                db.update_record(table_name, col_names, vals, record_id)
                db.log_action(
                    username,
                    "RESTORE_UPDATE",
                    table_name,
                    record_id,
                    new_data,
                    old_data,
                )

            elif action_type in ["INSERT", "INSERT_CSV"]:
                db.delete_record(table_name, id_col, record_id)
                db.log_action(
                    username, "RESTORE_DELETE", table_name, record_id, new_data, None
                )

            else:
                return messagebox.showwarning(
                    "Chú ý", "Không thể khôi phục thao tác khôi phục hệ thống!"
                )

            self.load_data()
            messagebox.showinfo(
                "Thành công",
                f"Đã khôi phục thành công dữ liệu bản ghi ID: {record_id} của bảng {table_name}!",
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khôi phục: {str(e)}")

    def clear_logs(self):
        if messagebox.askyesno(
            "Xác nhận",
            "Sếp có chắc chắn muốn xóa toàn bộ lịch sử nhật ký hệ thống không? (Thao tác này không thể khôi phục!)",
        ):
            try:
                db.execute_query("DELETE FROM system_logs", commit=True)
                self.load_data()
                messagebox.showinfo(
                    "Thành công", "Đã dọn dẹp sạch toàn bộ lịch sử giám sát hệ thống!"
                )
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa nhật ký: {str(e)}")
