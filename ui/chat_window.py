import customtkinter as ctk
import threading
import requests
import json
import os
import uuid
import hashlib
import base64
from tkinter import messagebox
from config import (
    COLOR_CREAM,
    COLOR_WHITE,
    COLOR_NAVY,
    COLOR_TEXT,
    COLOR_BORDER,
    COLOR_GOLD,
    FONT_LABEL,
    FONT_BODY,
    FONT_BODY_BOLD,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DREAMER_SYSTEM_PROMPT,
)


class ChatWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.title("Dreamer - Trợ lý ảo DreamStay")
        w, h = 400, 600
        self.update_idletasks()
        main_win = parent.winfo_toplevel()
        x = main_win.winfo_x() + main_win.winfo_width() - w - 50
        y = main_win.winfo_y() + main_win.winfo_height() - h - 100
        self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        self.configure(fg_color=COLOR_CREAM)
        self.transient(parent)
        self.resizable(False, False)

        self.api_key = GEMINI_API_KEY
        self.history = []

        header_f = ctk.CTkFrame(self, fg_color=COLOR_NAVY, height=60, corner_radius=0)
        header_f.pack(fill="x", side="top")
        header_f.pack_propagate(False)

        ctk.CTkLabel(
            header_f, text="🤖 DREAMER SUPPORT", font=FONT_LABEL, text_color=COLOR_GOLD
        ).pack(side="left", padx=15, pady=15)

        self.key_btn = ctk.CTkButton(
            header_f,
            text="API KEY",
            width=70,
            height=28,
            fg_color=COLOR_WHITE,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 11, "bold"),
            command=self.open_key_settings,
        )
        self.key_btn.pack(side="right", padx=15, pady=15)

        self.clear_btn = ctk.CTkButton(
            header_f,
            text="XÓA CHAT",
            width=70,
            height=28,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="white",
            font=("Segoe UI", 11, "bold"),
            command=self.clear_history,
        )
        self.clear_btn.pack(side="right", padx=0, pady=15)

        self.chat_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_area.pack(fill="both", expand=True, padx=10, pady=10)

        input_f = ctk.CTkFrame(self, fg_color=COLOR_NAVY, height=70, corner_radius=0)
        input_f.pack(fill="x", side="bottom")
        input_f.pack_propagate(False)

        self.entry = ctk.CTkEntry(
            input_f,
            placeholder_text="Nhập tin nhắn...",
            fg_color=COLOR_WHITE,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            height=40,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=15)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(
            input_f,
            text="GỬI",
            fg_color=COLOR_GOLD,
            hover_color="#b38f4d",
            text_color="white",
            font=FONT_BODY_BOLD,
            width=60,
            height=40,
            command=self.send_message,
        )
        self.send_btn.pack(side="right", padx=(0, 15), pady=15)

        self.load_api_key()
        self.load_history()

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def display_message(self, sender, text):
        align = "left" if sender == "bot" else "right"
        bg = COLOR_WHITE if sender == "bot" else COLOR_GOLD
        fg = COLOR_TEXT if sender == "bot" else "white"

        msg_f = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        msg_f.pack(fill="x", pady=5)

        bubble = ctk.CTkFrame(msg_f, fg_color=bg, corner_radius=10)
        bubble.pack(side=align, padx=10)

        lbl = ctk.CTkLabel(
            bubble,
            text=text,
            font=FONT_BODY,
            text_color=fg,
            wraplength=260,
            justify="left",
        )
        lbl.pack(padx=12, pady=8)
        self.scroll_to_bottom()

    def open_key_settings(self):
        dialog = ctk.CTkInputDialog(
            text="Nhập Gemini API Key của sếp:", title="Cấu hình API Key"
        )
        key = dialog.get_input()
        if key is not None:
            cleaned_key = key.strip()
            self.api_key = cleaned_key
            self.save_api_key(cleaned_key)

    def send_message(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.display_message("user", text)
        self.history.append({"role": "user", "parts": [{"text": text}]})
        self.save_history()

        self.send_btn.configure(state="disabled")
        threading.Thread(target=self.call_gemini_api, daemon=True).start()

    def call_gemini_api(self):
        if not self.api_key:
            self.after(
                0,
                lambda: self.display_message(
                    "bot",
                    "Sếp ơi, vui lòng cấu hình API Key ở nút góc trên để em có thể hoạt động hỗ trợ sếp nhé!",
                ),
            )
            self.after(0, lambda: self.send_btn.configure(state="normal"))
            return

        curr_user = getattr(self.app, "current_user", None)
        curr_role = getattr(self.app, "current_role", None)

        if curr_user is None:
            context = "Người dùng hiện tại là Khách vãng lai chưa đăng nhập. Chỉ hỗ trợ tư vấn giới thiệu phòng và các tiện ích công cộng của resort. TUYỆT ĐỐI NGHIÊM CẤM tiết lộ thông số quản trị, danh sách nhân viên hoặc cách xử lý CRUD. QUY TẮC XƯNG HÔ: Bạn phải tự xưng là 'Tôi' hoặc 'Em' và gọi người dùng là 'Quý khách'. Tuyệt đối không được dùng từ 'Sếp'!"
        elif curr_role == "user":
            context = f"Người dùng hiện tại là Khách hàng thành viên tên '{curr_user}'. Hãy hỗ trợ tư vấn đặt phòng, gọi dịch vụ F&B, tham gia sự kiện. TUYỆT ĐỐI NGHIÊM CẤM tiết lộ các tính năng quản trị, PMS, HRM, sửa xóa dữ liệu CRUD, hoặc thông tin quản trị nội bộ hệ thống. QUY TẮC XƯNG HÔ: Bạn phải tự xưng là 'Tôi' hoặc 'Em' và gọi người dùng là 'Quý khách'. Tuyệt đối không được dùng từ 'Sếp'!"
        elif curr_role == "staff":
            context = f"Người dùng hiện tại là Nhân viên resort tên '{curr_user}'. Hãy giải đáp các nghiệp vụ lễ tân (PMS) và quản lý đơn hàng. QUY TẮC XƯNG HÔ: Bạn phải tự xưng là 'Tôi' hoặc 'Em' và gọi người dùng là 'Anh/Chị' lịch sự để hỗ trợ đồng nghiệp."
        else:
            context = f"Người đang trò chuyện là Tổng Quản Lý tên '{curr_user}'. Sếp có đặc quyền quản trị cao nhất. Hãy hỗ trợ sếp tất cả các nghiệp vụ quản trị bao gồm PMS, HRM, quản lý kho hàng, hướng dẫn chi tiết cách sửa đổi dữ liệu CRUD, xuất nhập Excel và phân tích doanh thu. QUY TẮC XƯNG HÔ: Bạn phải tự xưng là 'Em' và gọi người dùng là 'Sếp' để thể hiện lòng kính trọng."

        music_context = self.get_realtime_music_context()

        full_system_prompt = f"{DREAMER_SYSTEM_PROMPT}\n[BỐI CẢNH PHÂN QUYỀN AN TOÀN HIỆN TẠI]: {context}\n[BỐI CẢNH NHẠC THỜI GIAN THỰC HIỆN TẠI]: {music_context}"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": self.history,
            "systemInstruction": {"parts": [{"text": full_system_prompt}]},
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                bot_text = data["candidates"][0]["content"]["parts"][0]["text"]
                import re

                bot_text = re.sub(r"\*\*|###|---", "", bot_text)
                bot_text = re.sub(r"^\s*[\-\*+]\s+", "• ", bot_text, flags=re.MULTILINE)
            else:
                bot_text = "Em đang gặp sự cố kết nối với hệ thống máy chủ Gemini. Sếp vui lòng kiểm tra lại API Key hoặc đường truyền mạng ạ!"
        except Exception as e:
            bot_text = f"Không thể kết nối máy chủ AI: {str(e)}"

        self.after(0, lambda: self.display_message("bot", bot_text))
        self.after(
            0,
            lambda: self.history_append_and_save(bot_text),
        )
        self.after(0, lambda: self.send_btn.configure(state="normal"))

    def load_history(self):
        if os.path.exists("chat_history.json"):
            try:
                with open("chat_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)

                for item in self.history:
                    sender = "bot" if item["role"] == "model" else "user"
                    text = item["parts"][0]["text"]
                    self.display_message(sender, text)
            except:
                self.history = []

        if not self.history:
            self.show_default_greeting()

    def save_history(self):
        try:
            with open("chat_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except:
            pass

    def clear_history(self):
        if messagebox.askyesno(
            "Xác nhận",
            "Sếp có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện không?",
            parent=self,
        ):
            if os.path.exists("chat_history.json"):
                try:
                    os.remove("chat_history.json")
                except:
                    pass
            self.history = []
            for widget in self.chat_area.winfo_children():
                widget.destroy()
            self.show_default_greeting()
            self.scroll_to_top()

    def show_default_greeting(self):
        curr_user = getattr(self.app, "current_user", None)
        curr_role = getattr(self.app, "current_role", None)

        if curr_user is None:
            greeting = "Xin chào quý khách! Tôi là Dreamer, trợ lý ảo của resort DreamStay. Quý khách cần tôi hỗ trợ gì hôm nay ạ?"
        elif curr_role == "user":
            greeting = "Xin chào quý khách! Tôi là Dreamer, trợ lý ảo của resort DreamStay. Quý khách cần tôi hỗ trợ gì hôm nay ạ?"
        elif curr_role == "staff":
            greeting = "Em chào Anh/Chị! Em là Dreamer, trợ lý ảo của resort DreamStay. Anh/Chị cần em hỗ trợ gì hôm nay ạ?"
        else:
            greeting = "Em chào Sếp! Em là Dreamer, trợ lý ảo của resort DreamStay. Sếp cần em hỗ trợ gì hôm nay ạ?"

        self.display_message("bot", greeting)

    def history_append_and_save(self, text):
        self.history.append({"role": "model", "parts": [{"text": text}]})
        self.save_history()

    def scroll_to_bottom(self):
        try:
            self.chat_area.update_idletasks()
            self.chat_area._parent_canvas.yview_moveto(1.0)
            self.after(50, lambda: self.chat_area._parent_canvas.yview_moveto(1.0))
        except:
            pass

    def scroll_to_top(self):
        try:
            self.chat_area.update_idletasks()
            self.chat_area._parent_canvas.yview_moveto(0.0)
            self.after(50, lambda: self.chat_area._parent_canvas.yview_moveto(0.0))
        except:
            pass

    def hide_window(self):
        self.withdraw()

    def encrypt_key(self, raw_key):
        mac = str(uuid.getnode())
        salt = "DreamStayKeySalt2026"
        key = hashlib.sha256((mac + salt).encode()).digest()
        encrypted_bytes = bytearray(raw_key.encode("utf-8"))
        for i in range(len(encrypted_bytes)):
            encrypted_bytes[i] ^= key[i % len(key)]
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt_key(self, encrypted_b64):
        mac = str(uuid.getnode())
        salt = "DreamStayKeySalt2026"
        key = hashlib.sha256((mac + salt).encode()).digest()
        encrypted_bytes = bytearray(base64.b64decode(encrypted_b64.encode("utf-8")))
        for i in range(len(encrypted_bytes)):
            encrypted_bytes[i] ^= key[i % len(key)]
        return encrypted_bytes.decode("utf-8")

    def load_api_key(self):
        if os.path.exists("api_key.enc"):
            try:
                with open("api_key.enc", "r", encoding="utf-8") as f:
                    encrypted_data = f.read().strip()
                self.api_key = self.decrypt_key(encrypted_data)
            except:
                self.api_key = GEMINI_API_KEY
        else:
            self.api_key = GEMINI_API_KEY

    def save_api_key(self, raw_key):
        try:
            encrypted_data = self.encrypt_key(raw_key)
            with open("api_key.enc", "w", encoding="utf-8") as f:
                f.write(encrypted_data)
        except:
            pass

    def get_realtime_music_context(self):
        header = getattr(self.app, "header", None)
        if not header:
            return "Hệ thống máy nghe nhạc của resort đang tắt."

        is_playing = getattr(header, "is_playing", False)
        is_paused = getattr(header, "is_paused", False)
        volume = int(getattr(header, "volume_level", 0.5) * 100)
        play_mode_val = getattr(header, "play_mode", 2)
        is_easter_egg = getattr(header, "is_easter_egg", False)

        try:
            if is_easter_egg:
                raw_title = header.track_label.cget("text")
                track_title = (
                    raw_title.replace("🎵 ", "").replace(" (Paused)", "").strip()
                )
            else:
                cur_album_idx = getattr(header, "cur_album", 0)
                cur_track_idx = getattr(header, "cur_track", 0)
                album = header.music_albums[cur_album_idx]
                track = album["tracks"][cur_track_idx]
                track_title = track["title"]
        except:
            track_title = "Không rõ bản nhạc"

        state_text = (
            "Đang phát nhạc thực tế"
            if is_playing
            else ("Đang tạm dừng phát nhạc" if is_paused else "Đang tắt nhạc")
        )

        if play_mode_val == 1:
            mode_text = "Phát xong tự động dừng (Chế độ Đơn bài)"
        elif play_mode_val == 2:
            mode_text = "Phát liên tục danh sách (Chế độ Album)"
        else:
            mode_text = "Lặp lại bài hiện tại (Chế độ Lặp một bài)"

        return (
            f"BỐI CẢNH NHẠC ĐANG PHÁT THỜI GIAN THỰC:\n"
            f"- Trạng thái: {state_text}\n"
            f"- Bản nhạc đang chọn: {track_title}\n"
            f"- Âm lượng loa hiện tại: {volume}%\n"
            f"- Chế độ phát nhạc: {mode_text}"
        )
