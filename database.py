import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("dreamstay.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT,
                password TEXT,
                role TEXT DEFAULT 'staff'
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
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                room_id TEXT,
                checkin_date TEXT,
                price_per_night REAL
            )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                location TEXT
            )""")

        self.conn.commit()

db = Database()