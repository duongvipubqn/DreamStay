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

    def create_tables(self):
        self.cursor.execute("""
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_id TEXT PRIMARY KEY,
                location TEXT,
                room_type TEXT,
                status TEXT DEFAULT 'Trống',
                capacity TEXT,
                price REAL
            )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                full_name TEXT,
                email TEXT,
                phone_number TEXT,
                city TEXT,
                total_spending REAL DEFAULT 0
            )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                full_name TEXT,
                position TEXT,
                location TEXT,
                phone_number TEXT,
                base_salary REAL,
                status TEXT DEFAULT 'Đang làm'
            )""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS bookings
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                customer_name
                                TEXT,
                                room_id
                                TEXT,
                                checkin_date
                                TEXT,
                                checkout_date TEXT,
                                                            total_price REAL,
                                                            status TEXT DEFAULT 'Pending'
                    )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue_history (
                                                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                           date TEXT,
                                                           amount REAL,
                                                           location TEXT
            )""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS user_coupons
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                username
                                TEXT,
                                code
                                TEXT,
                                description
                                TEXT,
                                discount_percent
                                INTEGER
                            )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT,
                items_detail TEXT,
                total_price REAL,
                order_date TEXT,
                status TEXT DEFAULT 'Chờ xử lý'
            )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                item_name TEXT UNIQUE,
                price REAL,
                stock INTEGER DEFAULT 50
            )""")

        self.conn.commit()

    def seed_manager(self):
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        res = self.cursor.fetchone()
        if not res:
            hashed_pw = self.hash_password("admin123", "admin")
            self.cursor.execute(
                """
                INSERT INTO users (full_name, username, email, phone, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    "Tổng Quản Lý",
                    "admin",
                    "admin@dreamstay.com",
                    "0000000000",
                    hashed_pw,
                    "manager",
                ),
            )
            self.conn.commit()
        else:
            old_hash = "2407519bfb85c15e8b417c80526e03f905fb55de21fbfb1cfa69bdf0af07a829"
            if res[5] == old_hash:
                new_hash = self.hash_password("admin123", "admin")
                self.cursor.execute("UPDATE users SET password=? WHERE username='admin'", (new_hash,))
                self.conn.commit()

    def seed_inventory(self):
        self.cursor.execute("SELECT COUNT(*) FROM inventory")
        if self.cursor.fetchone()[0] == 0:
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
            ]
            self.cursor.executemany(
                "INSERT INTO inventory (category, item_name, price, stock) VALUES (?,?,?,?)",
                seed_data,
            )
            self.conn.commit()

    def is_room_available(self, room_id, start_date, end_date):
        self.cursor.execute(
            """
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE room_id = ?
                              AND status != 'Cancelled'
                              AND NOT (checkout_date <= ? OR checkin_date >= ?)
                            """,
            (room_id, start_date, end_date),
        )
        return self.cursor.fetchone()[0] == 0

    def get_room_bookings(self, room_id, include_cancelled=False):
        query = (
            "SELECT checkin_date, checkout_date, status FROM bookings WHERE room_id = ?"
        )
        params = [room_id]
        if not include_cancelled:
            query += " AND status != 'Cancelled'"
        query += " ORDER BY checkin_date"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def is_room_currently_booked(self, room_id, today=None):
        if today is None:
            from datetime import datetime

            today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE room_id = ?
                              AND status != 'Cancelled'
                              AND checkin_date <= ?
                              AND checkout_date > ?
                            """,
            (room_id, today, today),
        )
        return self.cursor.fetchone()[0] > 0

    def get_user_level_info(self, full_name):
        self.cursor.execute(
            "SELECT user_level FROM users WHERE full_name=?", (full_name,)
        )
        res = self.cursor.fetchone()
        level = res[0] if res else 1
        from config import USER_LIMITS

        return level, USER_LIMITS.get(level)

    def count_active_bookings(self, full_name):
        self.cursor.execute(
            """
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE customer_name = ?
                              AND status IN ('Pending', 'Confirmed', 'Stay-in')
                            """,
            (full_name,),
        )
        return self.cursor.fetchone()[0]

    def get_room_stats(self):
        try:
            df = pd.read_sql_query(
                "SELECT price, status, capacity FROM rooms", self.conn
            )
            if df.empty:
                return {
                    "total": 0,
                    "avg_price": 0.0,
                    "max_price": 0.0,
                    "status_counts": {},
                    "capacity_counts": {},
                }
            prices = df["price"].to_numpy()
            avg_price = float(np.mean(prices))
            max_price = float(np.max(prices))
            status_counts = df["status"].value_counts().to_dict()
            capacity_counts = df["capacity"].value_counts().to_dict()
            return {
                "total": len(df),
                "avg_price": avg_price,
                "max_price": max_price,
                "status_counts": status_counts,
                "capacity_counts": capacity_counts,
            }
        except Exception:
            return {
                "total": 0,
                "avg_price": 0.0,
                "max_price": 0.0,
                "status_counts": {},
                "capacity_counts": {},
            }


db = Database()
