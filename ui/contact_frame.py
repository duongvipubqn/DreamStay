import urllib.request
import webbrowser
from io import BytesIO
from PIL import Image
from config import *

class ContactFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(
            self,
            text="Liên Hệ Với Chúng Tôi",
            font=FONT_HEADER,
            text_color=COLOR_TEXT
        ).pack(pady=(36, 14))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=60, pady=(0, 20))

        self.left = ctk.CTkFrame(
            body,
            fg_color=COLOR_WHITE,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.left.pack(side="left", fill="both", expand=True, padx=(0, 24), pady=12)

        self.right = ctk.CTkFrame(
            body,
            fg_color=COLOR_WHITE,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.right.pack(side="right", fill="both", expand=True, padx=(24, 0), pady=12)

        ctk.CTkLabel(
            self.left,
            text="Gửi Tin Nhắn",
            font=FONT_TITLE,
            text_color=COLOR_TEXT
        ).pack(pady=(24, 12))

        self.name_entry = ctk.CTkEntry(self.left, placeholder_text="Họ và tên", width=340, height=44)
        self.name_entry.pack(pady=10, padx=20)

        self.email_entry = ctk.CTkEntry(self.left, placeholder_text="Email", width=340, height=44)
        self.email_entry.pack(pady=10, padx=20)

        self.subject_entry = ctk.CTkEntry(self.left, placeholder_text="Chủ đề", width=340, height=44)
        self.subject_entry.pack(pady=10, padx=20)

        self.message_box = ctk.CTkTextbox(
            self.left,
            width=340,
            height=160,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.message_box.pack(pady=10, padx=20)

        self.feedback_label = ctk.CTkLabel(
            self.left,
            text="",
            font=FONT_BODY,
            text_color=COLOR_TEXT
        )
        self.feedback_label.pack(pady=(0, 10))

        ctk.CTkButton(
            self.left,
            text="GỬI TIN NHẮN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_LABEL,
            width=340,
            height=44,
            command=self._send_message
        ).pack(pady=(0, 24))

        ctk.CTkLabel(
            self.right,
            text="Thông Tin Liên Hệ",
            font=FONT_TITLE,
            text_color=COLOR_TEXT
        ).pack(pady=(24, 16), padx=20, anchor="w")

        info = [
            ("📍 Địa chỉ", "123 Đại lộ Thượng Lưu, TP. Biển"),
            ("📞 Điện thoại", "(+84) 123 456 789"),
            ("✉️ Email", "info@khachsanmongmo.vn"),
            ("🕒 Giờ mở cửa", "6:00 AM - 9:00 PM")
        ]

        for head, txt in info:
            frame = ctk.CTkFrame(self.right, fg_color="transparent")
            frame.pack(fill="x", padx=24, pady=8)

            ctk.CTkLabel(
                frame,
                text=head + ":",
                font=("Segoe UI", 15, "bold"),
                text_color=COLOR_GOLD
            ).pack(anchor="w")

            ctk.CTkLabel(
                frame,
                text=txt,
                font=FONT_BODY,
                text_color=COLOR_TEXT
            ).pack(anchor="w")

        map_frame = ctk.CTkFrame(
            self.right,
            fg_color=COLOR_CREAM,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER
        )
        map_frame.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(
            map_frame,
            text="Vị trí của chúng tôi",
            font=FONT_BODY,
            text_color=COLOR_TEXT
        ).pack(pady=(20, 8))

        self.map_label = ctk.CTkLabel(map_frame, text="Đang tải bản đồ...", fg_color=COLOR_BORDER,
                                      corner_radius=10, width=1, height=120)
        self.map_label.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(
            map_frame,
            text="Mở Google Maps",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_BODY_BOLD,
            command=self._open_google_maps
        ).pack(pady=(0, 18), padx=20)

        self._load_map_image()

    def _send_message(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", "end").strip()

        if not name or not email or not message:
            self.feedback_label.configure(
                text="Vui lòng điền đầy đủ họ tên, email và nội dung tin nhắn.",
                text_color="#d64545"
            )
            return

        self.feedback_label.configure(
            text="Tin nhắn đã được gửi thành công! Chúng tôi sẽ liên hệ lại sớm nhất.",
            text_color=COLOR_GOLD
        )
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.subject_entry.delete(0, "end")
        self.message_box.delete("1.0", "end")

    def _open_google_maps(self):
        url = "https://www.google.com/maps/search/?api=1&query=12.2388,109.1678"
        webbrowser.open(url)

    def _load_map_image(self):
        map_url = (
            "https://staticmap.openstreetmap.de/staticmap.php?center=12.2388,109.1678"
            "&zoom=13&size=600x320&markers=12.2388,109.1678,red-pushpin"
        )
        try:
            with urllib.request.urlopen(map_url, timeout=10) as resp:
                data = resp.read()
            image = Image.open(BytesIO(data)).convert("RGB")
            self.map_image = ctk.CTkImage(light_image=image, dark_image=image, size=(640, 320))
            self.map_label.configure(image=self.map_image, text="")
        except Exception:
            image = Image.new("RGB", (640, 320), (28, 34, 59))
            self.map_image = ctk.CTkImage(light_image=image, dark_image=image, size=(640, 320))
            self.map_label.configure(image=self.map_image, text="Bản đồ offline")

    def load_data(self):
        pass