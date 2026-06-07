import sqlite3
import hashlib
import os
import pandas as pd
import numpy as np


class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "dreamstay.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_manager()
        self.seed_inventory()

    @staticmethod
    def hash_password(password, username):
        pepper = "DreamStaySecretPepper2026"
        salt = username + pepper
        salted_pass = password + salt
        return hashlib.sha256(salted_pass.encode()).hexdigest()

    def get_connection(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "dreamstay.db")
        return sqlite3.connect(db_path)

    def execute_query(
        self, query, params=(), fetch=False, fetchone=False, commit=False
    ):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetch:
                return cursor.fetchall()
        finally:
            conn.close()

    def get_column_names(self, table_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            return [d[0] for d in cursor.description]
        finally:
            conn.close()

    def fetch_all(self, table_name):
        return self.execute_query(f"SELECT * FROM {table_name}", fetch=True)

    def record_exists(self, table_name, id_col, id_val):
        res = self.execute_query(
            f"SELECT 1 FROM {table_name} WHERE {id_col}=?", (id_val,), fetchone=True
        )
        return res is not None

    def insert_record(self, table_name, values):
        placeholders = ",".join(["?"] * len(values))
        self.execute_query(
            f"INSERT INTO {table_name} VALUES ({placeholders})", values, commit=True
        )

    def update_record(self, table_name, col_names, values, id_val):
        set_str = ", ".join([f"{name}=?" for name in col_names])
        id_col = col_names[0]
        self.execute_query(
            f"UPDATE {table_name} SET {set_str} WHERE {id_col}=?",
            (*values, id_val),
            commit=True,
        )

    def delete_record(self, table_name, id_col, id_val):
        self.execute_query(
            f"DELETE FROM {table_name} WHERE {id_col}=?", (id_val,), commit=True
        )

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT,
                password TEXT,
                role TEXT DEFAULT 'user',
                user_level INTEGER DEFAULT 1
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_id TEXT PRIMARY KEY,
                location TEXT,
                room_type TEXT,
                status TEXT DEFAULT 'Trống',
                capacity TEXT,
                price REAL
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                full_name TEXT,
                email TEXT,
                phone_number TEXT,
                city TEXT,
                total_spending REAL DEFAULT 0
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                full_name TEXT,
                position TEXT,
                location TEXT,
                phone_number TEXT,
                base_salary REAL,
                status TEXT DEFAULT 'Đang làm'
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                room_id TEXT,
                checkin_date TEXT,
                checkout_date TEXT,
                total_price REAL,
                status TEXT DEFAULT 'Pending'
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                location TEXT
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_coupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                code TEXT,
                description TEXT,
                discount_percent INTEGER
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT,
                items_detail TEXT,
                total_price REAL,
                order_date TEXT,
                status TEXT DEFAULT 'Chờ xử lý'
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                item_name TEXT UNIQUE,
                price REAL,
                stock INTEGER DEFAULT 50
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                action_type TEXT,
                table_name TEXT,
                record_id TEXT,
                old_data TEXT,
                new_data TEXT
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                subject TEXT,
                message TEXT,
                timestamp TEXT
            )""")

        conn.commit()
        conn.close()

    def seed_manager(self):
        res = self.execute_query(
            "SELECT * FROM users WHERE username='admin'", fetchone=True
        )
        hashed_pw = self.hash_password("admin123", "admin")
        if not res:
            self.execute_query(
                "INSERT INTO users (full_name, username, email, phone, password, role) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "Tổng Quản Lý",
                    "admin",
                    "admin@dreamstay.com",
                    "0000000000",
                    hashed_pw,
                    "manager",
                ),
                commit=True,
            )
        else:
            self.execute_query(
                "UPDATE users SET password=?, role='manager' WHERE username='admin'",
                (hashed_pw,),
                commit=True,
            )

    def seed_inventory(self):
        count = self.execute_query("SELECT COUNT(*) FROM inventory", fetchone=True)[0]
        if count == 0:
            seed_data = [
                ("Rượu Vang Đỏ Cao Cấp", "Chateau Margaux 2015", 5500000, 10),
                ("Rượu Vang Đỏ Cao Cấp", "Penfolds Bin 389", 2800000, 15),
                ("Rượu Vang Đỏ Cao Cấp", "Casillero del Diablo", 850000, 30),
                ("Bia Nhập Khẩu", "Heineken Silver", 45000, 100),
                ("Bia Nhập Khẩu", "Tiger Crystal", 40000, 120),
                ("Bia Nhập Khẩu", "Bia Thủ Công IPA", 95000, 50),
                ("Bia Nhập Khẩu", "Corona Extra", 55000, 80),
                ("Nước Ngọt & Soda", "Coca Cola Classic", 25000, 200),
                ("Nước Ngọt & Soda", "Pepsi Black", 25000, 200),
                ("Nước Ngọt & Soda", "7Up Lemon", 25000, 150),
                ("Nước Ngọt & Soda", "Sprite", 25000, 150),
                ("Nước Ngọt & Soda", "Schweppes Soda", 30000, 100),
                ("Champagne Sang Trọng", "Moët & Chandon", 3500000, 8),
                ("Champagne Sang Trọng", "Dom Pérignon", 8200000, 5),
                ("Champagne Sang Trọng", "Veuve Clicquot", 4100000, 12),
                ("Nước Ép Trái Cây", "Nước Ép Cam Tươi", 65000, 50),
                ("Nước Ép Trái Cây", "Nước Ép Dưa Hấu", 60000, 50),
                ("Nước Ép Trái Cây", "Nước Ép Thơm", 60000, 50),
                ("Nước Ép Trái Cây", "Sinh Tố Bơ", 85000, 30),
                ("Nước Khoáng Tinh Khiết", "Lavie 500ml", 15000, 300),
                ("Nước Khoáng Tinh Khiết", "Aquafina 500ml", 15000, 300),
                ("Nước Khoáng Tinh Khiết", "Evian Glass Bottle", 110000, 50),
                ("Nước Khoáng Tinh Khiết", "Perrier Sparkling", 95000, 60),
                ("Cà Phê Đặc Sản", "Cà Phê Phin Truyền Thống", 45000, 100),
                ("Cà Phê Đặc Sản", "Espresso Macchiato", 55000, 80),
                ("Cà Phê Đặc Sản", "Cappuccino Cốt Dừa", 65000, 60),
                ("Trà Hoa Thượng Hạng", "Trà Sen Tây Hồ", 75000, 50),
                ("Trà Hoa Thượng Hạng", "Trà Hoa Cúc Mật Ong", 60000, 70),
                ("Trà Hoa Thượng Hạng", "Trà Đào Cam Sả", 65000, 80),
                ("Bánh Ngọt Pháp", "Bánh Croissant Bơ Tỏi", 45000, 40),
                ("Bánh Ngọt Pháp", "Bánh Mousse Sô-cô-la", 55000, 30),
                ("Bánh Ngọt Pháp", "Bánh Macaron Sắc Màu", 65000, 50),
            ]
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO inventory (category, item_name, price, stock) VALUES (?,?,?,?)",
                seed_data,
            )
            conn.commit()
            conn.close()

    def is_room_available(self, room_id, start_date, end_date):
        res = self.execute_query(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE room_id = ?
              AND status != 'Cancelled'
              AND NOT (checkout_date <= ? OR checkin_date >= ?)
            """,
            (room_id, start_date, end_date),
            fetchone=True,
        )
        return res[0] == 0

    def get_room_bookings(self, room_id, include_cancelled=False):
        query = (
            "SELECT checkin_date, checkout_date, status FROM bookings WHERE room_id = ?"
        )
        params = [room_id]
        if not include_cancelled:
            query += " AND status != 'Cancelled'"
        query += " ORDER BY checkin_date"
        return self.execute_query(query, params, fetch=True)

    def is_room_currently_booked(self, room_id, today=None):
        if today is None:
            from datetime import datetime

            today = datetime.now().strftime("%Y-%m-%d")
        res = self.execute_query(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE room_id = ?
              AND status != 'Cancelled'
              AND checkin_date <= ?
              AND checkout_date > ?
            """,
            (room_id, today, today),
            fetchone=True,
        )
        return res[0] > 0

    def get_user_level_info(self, full_name):
        res = self.execute_query(
            "SELECT user_level FROM users WHERE full_name=?",
            (full_name,),
            fetchone=True,
        )
        level = res[0] if res else 1
        from config import USER_LIMITS

        return level, USER_LIMITS.get(level)

    def count_active_bookings(self, full_name):
        res = self.execute_query(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE customer_name = ?
              AND status IN ('Pending', 'Confirmed', 'Stay-in')
            """,
            (full_name,),
            fetchone=True,
        )
        return res[0]

    def log_action(
        self, username, action_type, table_name, record_id, old_data=None, new_data=None
    ):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute_query(
            "INSERT INTO system_logs (timestamp, username, action_type, table_name, record_id, old_data, new_data) VALUES (?,?,?,?,?,?,?)",
            (
                now,
                username,
                action_type,
                table_name,
                str(record_id),
                old_data,
                new_data,
            ),
            commit=True,
        )


db = Database()
