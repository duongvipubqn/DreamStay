import webbrowser
import tkintermapview
from config import *
from tkinter import messagebox


class ContactFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM, corner_radius=0)
        self.konami_state = 0
        self.ba_state = 0

        ctk.CTkLabel(
            self, text="Liên Hệ Với Chúng Tôi", font=FONT_HEADER, text_color=COLOR_TEXT
        ).pack(pady=(36, 14))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=250, pady=(0, 20))

        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1, uniform="contact_layout")
        body.grid_columnconfigure(1, weight=1, uniform="contact_layout")
        body.grid_columnconfigure(2, weight=2, uniform="contact_layout")

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
            self.col1,
            placeholder_text="Họ và tên",
            height=44,
            fg_color="#181824",
            border_width=0,
            text_color=COLOR_TEXT,
            placeholder_text_color="#888888",
        )
        self.name_entry.pack(pady=10, padx=20, fill="x")

        self.email_entry = ctk.CTkEntry(
            self.col1,
            placeholder_text="Email",
            height=44,
            fg_color="#181824",
            border_width=0,
            text_color=COLOR_TEXT,
            placeholder_text_color="#888888",
        )
        self.email_entry.pack(pady=10, padx=20, fill="x")

        self.subject_entry = ctk.CTkEntry(
            self.col1,
            placeholder_text="Chủ đề",
            height=44,
            fg_color="#181824",
            border_width=0,
            text_color=COLOR_TEXT,
            placeholder_text_color="#888888",
        )
        self.subject_entry.pack(pady=10, padx=20, fill="x")

        self.message_box = ctk.CTkTextbox(
            self.col1,
            height=180,
            fg_color="#181824",
            border_width=0,
            text_color="#888888",
            corner_radius=8,
        )
        self.message_box.pack(pady=10, padx=20, fill="both", expand=True)

        def on_focus_in(event):
            if self.message_box.get("1.0", "end-1c").strip() == "Nội dung tin nhắn":
                self.message_box.delete("1.0", "end")
                self.message_box.configure(text_color=COLOR_TEXT)

        def on_focus_out(event):
            if not self.message_box.get("1.0", "end-1c").strip():
                self.message_box.insert("1.0", "Nội dung tin nhắn")
                self.message_box.configure(text_color="#888888")

        self.message_box.bind("<FocusIn>", on_focus_in)
        self.message_box.bind("<FocusOut>", on_focus_out)
        self.message_box.insert("1.0", "Nội dung tin nhắn")

        self.feedback_label = ctk.CTkLabel(
            self.col1,
            text="",
            font=FONT_BODY,
            text_color=COLOR_TEXT,
            wraplength=200,
            justify="center",
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
        ).pack(pady=(24, 16))

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
            self.col3, width=600, height=450, corner_radius=10
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

        self.map_widget.set_position(21.0336, 106.7725)
        self.map_widget.set_zoom(16)
        self.map_widget.set_marker(21.0336, 106.7725, text="DreamStay Resort")

        self.nav_pad = ctk.CTkFrame(
            self.col3,
            fg_color="#252538",
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.nav_pad.place(relx=0.065, rely=0.85, anchor="sw")
        self.nav_pad.lift()

        ctk.CTkButton(
            self.nav_pad,
            text="▲",
            width=26,
            height=26,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            hover_color="#1a1a2e",
            corner_radius=6,
            command=lambda: self.pan_map("up"),
        ).grid(row=0, column=1, padx=2, pady=2)

        ctk.CTkButton(
            self.nav_pad,
            text="◀",
            width=26,
            height=26,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            hover_color="#1a1a2e",
            corner_radius=6,
            command=lambda: self.pan_map("left"),
        ).grid(row=1, column=0, padx=2, pady=2)

        ctk.CTkButton(
            self.nav_pad,
            text="▶",
            width=26,
            height=26,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            hover_color="#1a1a2e",
            corner_radius=6,
            command=lambda: self.pan_map("right"),
        ).grid(row=1, column=2, padx=2, pady=2)

        ctk.CTkButton(
            self.nav_pad,
            text="▼",
            width=26,
            height=26,
            fg_color="transparent",
            text_color=COLOR_GOLD,
            hover_color="#1a1a2e",
            corner_radius=6,
            command=lambda: self.pan_map("down"),
        ).grid(row=2, column=1, padx=2, pady=2)

    def pan_map(self, direction):
        try:
            lat, lon = self.map_widget.get_position()
            step = 0.005

            if direction == "up":
                lat += step
            elif direction == "down":
                lat -= step
            elif direction == "left":
                lon -= step
            elif direction == "right":
                lon += step

            self.map_widget.set_position(lat, lon)

            sequence = ["up", "up", "down", "down", "left", "right", "left", "right"]
            if direction == sequence[self.konami_state]:
                self.konami_state += 1
                if self.konami_state == 8:
                    self.konami_state = 0
                    self.trigger_konami_easter_egg()
            else:
                if direction == "up":
                    self.konami_state = 1
                else:
                    self.konami_state = 0

        except Exception as e:
            messagebox.showerror("Lỗi bản đồ", f"Không thể điều hướng bản đồ: {str(e)}")

    def trigger_konami_easter_egg(self):
        self.btn_b = ctk.CTkButton(
            self.nav_pad,
            text="B",
            width=26,
            height=26,
            fg_color="#e74c3c",
            text_color="white",
            hover_color="#c0392b",
            corner_radius=13,
            command=self.click_b,
            font=("Segoe UI", 12, "bold"),
        )
        self.btn_b.grid(row=1, column=3, padx=(10, 2), pady=2)

        self.btn_a = ctk.CTkButton(
            self.nav_pad,
            text="A",
            width=26,
            height=26,
            fg_color="#27ae60",
            text_color="white",
            hover_color="#219150",
            corner_radius=13,
            command=self.click_a,
            font=("Segoe UI", 12, "bold"),
        )
        self.btn_a.grid(row=1, column=4, padx=2, pady=2)

    def click_a(self):
        if getattr(self, "ba_state", 0) == 1:
            self.ba_state = 0

            if hasattr(self, "btn_b") and self.btn_b:
                self.btn_b.destroy()
            if hasattr(self, "btn_a") and self.btn_a:
                self.btn_a.destroy()

            app = self.winfo_toplevel()
            header = getattr(app, "header", None)
            if header and hasattr(header, "play_easter_egg"):
                header.play_easter_egg("musics/Megalovania.mp3", "Megalovania")
        else:
            self.ba_state = 0

    def click_b(self):
        self.ba_state = 1

    def _send_message(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_box.get("1.0", "end-1c").strip()

        if message == "Nội dung tin nhắn":
            message = ""

        if not name or not email or not message:
            self.feedback_label.configure(
                text="Vui lòng điền đầy đủ các trường thông tin!",
                text_color="#d64545",
            )
            return

        try:
            from database import db
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.execute_query(
                "INSERT INTO contact_messages (name, email, subject, message, timestamp) VALUES (?,?,?,?,?)",
                (name, email, subject, message, now),
                commit=True,
            )
            self.feedback_label.configure(
                text="Tin nhắn đã được gửi và lưu trữ thành công vào hệ thống!",
                text_color=COLOR_GOLD,
            )
            self.name_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.subject_entry.delete(0, "end")
            self.message_box.delete("1.0", "end")
            self.message_box.insert("1.0", "Nội dung tin nhắn")
            self.message_box.configure(text_color="#888888")
        except Exception as e:
            self.feedback_label.configure(
                text=f"Lỗi kết nối cơ sở dữ liệu: {str(e)}",
                text_color="#d64545",
            )

    def _open_google_maps(self):
        url = "https://www.google.com/maps/place/21.0336,106.7725"
        webbrowser.open(url)

    def load_data(self):
        self.map_widget.set_position(21.0336, 106.7725)
        self.map_widget.set_zoom(16)
