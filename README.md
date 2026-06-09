# DreamStay - Resort Management System

Hệ thống quản lý khu nghỉ dưỡng 5 sao DreamStay được xây dựng phục vụ báo cáo Bài tập lớn môn Lập trình Python.

## Thành viên thực hiện
- Trần Đức Dương (Nhưởng trưởng)
- Bùi Thị Thúy Hoa
- Đơn vị: Trường Đại học Hạ Long
- GVHD: ThS. Phạm Nguyên Hồng

## Các công nghệ sử dụng
- Giao diện: CustomTkinter (ctk)
- Cơ sở dữ liệu: SQLite (dreamstay.db)
- Xử lý và phân tích số liệu: Pandas, NumPy
- Vẽ biểu đồ thống kê: Matplotlib
- Xử lý âm thanh (Easter Eggs): Pygame
- API tỷ giá trực tuyến: Requests (REST API)
- Trợ lý ảo AI: Google Gemini API (gemini-3.5-flash)

## Hướng dẫn cài đặt & khởi động

1. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

2. Khởi chạy ứng dụng:
   ```bash
   python main.py
   ```

## Tài khoản dùng thử (Quản lý)
- Tài khoản: admin
- Mật khẩu: admin123

## Các tính năng nâng cao & Easter Eggs

### 1. Tính năng nâng cao nổi bật
- **An toàn luồng DB:** Đóng/mở kết nối SQLite động tránh sập luồng khi chạy đa tác vụ.
- **Mã hóa phần cứng:** Mã hóa file phiên làm việc và API key cục bộ bằng SHA-256 kết hợp mã vật lý MAC của thiết bị.
- **Trợ lý ảo Dreamer:** Đọc bối cảnh thực tế (dịch vụ, trạng thái phòng) và hỗ trợ điều khiển nhạc qua giọng lệnh `{CMD:...}`.
- **Nhập/Xuất CSV chạy ngầm:** Đa luồng xử lý CSV với Pandas không gây đơ treo giao diện.
- **Nhật ký & Phục hồi:** Ghi vết hoạt động quản trị dạng JSON và hỗ trợ Rollback dữ liệu.

### 2. Danh sách nhạc ẩn (Easter Eggs)
- **Nightglow:** Nhấp hoạt ảnh tại trang Giới thiệu (đánh thức 6 bức tranh xung quanh, chừa lại cô gái tóc trắng để mở "Final Lesson").
- **Megalovania:** Nhập mã Konami huyền thoại tại trang Liên hệ.
- **Pushing Rewind:** Nhấp tua lùi bài hát nhiều lần liên tục trên thanh phát nhạc.
- **Sthlm Sunset:** Nhấp nhẹ nhàng vào từng ký tự của chữ "DreamStay" trên thanh tiêu đề logo.
- **I Really Want to Stay at Your House:** Nhập mật danh "cyberpunk" vào ô chuyển trang ở phía cuối trang Phòng nghỉ.
- **Hope Is the Thing With Feathers:** Đứng yên hoàn toàn không tương tác tại Trang chủ trong một khoảng thời gian dài.
- **Kamin:** Nhấp đổi liên tục giữa hai dịch vụ Hồ bơi (Lạnh) và Spa (Nóng) tại trang Tiện ích.
- **Memory Reboot:** Gõ từ khóa "Ký ức" bằng tiếng Anh (Memory) vào thanh tìm kiếm nhanh của trang ẩm thực.
- **A Cyber's World:** Nhấp nhiều lần vào quái vật pixel màu vàng tại một sự kiện số.
