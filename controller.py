import json
import re
from datetime import datetime
from tkinter import messagebox
from database import db


class Controller:
    @staticmethod
    def process_room_booking(app, room_id, checkin_str, checkout_str, total, limits):
        try:
            d_in_dt = datetime.strptime(checkin_str, "%d/%m/%Y")
            d_out_dt = datetime.strptime(checkout_str, "%d/%m/%Y")
            stay_days = (d_out_dt - d_in_dt).days

            curr_username = getattr(app, "current_username", None)
            curr_user = getattr(app, "current_user", None)

            user_info = db.execute_query(
                "SELECT email, phone FROM users WHERE username=?",
                (curr_username,),
                fetchone=True,
            )
            u_email, u_phone = user_info if user_info else ("", "")
            db.ensure_customer_profile(curr_username, curr_user, u_email, u_phone)

            active_bookings = db.count_active_bookings(curr_username)

            if stay_days > limits["max_days"]:
                messagebox.showerror(
                    "Từ chối",
                    f"Tối đa {limits['max_days']} ngày cho hạng {limits['label']}",
                )
                return False

            if active_bookings >= limits["max_rooms"]:
                messagebox.showerror(
                    "Từ chối",
                    f"Hạng {limits['label']} chỉ được đặt tối đa {limits['max_rooms']} phòng!",
                )
                return False

            d_in = d_in_dt.strftime("%Y-%m-%d")
            d_out = d_out_dt.strftime("%Y-%m-%d")

            if not db.is_room_available(room_id, d_in, d_out):
                messagebox.showerror("Hết chỗ", "Khoảng thời gian này đã có người đặt!")
                return False

            db.execute_query(
                """
                INSERT INTO bookings (customer_id, room_id, checkin_date, checkout_date, total_price, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (curr_username, room_id, d_in, d_out, total, "Pending"),
                commit=True,
            )

            active_coupon = getattr(app, "active_coupon", None)
            if active_coupon:
                c_code = active_coupon[0]
                db.execute_query(
                    "DELETE FROM user_coupons WHERE username=? AND code=?",
                    (curr_username, c_code),
                    commit=True,
                )
                app.active_coupon = None

            messagebox.showinfo(
                "Thành công", f"Yêu cầu đặt phòng {room_id} đã được gửi!"
            )
            return True

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đặt phòng: {str(e)}")
            return False

    @staticmethod
    def pms_confirm_booking(b_id):
        db.execute_query(
            "UPDATE bookings SET status='Confirmed' WHERE id=?", (b_id,), commit=True
        )

    @staticmethod
    def pms_check_in(b_id, rm_id):
        db.execute_query(
            "UPDATE bookings SET status='Stay-in' WHERE id=?", (b_id,), commit=True
        )
        db.execute_query(
            "UPDATE rooms SET status='Đã đặt' WHERE room_id=?", (rm_id,), commit=True
        )

    @staticmethod
    def pms_check_out(b_id, rm_id, cus, price):
        unpaid_orders = db.execute_query(
            "SELECT items_detail, total_price, id FROM service_orders WHERE room_id=? AND status NOT IN ('Completed', 'Cancelled')",
            (rm_id,),
            fetch=True,
        )
        order_ids = [o[2] for o in unpaid_orders]

        room_charge = float(re.sub(r"[^\d]", "", price))
        services_charge = 0
        order_details = []

        for items, total_p, o_id in unpaid_orders:
            services_charge += total_p
            order_details.append(f"- {items} ({int(total_p):,} VNĐ)")

        final_bill = room_charge + services_charge

        if services_charge > 0:
            details_msg = "\n".join(order_details)
            msg = (
                f"HÓA ĐƠN THANH TOÁN CHI TIẾT PHÒNG {rm_id}\n\n"
                f"1. Tiền thuê phòng: {int(room_charge):,} VNĐ\n"
                f"2. Tiền dịch vụ ẩm thực (F&B):\n{details_msg}\n"
                f"--------------------------------------------------\n"
                f"TỔNG CỘNG HÓA ĐƠN: {int(final_bill):,} VNĐ\n\n"
                f"Xác nhận thanh toán gộp và làm thủ tục trả phòng cho khách {cus}?"
            )
        else:
            msg = (
                f"Xác nhận thanh toán hóa đơn phòng {rm_id} cho khách {cus}?\n"
                f"Tổng cộng tiền phòng: {int(room_charge):,} VNĐ"
            )

        if messagebox.askyesno("Thanh toán", msg):
            loc_res = db.execute_query(
                "SELECT location FROM rooms WHERE room_id=?", (rm_id,), fetchone=True
            )
            loc = loc_res[0] if loc_res else "Đà Nẵng"

            db.execute_query(
                "INSERT INTO revenue_history (date, amount, location) VALUES (?,?,?)",
                (datetime.now().strftime("%Y-%m-%d"), final_bill, loc),
                commit=True,
            )

            cust_id_res = db.execute_query(
                "SELECT customer_id FROM bookings WHERE id=?", (b_id,), fetchone=True
            )
            cust_id = cust_id_res[0] if cust_id_res else None

            db.execute_query(
                "UPDATE customers SET total_spending = total_spending + ? WHERE customer_id=?",
                (final_bill, cust_id),
                commit=True,
            )
            db.execute_query(
                "UPDATE bookings SET status='Completed' WHERE id=?",
                (b_id,),
                commit=True,
            )
            db.execute_query(
                "UPDATE rooms SET status='Đang dọn' WHERE room_id=?",
                (rm_id,),
                commit=True,
            )

            for o_id in order_ids:
                db.execute_query(
                    "UPDATE service_orders SET status='Completed' WHERE id=?",
                    (o_id,),
                    commit=True,
                )
            messagebox.showinfo(
                "Thành công",
                "Đã thanh toán hóa đơn và hoàn tất Check-out cho khách thành công!",
            )
            return True
        return False

    @staticmethod
    def pms_cancel_booking(b_id, rm_id):
        db.execute_query(
            "UPDATE bookings SET status='Cancelled' WHERE id=?", (b_id,), commit=True
        )
        db.execute_query(
            "UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,), commit=True
        )

    @staticmethod
    def login(username, password):
        hashed_pw = db.hash_password(password, username)
        res = db.execute_query(
            "SELECT username, full_name, role FROM users WHERE username=? AND password=?",
            (username, hashed_pw),
            fetchone=True,
        )
        if not res:
            raise ValueError("Tài khoản hoặc mật khẩu không đúng!")
        return res

    @staticmethod
    def register(name, username, email, phone, password, confirm):
        name = name.strip()
        username = username.strip()
        email = email.strip()
        phone = phone.strip()

        if not name or not username or not email or not phone or not password or not confirm:
            raise ValueError("Vui lòng nhập đầy đủ thông tin!")

        import re
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValueError("Email không đúng định dạng!")

        phone_regex = r"^\d{9,11}$"
        if not re.match(phone_regex, phone):
            raise ValueError("Số điện thoại phải chỉ chứa số và từ 9 đến 11 ký tự!")

        if len(password) < 6:
            raise ValueError("Mật khẩu phải chứa ít nhất 6 ký tự!")

        if password != confirm:
            raise ValueError("Mật khẩu không khớp!")

        import sqlite3
        try:
            hashed_pw = db.hash_password(password, username)
            db.execute_query(
                "INSERT INTO users (full_name, username, email, phone, password, role) VALUES (?,?,?,?,?,?)",
                (name, username, email, phone, hashed_pw, "user"),
                commit=True,
            )
        except sqlite3.Error:
            raise ValueError("Username hoặc Email đã tồn tại!")

    @staticmethod
    def reset_password(username, email, phone, new_pass, confirm):
        username = username.strip()
        email = email.strip()
        phone = phone.strip()

        if not username or not email or not phone or not new_pass or not confirm:
            raise ValueError("Vui lòng nhập đầy đủ thông tin!")

        if len(new_pass) < 6:
            raise ValueError("Mật khẩu mới phải chứa ít nhất 6 ký tự!")

        if new_pass != confirm:
            raise ValueError("Mật khẩu mới không trùng khớp!")

        res = db.execute_query(
            "SELECT email, phone FROM users WHERE username=?", (username,), fetchone=True
        )
        if not res:
            raise ValueError("Tên đăng nhập không tồn tại!")

        db_email, db_phone = res
        if db_email != email or db_phone != phone:
            raise ValueError("Thông tin xác thực (Email hoặc Số điện thoại) không khớp với tài khoản đã đăng ký!")

        hashed_pw = db.hash_password(new_pass, username)
        db.execute_query(
            "UPDATE users SET password=? WHERE username=?", (hashed_pw, username), commit=True
        )

    @staticmethod
    def crud_save_record(table_name, col_names, vals, original_id, username):
        id_col = col_names[0]
        lookup_id = original_id if original_id else vals[0]

        if db.record_exists(table_name, id_col, lookup_id):
            old_record = db.execute_query(
                f"SELECT * FROM {table_name} WHERE {id_col}=?",
                (lookup_id,),
                fetchone=True,
            )
            old_json = (
                json.dumps(old_record, ensure_ascii=False) if old_record else None
            )
            db.update_record(table_name, col_names, vals, lookup_id)
            db.log_action(
                username,
                "UPDATE",
                table_name,
                lookup_id,
                old_json,
                json.dumps(vals, ensure_ascii=False),
            )
        else:
            db.insert_record(table_name, vals)
            db.log_action(
                username,
                "INSERT",
                table_name,
                vals[0],
                None,
                json.dumps(vals, ensure_ascii=False),
            )

    @staticmethod
    def crud_import_row(table_name, col_names, row, username):
        id_col = col_names[0]
        if db.record_exists(table_name, id_col, row[0]):
            old_record = db.execute_query(
                f"SELECT * FROM {table_name} WHERE {id_col}=?",
                (row[0],),
                fetchone=True,
            )
            old_json = (
                json.dumps(old_record, ensure_ascii=False) if old_record else None
            )
            db.update_record(table_name, col_names, row, row[0])
            db.log_action(
                username,
                "UPDATE_CSV",
                table_name,
                row[0],
                old_json,
                json.dumps(row, ensure_ascii=False),
            )
            return "update"
        else:
            db.insert_record(table_name, row)
            db.log_action(
                username,
                "INSERT_CSV",
                table_name,
                row[0],
                None,
                json.dumps(row, ensure_ascii=False),
            )
            return "insert"

    @staticmethod
    def crud_delete_records(table_name, id_col, row_ids, username):
        for rid in row_ids:
            old_record = db.execute_query(
                f"SELECT * FROM {table_name} WHERE {id_col}=?",
                (rid,),
                fetchone=True,
            )
            old_json = (
                json.dumps(old_record, ensure_ascii=False)
                if old_record
                else None
            )
            db.delete_record(table_name, id_col, rid)
            db.log_action(
                username, "DELETE", table_name, rid, old_json, None
            )

    @staticmethod
    def get_statistics_data():
        import sqlite3
        import pandas as pd
        import numpy as np
        from config import DB_PATH

        local_conn = sqlite3.connect(DB_PATH)
        local_cursor = local_conn.cursor()

        try:
            df = pd.read_sql_query(
                "SELECT price, status, capacity FROM rooms", local_conn
            )
            if df.empty:
                stats = {
                    "total": 0,
                    "avg_price": 0.0,
                    "max_price": 0.0,
                    "status_counts": {},
                    "capacity_counts": {},
                }
            else:
                prices = df["price"].to_numpy()
                avg_price = float(np.mean(prices))
                max_price = float(np.max(prices))
                status_counts = df["status"].value_counts().to_dict()
                capacity_counts = df["capacity"].value_counts().to_dict()
                stats = {
                    "total": len(df),
                    "avg_price": avg_price,
                    "max_price": max_price,
                    "status_counts": status_counts,
                    "capacity_counts": capacity_counts,
                }

            from config import LOCATIONS
            local_cursor.execute(
                "SELECT location, SUM(amount) FROM revenue_history GROUP BY location"
            )
            data = local_cursor.fetchall()
            
            revenue_dict = {loc: 0.0 for loc in LOCATIONS}
            if data:
                for loc, amount in data:
                    revenue_dict[loc] = amount
            
            locs = list(revenue_dict.keys())
            amounts = list(revenue_dict.values())

            local_cursor.execute(
                "SELECT status, COUNT(*) FROM rooms GROUP BY status"
            )
            status_data = local_cursor.fetchall()
            labels = (
                [r[0] for r in status_data] if status_data else ["Không có dữ liệu"]
            )
            sizes = [r[1] for r in status_data] if status_data else [1]

            return stats, locs, amounts, labels, sizes
        finally:
            local_conn.close()

    @staticmethod
    def get_active_bookings():
        return db.execute_query(
            """
            SELECT b.id, c.full_name, b.room_id, b.checkin_date, b.checkout_date, b.total_price, b.status 
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            WHERE b.status NOT IN ('Completed', 'Cancelled')
            """,
            fetch=True,
        )

    @staticmethod
    def get_utility_bookings():
        return db.execute_query(
            "SELECT id, customer_id, utility_name, booking_date, status FROM utility_bookings",
            fetch=True,
        )

    @staticmethod
    def pms_confirm_utility(booking_id):
        db.execute_query(
            "UPDATE utility_bookings SET status='Confirmed' WHERE id=?",
            (booking_id,),
            commit=True,
        )

    @staticmethod
    def pms_complete_utility(booking_id):
        db.execute_query(
            "UPDATE utility_bookings SET status='Completed' WHERE id=?",
            (booking_id,),
            commit=True,
        )

    @staticmethod
    def pms_cancel_utility(booking_id):
        db.execute_query(
            "UPDATE utility_bookings SET status='Cancelled' WHERE id=?",
            (booking_id,),
            commit=True,
        )

    @staticmethod
    def pms_delete_utility(booking_id):
        db.execute_query(
            "DELETE FROM utility_bookings WHERE id=?",
            (booking_id,),
            commit=True,
        )

    @staticmethod
    def order_get_pending():
        return db.execute_query(
            "SELECT id, room_id, items_detail, total_price, order_date, status FROM service_orders WHERE status NOT IN ('Completed', 'Cancelled') ORDER BY order_date DESC",
            fetch=True,
        )

    @staticmethod
    def order_confirm(o_id):
        db.execute_query(
            "UPDATE service_orders SET status='Đã xác nhận' WHERE id=?",
            (o_id,),
            commit=True,
        )

    @staticmethod
    def order_deliver(o_id):
        db.execute_query(
            "UPDATE service_orders SET status='Đang giao' WHERE id=?",
            (o_id,),
            commit=True,
        )

    @staticmethod
    def order_pay(o_id, rm_id, total):
        import re
        real_price = float(re.sub(r"[^\d]", "", total))
        loc_res = db.execute_query(
            "SELECT location FROM rooms WHERE room_id=?",
            (rm_id,),
            fetchone=True,
        )
        loc = loc_res[0] if loc_res else "Đà Nẵng"

        db.execute_query(
            "INSERT INTO revenue_history (date, amount, location) VALUES (?,?,?)",
            (datetime.now().strftime("%Y-%m-%d"), real_price, loc),
            commit=True,
        )

        res_cust = db.execute_query(
            "SELECT customer_id FROM bookings WHERE room_id=? AND status='Stay-in'",
            (rm_id,),
            fetchone=True,
        )
        guest_id = res_cust[0] if res_cust else None

        if guest_id:
            db.execute_query(
                "UPDATE customers SET total_spending = total_spending + ? WHERE customer_id=?",
                (real_price, guest_id),
                commit=True,
            )

        db.execute_query(
            "UPDATE service_orders SET status='Completed' WHERE id=?",
            (o_id,),
            commit=True,
        )

    @staticmethod
    def order_cancel(o_id, detail):
        items = detail.split(", ")
        for item_str in items:
            name = item_str.split(" (x")[0]
            qty = int(item_str.split(" (x")[1].replace(")", ""))
            db.execute_query(
                "UPDATE inventory SET stock = stock + ? WHERE item_name = ?",
                (qty, name),
                commit=True,
            )

        db.execute_query(
            "UPDATE service_orders SET status='Cancelled' WHERE id=?",
            (o_id,),
            commit=True,
        )

    @staticmethod
    def log_get_all():
        return db.execute_query(
            "SELECT id, timestamp, username, action_type, table_name, record_id FROM system_logs ORDER BY id DESC",
            fetch=True,
        )

    @staticmethod
    def log_restore(log_id, username):
        log_detail = db.execute_query(
            "SELECT action_type, table_name, record_id, old_data, new_data FROM system_logs WHERE id=?",
            (log_id,),
            fetchone=True,
        )
        if not log_detail:
            raise ValueError("Không tìm thấy dòng nhật ký cần khôi phục!")

        action_type, table_name, record_id, old_data, new_data = log_detail
        col_names = db.get_column_names(table_name)
        id_col = col_names[0]

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
            raise ValueError("Không thể khôi phục thao tác khôi phục hệ thống!")

    @staticmethod
    def log_clear_all():
        db.execute_query("DELETE FROM system_logs", commit=True)

    @staticmethod
    def create_staff_account(name, user, email, phone, pw):
        import sqlite3
        hashed_pw = db.hash_password(pw, user)
        db.execute_query(
            "INSERT INTO users (full_name, username, email, phone, password, role) VALUES (?, ?, ?, ?, ?, ?)",
            (name, user, email, phone, hashed_pw, "staff"),
            commit=True,
        )

    @staticmethod
    def grant_voucher(target, code, desc, percent):
        db.execute_query(
            "INSERT INTO user_coupons (username, code, description, discount_percent) VALUES (?, ?, ?, ?)",
            (target, code.upper(), desc, int(percent)),
            commit=True,
        )

    @staticmethod
    def get_customer_list():
        res_users = db.execute_query(
            "SELECT username FROM users WHERE role='user'", fetch=True
        )
        return [r[0] for r in res_users] if res_users else []

    @staticmethod
    def profile_get_data(username):
        user_res = db.execute_query(
            "SELECT full_name, email, phone, username, role FROM users WHERE username=?",
            (username,),
            fetchone=True,
        )
        bookings_res = db.execute_query(
            "SELECT id, room_id, checkin_date, checkout_date, total_price, status FROM bookings WHERE customer_id=?",
            (username,),
            fetch=True,
        )
        coupons = db.execute_query(
            "SELECT code, description, discount_percent FROM user_coupons WHERE username=?",
            (username,),
            fetch=True,
        )
        return {
            "user_info": user_res,
            "bookings": bookings_res,
            "coupons": coupons
        }

    @staticmethod
    def profile_update(username, current_fullname, new_fullname, new_email, new_phone, new_password):
        db.update_user_profile(
            username,
            current_fullname,
            new_fullname,
            new_email,
            new_phone,
            new_password
        )

    @staticmethod
    def event_register(curr_username, title):
        import re
        import unicodedata
        text_no_d = title.replace("Đ", "D").replace("đ", "d")
        text_normalized = "".join(
            c
            for c in unicodedata.normalize("NFKD", text_no_d)
            if not unicodedata.combining(c)
        )
        words = text_normalized.split()
        initials = "".join([w[0] for w in words if w]).upper()
        clean_initials = re.sub(r"[^\w]", "", initials)
        code = f"EV_{clean_initials}"

        res_exists = db.execute_query(
            "SELECT 1 FROM user_coupons WHERE username=? AND code=?",
            (curr_username, code),
            fetchone=True,
        )
        if res_exists:
            return False, code

        db.execute_query(
            "INSERT INTO user_coupons (username, code, description, discount_percent) VALUES (?,?,?,?)",
            (curr_username, code, f"Voucher qua tang tu su kien: {title}", 15),
            commit=True,
        )
        return True, code

    @staticmethod
    def book_utility(curr_username, name):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db.execute_query(
            "INSERT INTO utility_bookings (customer_id, utility_name, booking_date, status) VALUES (?,?,?,?)",
            (curr_username, name, now, "Pending"),
            commit=True,
        )
        db.log_action(
            curr_username,
            "INSERT",
            "utility_bookings",
            name,
            None,
            f"Đặt dịch vụ: {name}",
        )

    @staticmethod
    def contact_send(name, email, subject, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute_query(
            "INSERT INTO contact_messages (name, email, subject, message, timestamp) VALUES (?,?,?,?,?)",
            (name, email, subject, message, now),
            commit=True,
        )

    @staticmethod
    def mgmt_get_pms_logs():
        return db.execute_query(
            """
            SELECT b.id, c.full_name, b.room_id, b.checkin_date, b.checkout_date, b.total_price 
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            WHERE b.status='Completed' 
            ORDER BY b.id DESC
            """,
            fetch=True,
        )

    @staticmethod
    def mgmt_get_fb_orders():
        return db.execute_query(
            "SELECT id, room_id, items_detail, order_date, total_price FROM service_orders WHERE status='Completed' ORDER BY id DESC",
            fetch=True,
        )


