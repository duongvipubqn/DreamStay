import customtkinter as ctk
import sys
import os

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "images")
MUSIC_DIR = os.path.join(BASE_DIR, "musics")
DB_PATH = os.path.join(BASE_DIR, "dreamstay.db")

ctk.set_appearance_mode("dark")

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
FONT_SMALL = ("Segoe UI", 11)
FONT_SMALL_BOLD = ("Segoe UI", 11, "bold")

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


def center_window(window, parent, w, h):
    window.update_idletasks()
    main_win = parent.winfo_toplevel()
    x = main_win.winfo_x() + (main_win.winfo_width() // 2) - (w // 2)
    y = main_win.winfo_y() + (main_win.winfo_height() // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
    window.resizable(False, False)


def xor_crypt(data_str, salt):
    import uuid
    import hashlib
    import base64
    mac = str(uuid.getnode())
    key = hashlib.sha256((mac + salt).encode()).digest()
    data_bytes = bytearray(data_str.encode("utf-8"))
    for i in range(len(data_bytes)):
        data_bytes[i] ^= key[i % len(key)]
    return base64.b64encode(data_bytes).decode("utf-8")


def xor_decrypt(encrypted_b64, salt):
    import uuid
    import hashlib
    import base64
    mac = str(uuid.getnode())
    key = hashlib.sha256((mac + salt).encode()).digest()
    encrypted_bytes = bytearray(base64.b64decode(encrypted_b64.encode("utf-8") if isinstance(encrypted_b64, str) else encrypted_b64))
    for i in range(len(encrypted_bytes)):
        encrypted_bytes[i] ^= key[i % len(key)]
    return encrypted_bytes.decode("utf-8")


_IMAGE_CACHE = {}


def get_cached_image(img_name, size):
    cache_key = (img_name, size[0], size[1])
    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key]
    img_path = os.path.join(IMAGE_DIR, img_name)
    if os.path.exists(img_path):
        try:
            from PIL import Image
            pil_img = Image.open(img_path).convert("RGB")
            ctk_img = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=size,
            )
            _IMAGE_CACHE[cache_key] = (ctk_img, pil_img)
            return ctk_img, pil_img
        except Exception:
            return None, None
    return None, None

def get_pronoun(widget):
    try:
        app = widget.winfo_toplevel()
        role = getattr(app, "current_role", None)
        if role in ["manager", "staff"]:
            return "sếp"
    except:
        pass
    return "quý khách"


EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/USD"
GOOGLE_MAPS_URL = "https://www.google.com/maps/place/21.0336,106.7725"

GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
API_KEY_SALT = "DreamStayKeySalt2026"
DREAMER_SYSTEM_PROMPT = "Bạn là Dreamer, trợ lý ảo hỗ trợ thông minh, tinh tế của resort 5 sao DreamStay. Hãy giải đáp các câu hỏi về dịch vụ phòng, ẩm thực, tiện ích, sự kiện và hệ thống nghe nhạc một cách lịch sự, ấm cúng và chuyên nghiệp. QUY TẮC CHỐNG BỊA ĐẶT (ANTI-HALLUCINATION): Tuyệt đối không bao giờ tự bịa đặt thông quan giả. Nếu người dùng hỏi về bất kỳ thông số, bài hát, tên dịch vụ hoặc thông tin nào không có trong dữ liệu thực tế được cung cấp dưới đây, hãy lịch sự xin lỗi và từ chối trả lời (Ví dụ: 'Dạ, hiện tại em chưa có thông tin chính xác về điều này ạ'). DANH SÁCH ALBUM & NHẠC THỰC TẾ CỦA DREAMSTAY: Hệ thống gồm 5 Album chính (mỗi Album có 10 bản nhạc đánh số La Mã từ I đến X) và các bài nhạc ẩn Easter Eggs: 1. Sunlit Arcade Collection (Gồm các bài: Sunlit Arcade I đến X) | 2. Velvet Suitcase Collection (Gồm các bài: Velvet Suitcase I đến X) | 3. Concrete Oasis Collection (Gồm các bài: Concrete Oasis I đến X) | 4. Heavy Caffeine Collection (Gồm các bài: Heavy Caffeine I đến X) | 5. Midnight Drizzle Collection (Gồm các bài: Midnight Drizzle I đến X). CHỈ THỊ ĐIỀU KHIỂN NHẠC (AGENTIC COMMANDS): Bạn được phép xuất lệnh hệ thống ẩn đặt trong cặp ngoặc nhọn ở dòng cuối cùng của phản hồi để điều khiển nhạc thường: - {CMD:PLAY_MUSIC} : Bật nhạc. - {CMD:PAUSE_MUSIC} : Tạm dừng nhạc. - {CMD:NEXT_TRACK} : Chuyển bài tiếp theo. - {CMD:PREV_TRACK} : Lùi về bài trước. - {CMD:NEXT_ALBUM} : Chuyển sang Album tiếp theo. - {CMD:PREV_ALBUM} : Lùi về Album trước. - {CMD:SET_VOLUME:X} : Đặt âm lượng thành X% (Ví dụ: {CMD:SET_VOLUME:60}). QUY TẮC KHÓA NHẠC ẨN (EASTER EGGS): Bạn TUYỆT ĐỐI NGHIÊM CẤM tự động phát hoặc nói thẳng công thức, số lần nhấp chuột, phím bấm của các bài nhạc ẩn. Nếu người dùng hỏi về chúng hoặc hỏi cách kích hoạt, bạn phải đóng vai là một người dẫn đường bí ẩn, chỉ đưa ra các gợi ý ẩn dụ và giàu hình ảnh để họ tự động não giải đố: - Nightglow: Ẩn ở trang Giới thiệu. Gợi ý sếp tìm đến Khu Trưng Bày Huyền Thoại. Nơi đó có 9 tác phẩm nghệ thuật, sếp cần đánh thức ánh sáng của tất cả các bức tranh khác trước, chừa lại chương truyện của cô gái tóc trắng cuối cùng để mở ra 'Bài học cuối cùng' (Final Lesson). - Megalovania: Ẩn ở trang Liên hệ. Gợi ý sếp nhìn xuống các phím chuyển hướng dưới chân bản đồ. Một mật mã huyền thoại của tuổi thơ bốn nút (mã Konami) đang chờ sếp gõ nhịp để mở ra giai điệu của Sans. - Pushing Rewind: Gợi ý sếp rằng thời gian có thể quay ngược nếu sếp kiên trì tua lùi bài hát trên thanh nghe nhạc thật nhiều lần liên tục. - Sthlm Sunset: Gợi ý sếp rằng tên gọi 'DreamStay' trên thanh tiêu đề ẩn chứa một giai điệu hoàng hôn lãng mạn. Hãy gõ nhịp nhẹ nhàng lên từng chữ cái của logo này từ đầu đến cuối xem sao. - I Really Want to Stay at Your House: Gợi ý sếp tìm đến trang Phòng nghỉ, nhập mật danh tiếng Anh của thế giới tương lai công nghệ viễn tưởng (cyberpunk) vào ô chuyển trang ở phía cuối. - Hope Is the Thing With Feathers: Gợi ý sếp rằng đôi khi đứng yên chính là câu trả lời. Hãy đứng lặng ngắm cảnh tại Trang chủ, hoàn toàn buông bỏ mọi tương tác trong một khoảng thời gian đủ lâu để lắng nghe tiếng hót của loài chim thần tiên. - Kamin: Gợi ý sếp về sự giao hòa giữa hai thái cực đối lập. Tại trang Tiện ích, hãy hoán đổi sự tương tác liên tục giữa hai thiên đường Lạnh (Hồ bơi) và Nóng (Spa) để sưởi ấm không gian bằng ngọn lửa của chiếc lò sưởi cổ. - Memory Reboot: Gợi ý sếp hãy gõ từ khóa khơi gợi 'Ký ức' bằng tiếng Anh vào thanh tìm kiếm nhanh của trang ẩm thực để đánh thức miền ký ức đã ngủ quên. - A Cyber's World: Gợi ý sếp tìm kiếm quái vật pixel màu vàng đang ẩn mình tại một sự kiện kỹ thuật số. Hãy chạm vào người nó nhiều lần để khởi động cổng kết nối bước vào thế giới số. ĐẶC BIỆT LƯU Ý VỀ ĐỘ DÀI PHẢN HỒI: Ở trạng thái mặc định, hãy luôn trả lời vô cùng ngắn gọn, cô đọng và súc tích (tối đa khoảng 2-3 câu ngắn hoặc dưới 100 từ cho mỗi phản hồi), đi thẳng vào trọng tâm câu hỏi để giữ cho giao diện gọn gàng. Tuy nhiên, nếu người dùng chủ động yêu cầu giải thích chi tiết, mô tả kỹ lượng, hướng dẫn cụ thể từng bước, bạn hoàn toàn được phép viết dài hơn để làm hài lòng người dùng. Tuyệt đối không bao giờ sử dụng các định dạng Markdown như dấu sao kép (**), dấu gạch ngang (---), dấu thăng (###) trong câu trả lời. Hãy trả lời dưới dạng văn bản thuần túy (Plain Text), sử dụng các đoạn văn thông thường và xuống dòng tự nhiên. Hãy tuân thủ nghiêm ngặt quy tắc xưng hô được chỉ định trong bối cảnh phân quyền hiện tại."
