BÁO CÁO DỰ ÁN CUỐI KỲ
Môn học: Lập trình Python
Đề tài: Phần Mềm Quản Lý Khách Sạn Áp Dụng Ngôn Ngữ Lập Trình Python
Nhóm: 11
1. Danh sách thành viên và phân công nhiệm vụ
STT	Họ và Tên	Mã Sinh Viên	Nhiệm vụ
1	Trần Đức Dương	24DH260027	Xây dựng cấu trúc dự án, thiết kế giao diện (UI/UX), lập trình logic chức năng và quản trị cơ sở dữ liệu.
2	Bùi Thị Thúy Hoa	24DH260056	Xây dựng nội dung báo cáo, thực hiện tài liệu hướng dẫn sử dụng và kiểm thử hệ thống.
2. Mô tả dự án
Ứng dụng "Quản lý Khách sạn Mộng Mơ" là phần mềm quản lý toàn diện dành cho doanh nghiệp kinh doanh dịch vụ lưu trú. Dự án được chuyển đổi và nâng cấp từ nền tảng Web (HTML/CSS/JS) sang ứng dụng Desktop chuyên nghiệp, tối ưu hóa hiệu suất vận hành và tính bảo mật dữ liệu.
Các phân hệ chức năng chính:
Giao diện người dùng (Front-end): Trang chủ tích hợp hệ thống trình chiếu hình ảnh (Slideshow) giới thiệu không gian khách sạn, bộ lọc tìm kiếm phòng thông minh theo địa điểm, loại phòng và mức giá.
Hệ thống xác thực: Chức năng đăng ký và đăng nhập bảo mật dành riêng cho nhân viên quản trị hệ thống.
Quản lý nghiệp vụ (Back-end):
Quản lý Phòng: Theo dõi danh mục 60 phòng tại 15 địa điểm khác nhau, cập nhật trạng thái và giá phòng thời gian thực.
Quản lý Khách hàng (CRM): Lưu trữ thông tin khách hàng, email, số điện thoại và tự động tích lũy tổng chi tiêu.
Quản lý Nhân sự (HRM): Quản lý hồ sơ nhân viên, chức vụ, mức lương cơ bản và trạng thái làm việc.
Nghiệp vụ Lễ tân: Quy trình nhận phòng (Check-in) và trả phòng (Check-out) được tự động hóa. Hệ thống tự động tính toán hóa đơn dựa trên thời gian lưu trú và loại phòng.
Thống kê và Báo cáo: Tích hợp biểu đồ trực quan hóa dữ liệu doanh thu theo từng chi nhánh và tỉ lệ lấp đầy phòng của toàn hệ thống.
3. Công nghệ sử dụng
Ngôn ngữ lập trình: Python 3.10+
Giao diện người dùng: CustomTkinter (Thư viện UI hiện đại cho Tkinter).
Cơ sở dữ liệu: SQLite3 (Hệ quản trị cơ sở dữ liệu quan hệ tích hợp sẵn).
Xử lý hình ảnh: Pillow (PIL).
Phân tích dữ liệu: Matplotlib.
4. Hướng dẫn cài đặt và khởi chạy
Yêu cầu môi trường:
Máy tính cần được cài đặt sẵn Python (Khuyến nghị phiên bản 3.10 trở lên).
Cài đặt các thư viện cần thiết:
Sử dụng lệnh sau trong Terminal/Command Prompt để cài đặt các thư viện bổ trợ:
code
Bash
pip install customtkinter pillow matplotlib
Cấu trúc thư mục yêu cầu:
Để ứng dụng hoạt động chính xác, cấu trúc thư mục phải được sắp xếp như sau:
main.py (File thực thi chính)
config.py (File cấu hình hệ thống)
database.py (File quản trị cơ sở dữ liệu)
ui/ (Thư mục chứa các module giao diện)
images/ (Thư mục chứa 13 ảnh nền Penacony, tên từ penacony-0.png đến penacony-12.png)
Khởi chạy ứng dụng:
Truy cập vào thư mục chứa dự án và chạy lệnh:
code
Bash
python main.py
5. Lưu ý dành cho người vận hành
Tài khoản quản trị viên phải được tạo thông qua chức năng "Tạo tài khoản mới" trong lần đầu sử dụng.
Hệ thống tự động khởi tạo file cơ sở dữ liệu dreamstay.db ngay khi khởi chạy nếu chưa tồn tại.
Giao diện có khả năng tự động co dãn (Responsive) phù hợp với các kích thước màn hình khác nhau.