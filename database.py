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

    def hash_password(self, password):
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
                role TEXT DEFAULT 'user'
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

db = Database()