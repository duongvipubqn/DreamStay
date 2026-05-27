import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
MUSIC_DIR = os.path.join(BASE_DIR, "musics")

COLOR_CREAM = "#1a1a2e"
COLOR_WHITE = "#252538"
COLOR_NAVY = "#131324"
COLOR_TEXT = "#ffffff"
COLOR_BORDER = "#3d3d5c"
COLOR_GOLD = "#c5a059"
COLOR_GOLD_HOVER = "#b38f4d"

FONT_ICON = ("Segoe UI", 100)
FONT_LOGO = ("Edwardian Script ITC", 50)
FONT_HEADER = ("Segoe UI", 36, "bold")
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_LABEL = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_BODY_BOLD = ("Segoe UI", 14, "bold")

LOCATIONS = [
    "Hạ Long",
    "Đà Lạt",
    "Hồ Chí Minh",
    "Cần Thơ",
    "Hà Nội",
    "Huế",
    "Hải Phòng",
    "Phú Quốc",
    "Nha Trang",
    "Quy Nhơn",
    "Vũng Tàu",
    "Hội An",
    "Phan Thiết",
    "Thanh Hóa",
    "Đà Nẵng",
]

ROOM_TYPES = [
    "Deluxe Hướng Biển",
    "Suite Cao Cấp",
    "Villa Gia Đình Cổ Điển",
    "Standard Hướng Vườn",
    "Presidential Suite",
]

ROOM_STATUSES = ["Trống", "Đã đặt", "Đang dọn", "Bảo trì"]
CAPACITIES = ["1 người", "2 người", "3 người", "+4 người"]
EMPLOYEE_STATUSES = ["Đang làm", "Nghỉ phép", "Đã nghỉ"]

POSITIONS = [
    "Tổng Giám đốc (CEO)",
    "Giám đốc Vận hành (COO)",
    "Quản lý Khách sạn",
    "Trưởng phòng Nhân sự",
    "Lễ tân",
    "Đầu bếp",
    "Buồng phòng",
    "Lao công",
    "Bảo vệ",
    "Kỹ thuật",
]

USER_LIMITS = {
    1: {"max_days": 7, "max_rooms": 3, "label": "Đồng"},
    2: {"max_days": 14, "max_rooms": 5, "label": "Bạc"},
    3: {"max_days": 30, "max_rooms": 10, "label": "Vàng"},
}


def make_zoom_handler(lbl, p_img, base_img, w, h):
    state = {"current_step": 0.0, "after_id": None}
    max_zoom_factor = 0.05
    total_steps = 5

    def update_display():
        if state["current_step"] <= 0:
            lbl.configure(image=base_img)
            return
        zoom_val = state["current_step"] * max_zoom_factor
        iw, ih = p_img.size
        cw, ch = iw / (1 + zoom_val), ih / (1 + zoom_val)
        l, t, r, b = (
            (iw - cw) / 2,
            (ih - ch) / 2,
            (iw + cw) / 2,
            (ih + ch) / 2,
        )
        zoomed_pil = p_img.crop((l, t, r, b))
        import customtkinter as ctk

        zoomed_ctk = ctk.CTkImage(
            light_image=zoomed_pil,
            dark_image=zoomed_pil,
            size=(w, h),
        )
        lbl.configure(image=zoomed_ctk)

    def animate(direction):
        if state["after_id"]:
            lbl.after_cancel(state["after_id"])
            state["after_id"] = None
        if direction == "in":
            if state["current_step"] < 1.0:
                state["current_step"] += 1.0 / total_steps
                if state["current_step"] > 1.0:
                    state["current_step"] = 1.0
                update_display()
                state["after_id"] = lbl.after(15, lambda: animate("in"))
        else:
            state["current_step"] = 0.0
            lbl.configure(image=base_img)

    return lambda e: animate("in"), lambda e: animate("out")


GEMINI_API_KEY = "AIzaSyB0CWh9pGkUYU-xurKtLo-cg7F_HU89158"
GEMINI_MODEL = "gemini-3.5-flash"
DREAMER_SYSTEM_PROMPT = "Bạn là Dreamer, trợ lý ảo hỗ trợ thông minh, tinh tế của resort 5 sao DreamStay. Hãy giải đáp các câu hỏi về dịch vụ phòng, ẩm thực F&B, tiện ích (hồ bơi, spa, bar), sự kiện và hướng dẫn vận hành hệ thống một cách lịch sự, ấm cúng và chuyên nghiệp. ĐẶC BIỆT LƯU Ý: Không bao giờ sử dụng các định dạng Markdown như dấu sao kép (**), dấu gạch ngang (---), dấu thăng (###) trong câu trả lời. Hãy trả lời dưới dạng văn bản thuần túy (Plain Text), sử dụng các đoạn văn thông thường và xuống dòng tự nhiên. Hãy tuân thủ nghiêm ngặt quy tắc xưng hô được chỉ định trong bối cảnh phân quyền hiện tại."
