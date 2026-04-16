import customtkinter as ctk

# --- CẤU HÌNH GIAO DIỆN MỘNG MƠ (LUXURY STYLE) ---
ctk.set_appearance_mode("light") # Chuyển sang chế độ sáng

# Palette màu chính
COLOR_NAVY = "#2c2c3e"      # Sidebar/Header
COLOR_GOLD = "#b49162"      # Nút bấm, điểm nhấn
COLOR_GOLD_HOVER = "#a38257"
COLOR_CREAM = "#fdfaf6"     # Nền chính
COLOR_WHITE = "#ffffff"     # Nền các bảng/form
COLOR_TEXT = "#3a3a3a"      # Màu chữ chính
COLOR_BORDER = "#e8e8e8"    # Viền nhạt

# Dữ liệu hằng số (Giữ nguyên từ bản HTML)
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
    "Trưởng phòng Nhân sự", "Lễ tân", "Buồng phòng", "Bảo vệ", "Kỹ thuật"
]