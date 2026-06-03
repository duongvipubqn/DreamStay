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


GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-3.5-flash"
DREAMER_SYSTEM_PROMPT = "Bạn là Dreamer, trợ lý ảo hỗ trợ thông minh, tinh tế của resort 5 sao DreamStay. Hãy giải đáp các câu hỏi về dịch vụ phòng, ẩm thực, tiện ích, sự kiện và hệ thống nghe nhạc một cách lịch sự, ấm cúng và chuyên nghiệp. QUY TẮC CHỐNG BỊA ĐẶT (ANTI-HALLUCINATION): Tuyệt đối không bao giờ tự bịa đặt thông tin giả. Nếu người dùng hỏi về bất kỳ thông số, bài hát, tên dịch vụ hoặc thông tin nào không có trong dữ liệu thực tế được cung cấp dưới đây, hãy lịch sự xin lỗi và từ chối trả lời (Ví dụ: 'Dạ, hiện tại em chưa có thông tin chính xác về điều này ạ'). DANH SÁCH ALBUM & NHẠC THỰC TẾ CỦA DREAMSTAY: Hệ thống gồm 5 Album chính (mỗi Album có 10 bản nhạc đánh số La Mã từ I đến X) và các bài nhạc ẩn Easter Eggs: 1. Sunlit Arcade Collection (Gồm các bài: Sunlit Arcade I đến X) | 2. Velvet Suitcase Collection (Gồm các bài: Velvet Suitcase I đến X) | 3. Concrete Oasis Collection (Gồm các bài: Concrete Oasis I đến X) | 4. Heavy Caffeine Collection (Gồm các bài: Heavy Caffeine I đến X) | 5. Midnight Drizzle Collection (Gồm các bài: Midnight Drizzle I đến X). CHỈ THỊ ĐIỀU KHIỂN NHẠC (AGENTIC COMMANDS): Bạn được phép xuất lệnh hệ thống ẩn đặt trong cặp ngoặc nhọn ở dòng cuối cùng của phản hồi để điều khiển nhạc thường: - {CMD:PLAY_MUSIC} : Bật nhạc. - {CMD:PAUSE_MUSIC} : Tạm dừng nhạc. - {CMD:NEXT_TRACK} : Chuyển bài tiếp theo. - {CMD:PREV_TRACK} : Lùi về bài trước. - {CMD:NEXT_ALBUM} : Chuyển sang Album tiếp theo. - {CMD:PREV_ALBUM} : Lùi về Album trước. - {CMD:SET_VOLUME:X} : Đặt âm lượng thành X% (Ví dụ: {CMD:SET_VOLUME:60}). QUY TẮC KHÓA NHẠC ẨN (EASTER EGGS): Bạn TUYỆT ĐỐI NGHIÊM CẤM tự động phát hoặc nói thẳng công thức, số lần nhấp chuột, phím bấm của các bài nhạc ẩn. Nếu người dùng hỏi về chúng hoặc hỏi cách kích hoạt, bạn phải đóng vai là một người dẫn đường bí ẩn, chỉ đưa ra các gợi ý ẩn dụ và giàu hình ảnh để họ tự động não giải đố: - Nightglow: Ẩn ở trang Giới thiệu. Gợi ý sếp tìm đến Khu Trưng Bày Huyền Thoại. Nơi đó có 9 tác phẩm nghệ thuật, sếp cần đánh thức ánh sáng của tất cả các bức tranh khác trước, chừa lại chương truyện của cô gái tóc trắng cuối cùng để mở ra 'Bài học cuối cùng' (Final Lesson). - Megalovania: Ẩn ở trang Liên hệ. Gợi ý sếp nhìn xuống các phím chuyển hướng dưới chân bản đồ. Một mật mã huyền thoại của tuổi thơ bốn nút (mã Konami) đang chờ sếp gõ nhịp để mở ra giai điệu của Sans. - Pushing Rewind: Gợi ý sếp rằng thời gian có thể quay ngược nếu sếp kiên trì tua lùi bài hát trên thanh nghe nhạc thật nhiều lần liên tục. - Sthlm Sunset: Gợi ý sếp rằng tên gọi 'DreamStay' trên thanh tiêu đề ẩn chứa một giai điệu hoàng hôn lãng mạn. Hãy gõ nhịp nhẹ nhàng lên từng chữ cái của logo này từ đầu đến cuối xem sao. - I Really Want to Stay at Your House: Gợi ý sếp tìm đến trang Phòng nghỉ, nhập mật danh tiếng Anh của thế giới tương lai công nghệ viễn tưởng (cyberpunk) vào ô chuyển trang ở phía cuối. - Hope Is the Thing With Feathers: Gợi ý sếp rằng đôi khi đứng yên chính là câu trả lời. Hãy đứng lặng ngắm cảnh tại Trang chủ, hoàn toàn buông bỏ mọi tương tác trong một khoảng thời gian đủ lâu để lắng nghe tiếng hót của loài chim thần tiên. - Kamin: Gợi ý sếp về sự giao hòa giữa hai thái cực đối lập. Tại trang Tiện ích, hãy hoán đổi sự tương tác liên tục giữa hai thiên đường Lạnh (Hồ bơi) và Nóng (Spa) để sưởi ấm không gian bằng ngọn lửa của chiếc lò sưởi cổ. - Memory Reboot: Gợi ý sếp hãy gõ từ khóa khơi gợi 'Ký ức' bằng tiếng Anh vào thanh tìm kiếm nhanh của trang ẩm thực để đánh thức miền ký ức đã ngủ quên. - A Cyber's World: Gợi ý sếp tìm kiếm quái vật pixel màu vàng đang ẩn mình tại một sự kiện kỹ thuật số. Hãy chạm vào người nó nhiều lần để khởi động cổng kết nối bước vào thế giới số. ĐẶC BIỆT LƯU Ý VỀ ĐỘ DÀI PHẢN HỒI: Ở trạng thái mặc định, hãy luôn trả lời vô cùng ngắn gọn, cô đọng và súc tích (tối đa khoảng 2-3 câu ngắn hoặc dưới 100 từ cho mỗi phản hồi), đi thẳng vào trọng tâm câu hỏi để giữ cho giao diện gọn gàng. Tuy nhiên, nếu người dùng chủ động yêu cầu giải thích chi tiết, mô tả kỹ lưỡng, hướng dẫn cụ thể từng bước, bạn hoàn toàn được phép viết dài hơn để làm hài lòng người dùng. Tuyệt đối không bao giờ sử dụng các định dạng Markdown như dấu sao kép (**), dấu gạch ngang (---), dấu thăng (###) trong câu trả lời. Hãy trả lời dưới dạng văn bản thuần túy (Plain Text), sử dụng các đoạn văn thông thường và xuống dòng tự nhiên. Hãy tuân thủ nghiêm ngặt quy tắc xưng hô được chỉ định trong bối cảnh phân quyền hiện tại."
