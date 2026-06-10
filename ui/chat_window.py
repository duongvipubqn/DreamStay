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
    FONT_SMALL_BOLD,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DREAMER_SYSTEM_PROMPT,
    API_KEY_SALT,
    GEMINI_API_URL_TEMPLATE,
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
            font=FONT_SMALL_BOLD,
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
            font=FONT_SMALL_BOLD,
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
        rooms_context = self.get_realtime_rooms_context()
        services_context = self.get_realtime_services_context()
        utilities_context = self.get_utilities_context()

        full_system_prompt = f"{DREAMER_SYSTEM_PROMPT}\n[BỐI CẢNH PHÂN QUYỀN AN TOÀN HIỆN TẠI]: {context}\n[BỐI CẢNH NHẠC THỜI GIAN THỰC HIỆN TẠI]: {music_context}\n[BỐI CẢNH CÁC PHÒNG NGHỈ THỜI GIAN THỰC HIỆN TẠI]: {rooms_context}\n[BỐI CẢNH THỰC ĐƠN & KHO HÀNG F&B THỰC TẾ]: {services_context}\n[BỐI CẢNH 9 TIỆN ÍCH CAO CẤP]: {utilities_context}"

        url = GEMINI_API_URL_TEMPLATE.format(model=GEMINI_MODEL, key=self.api_key)
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": self.history,
            "systemInstruction": {"parts": [{"text": full_system_prompt}]},
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                bot_text = data["candidates"][0]["content"]["parts"][0]["text"]
                import re

                cmd_match = re.search(r"\{CMD:([^\}]+)\}", bot_text)
                if cmd_match:
                    cmd_str = cmd_match.group(1)
                    bot_text = re.sub(r"\{CMD:[^\}]+\}", "", bot_text).strip()
                    self.after(0, lambda c=cmd_str: self.execute_ai_command(c))

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

    def get_realtime_rooms_context(self):
        try:
            from database import db

            rooms = db.fetch_all("rooms")
            if not rooms:
                return "Hiện tại resort chưa có phòng nào trong danh sách."
            lines = []
            for r_id, loc, r_type, status, cap, price in rooms:
                price_f = f"{int(price):,}".replace(",", ".")
                lines.append(
                    f"- Phòng {r_id}: {loc} | {r_type} | Trạng thái: {status} | Sức chứa: {cap} | Giá: {price_f} VNĐ/đêm"
                )
            return "DANH SÁCH TOÀN BỘ PHÒNG THỰC TẾ TRONG HỆ THỐNG:\n" + "\n".join(
                lines
            )
        except Exception as e:
            return f"Không thể lấy dữ liệu phòng từ database: {str(e)}"

    def get_realtime_services_context(self):
        try:
            from database import db

            items = db.fetch_all("inventory")
            if not items:
                return "Hiện tại hệ thống thực đơn ẩm thực F&B trống."
            lines = []
            for id_val, cat, name, price, stock in items:
                price_f = f"{int(price):,}".replace(",", ".")
                lines.append(
                    f"- Món: {name} (Nhóm: {cat}) | Giá: {price_f} VNĐ | Tồn kho: {stock} phần"
                )
            return "DANH SÁCH THỰC ĐƠN & KHO HÀNG F&B THỰC TẾ:\n" + "\n".join(lines)
        except Exception as e:
            return f"Không thể lấy dữ liệu dịch vụ F&B từ database: {str(e)}"

    def get_utilities_context(self):
        return (
            "DANH SÁCH 9 TIỆN ÍCH CAO CẤP TẠI RESORT DREAMSTAY:\n"
            "- Hồ Bơi Vô Cực (Ngoài trời | Hoạt động): Tầm nhìn biển vô cực mát lạnh.\n"
            "- Nhà Hàng The Golden (Trong nhà | Hoạt động): Khám phá tinh hoa ẩm thực Á - Âu chuẩn 5 sao.\n"
            "- Mộng Mơ Spa (Trong nhà | Hoạt động): Liệu pháp massage đá nóng và xông hơi thảo dược thư giãn.\n"
            "- Fitness Center (Trong nhà | Hoạt động): Trung tâm thể hình rèn luyện sức khỏe hiện đại.\n"
            "- Sky Bar Tầng Thượng (Ngoài trời | Hoạt động): Cocktails sáng tạo và ngắm hoàng hôn lãng mạn.\n"
            "- Phòng Đại Tiệc (Trong nhà | Hoạt động): Không gian lý tưởng tổ chức hội nghị và sự kiện.\n"
            "- Sảnh Đón Hoàng Gia (Trong nhà | Hoạt động): Đón chào nồng hậu bằng trà hoa và dịch vụ concierge.\n"
            "- Vườn Thượng Uyển (Ngoài trời | Hoạt động): Khu vườn ngập tràn kỳ hoa dị thảo dạo bước tĩnh tâm.\n"
            "- Bãi Biển Riêng Tư (Ngoài trời | Hoạt động): Bờ cát trắng mịn biệt lập riêng tư tuyệt đối."
        )

    def execute_ai_command(self, cmd_str):
        header = getattr(self.app, "header", None)
        if not header:
            return
        try:
            if cmd_str == "PLAY_MUSIC":
                if not getattr(header, "is_playing", False):
                    header.toggle_play()
            elif cmd_str == "PAUSE_MUSIC":
                if getattr(header, "is_playing", False):
                    header.toggle_play()
            elif cmd_str == "NEXT_TRACK":
                header.next_track()
            elif cmd_str == "PREV_TRACK":
                header.prev_track()
            elif cmd_str == "NEXT_ALBUM":
                header.next_album()
            elif cmd_str == "PREV_ALBUM":
                header.prev_album()
            elif cmd_str.startswith("SET_VOLUME:"):
                vol_str = cmd_str.split(":")[1]
                vol_val = int(vol_str)
                header.change_volume(vol_val)
                header.volume_slider.set(vol_val)
        except:
            pass

    def hide_window(self):
        self.withdraw()

    def encrypt_key(self, raw_key):
        from config import xor_crypt
        return xor_crypt(raw_key, API_KEY_SALT)

    def decrypt_key(self, encrypted_b64):
        from config import xor_decrypt
        return xor_decrypt(encrypted_b64, API_KEY_SALT)

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
