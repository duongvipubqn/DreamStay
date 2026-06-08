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
    def pms_cancel_booking(b_id, rm_id):
        db.execute_query(
            "UPDATE bookings SET status='Cancelled' WHERE id=?", (b_id,), commit=True
        )
        db.execute_query(
            "UPDATE rooms SET status='Trống' WHERE room_id=?", (rm_id,), commit=True
        )

    @staticmethod
    def pms_check_out(b_id, rm_id, cus, price, unpaid_orders, order_ids):
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
