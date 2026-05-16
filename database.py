import sqlite3
import hashlib
import os

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "dreamstay.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_manager()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

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

        self.conn.commit()

    def seed_manager(self):
        self.cursor.execute("SELECT * FROM users WHERE role='manager'")
        if not self.cursor.fetchone():
            hashed_pw = self.hash_password("admin123")
            self.cursor.execute("""
                INSERT INTO users (full_name, username, email, phone, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("Tổng Quản Lý", "admin", "admin@dreamstay.com", "0000000000", hashed_pw, "manager"))
            self.conn.commit()

    def is_room_available(self, room_id, start_date, end_date):
        self.cursor.execute("""
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE room_id = ?
                              AND status != 'Cancelled'
                              AND NOT (checkout_date <= ? OR checkin_date >= ?)
                            """, (room_id, start_date, end_date))
        return self.cursor.fetchone()[0] == 0

    def get_room_bookings(self, room_id, include_cancelled=False):
        query = "SELECT checkin_date, checkout_date, status FROM bookings WHERE room_id = ?"
        params = [room_id]
        if not include_cancelled:
            query += " AND status != 'Cancelled'"
        query += " ORDER BY checkin_date"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def is_room_currently_booked(self, room_id, today=None):
        if today is None:
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("""
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE room_id = ?
                              AND status != 'Cancelled'
                              AND checkin_date <= ?
                              AND checkout_date > ?
                            """, (room_id, today, today))
        return self.cursor.fetchone()[0] > 0

    def get_user_level_info(self, full_name):
        self.cursor.execute("SELECT user_level FROM users WHERE full_name=?", (full_name,))
        res = self.cursor.fetchone()
        level = res[0] if res else 1
        from config import USER_LIMITS
        return level, USER_LIMITS.get(level)

    def count_active_bookings(self, full_name):
        self.cursor.execute("""
                            SELECT COUNT(*)
                            FROM bookings
                            WHERE customer_name = ?
                              AND status IN ('Pending', 'Confirmed', 'Stay-in')
                            """, (full_name,))
        return self.cursor.fetchone()[0]

db = Database()