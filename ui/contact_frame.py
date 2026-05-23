import webbrowser
import tkintermapview
from config import *


class ContactFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)

        ctk.CTkLabel(
            self, text="Liên Hệ Với Chúng Tôi", font=FONT_HEADER, text_color=COLOR_TEXT
        ).pack(pady=(36, 14))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_columnconfigure(2, weight=5)

        self.col1 = ctk.CTkFrame(
            body,
            fg_color=COLOR_WHITE,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.col1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.col2 = ctk.CTkFrame(
            body,
            fg_color=COLOR_WHITE,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.col2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.col3 = ctk.CTkFrame(
            body,
            fg_color=COLOR_WHITE,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.col3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            self.col1, text="Gửi Tin Nhắn", font=FONT_TITLE, text_color=COLOR_TEXT
        ).pack(pady=(24, 12))

        self.name_entry = ctk.CTkEntry(
            self.col1, placeholder_text="Họ và tên", height=44
        )
        self.name_entry.pack(pady=10, padx=20, fill="x")

        self.email_entry = ctk.CTkEntry(self.col1, placeholder_text="Email", height=44)
        self.email_entry.pack(pady=10, padx=20, fill="x")

        self.subject_entry = ctk.CTkEntry(
            self.col1, placeholder_text="Chủ đề", height=44
        )
        self.subject_entry.pack(pady=10, padx=20, fill="x")

        self.message_box = ctk.CTkTextbox(
            self.col1, height=180, border_width=1, border_color=COLOR_BORDER
        )
        self.message_box.pack(pady=10, padx=20, fill="both", expand=True)

        self.feedback_label = ctk.CTkLabel(
            self.col1, text="", font=FONT_BODY, text_color=COLOR_TEXT, wraplength=200, justify="center"
        )
        self.feedback_label.pack(pady=(5, 5), fill="x", padx=10)

        ctk.CTkButton(
            self.col1,
            text="GỬI TIN NHẮN",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_LABEL,
            height=44,
            command=self._send_message,
        ).pack(pady=(0, 24), padx=20, fill="x")

        ctk.CTkLabel(
            self.col2, text="Thông Tin Liên Hệ", font=FONT_TITLE, text_color=COLOR_TEXT
        ).pack(pady=(24, 16), padx=20, anchor="w")

        info = [
            ("📍 Địa chỉ", "123 Đại lộ Thượng Lưu, TP. Biển"),
            ("📞 Điện thoại", "(+84) 123 456 789"),
            ("✉️ Email", "info@khachsanmongmo.vn"),
            ("🕒 Giờ mở cửa", "6:00 AM - 9:00 PM"),
        ]

        for head, txt in info:
            frame = ctk.CTkFrame(self.col2, fg_color="transparent")
            frame.pack(fill="x", padx=24, pady=12)

            ctk.CTkLabel(
                frame,
                text=head + ":",
                font=("Segoe UI", 16, "bold"),
                text_color=COLOR_GOLD,
            ).pack(anchor="w")

            ctk.CTkLabel(frame, text=txt, font=FONT_BODY, text_color=COLOR_TEXT).pack(
                anchor="w", pady=(2, 0)
            )

        ctk.CTkLabel(
            self.col3,
            text="Vị Trí Của Chúng Tôi",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
        ).pack(pady=(24, 12))

        self.map_widget = tkintermapview.TkinterMapView(
            self.col3,
            width=600,
            height=450,
            corner_radius=10
        )

        google_maps_btn = ctk.CTkButton(
            self.col3,
            text="Mở Google Maps",
            fg_color=COLOR_GOLD,
            hover_color=COLOR_GOLD_HOVER,
            text_color="white",
            font=FONT_BODY_BOLD,
            height=44,
            command=self._open_google_maps,
        )
        google_maps_btn.pack(side="bottom", pady=(0, 24), padx=20, fill="x")

        self.map_widget.pack(fill="both", expand=True, padx=20, pady=(10, 15))

        self.winfo_toplevel().update_idletasks()

        self.map_widget.set_position(12.2388, 109.1678)
        self.map_widget.set_zoom(15)
        self.map_widget.set_marker(12.2388, 109.1678, text="DreamStay Resort")

    def _send_message(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", "end").strip()

        if not name or not email or not message:
            self.feedback_label.configure(
                text="Vui lòng điền đầy đủ các trường thông tin!",
                text_color="#d64545",
            )
            return

        self.feedback_label.configure(
            text="Tin nhắn đã được gửi thành công! Chúng tôi sẽ liên hệ lại sớm nhất.",
            text_color=COLOR_GOLD,
        )
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.subject_entry.delete(0, "end")
        self.message_box.delete("1.0", "end")

    def _open_google_maps(self):
        url = "https://www.google.com/maps/search/?api=1&query=12.2388,109.1678"
        webbrowser.open(url)

    def load_data(self):
        pass
