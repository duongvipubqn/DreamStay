import customtkinter as ctk

ctk.set_appearance_mode("dark")

COLOR_CREAM = "#1a1a2e"
COLOR_WHITE = "#252538"
COLOR_NAVY = "#131324"
COLOR_TEXT = "#ffffff"
COLOR_BORDER = "#3d3d5c"
COLOR_GOLD = "#c5a059"
COLOR_GOLD_HOVER = "#b38f4d"

LOCATIONS = [
    "Hạ Long", "Đà Lạt", "Hồ Chí Minh", "Cần Thơ", "Hà Nội", "Huế",
    "Hải Phòng", "Phú Quốc", "Nha Trang", "Quy Nhơn", "Vũng Tàu",
    "Hội An", "Phan Thiết", "Thanh Hóa", "Đà Nẵng"
]

ROOM_TYPES = [
    "Deluxe Hướng Biển", "Suite Cao Cấp", "Villa Gia Đình Cổ Điển",
    "Standard Hướng Vườn", "Presidential Suite"
]

ROOM_STATUSES = ["Trống", "Đã đặt", "Đang dọn", "Bảo trì"]
CAPACITIES = ["1 người", "2 người", "3 người", "+4 người"]
EMPLOYEE_STATUSES = ["Đang làm", "Nghỉ phép", "Đã nghỉ"]

POSITIONS = [
    "Tổng Giám đốc (CEO)", "Giám đốc Vận hành (COO)", "Quản lý Khách sạn",
    "Trưởng phòng Nhân sự", "Lễ tân", "Đầu bếp", "Buồng phòng", "Lao công",
    "Bảo vệ", "Kỹ thuật"
]

USER_LIMITS = {
    1: {"max_days": 7, "max_rooms": 3, "label": "Đồng"},
    2: {"max_days": 14, "max_rooms": 5, "label": "Bạc"},
    3: {"max_days": 30, "max_rooms": 10, "label": "Vàng"}
}