import customtkinter as ctk
from config import *
from .reception import ReceptionFrame
from .crud_frame import CRUDFrame
from .statistics import StatisticsFrame


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        # Đã đổi CYBER_BG thành COLOR_CREAM
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master  # Đây là self.container trong main.py

        # --- SIDEBAR (Màu Navy đậm chuẩn Mộng Mơ) ---
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=COLOR_NAVY, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Logo / Header Sidebar
        self.logo_label = ctk.CTkLabel(self.sidebar, text="KháchSạnMộngMơ",
                                       font=("Georgia", 22, "bold"),
                                       text_color=COLOR_GOLD)
        self.logo_label.pack(pady=(30, 10))

        self.lbl_user = ctk.CTkLabel(self.sidebar, text="Chào mừng trở lại!",
                                     font=("Segoe UI", 12), text_color="white")
        self.lbl_user.pack(pady=(0, 30))

        # Vùng chứa nội dung module quản lý
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Cấu hình các Frame con (Đã port toàn bộ cột từ SQL của sếp)
        self.frames = {
            "Lễ Tân": ReceptionFrame(self.content),
            "Phòng": CRUDFrame(self.content, "Hệ Thống Quản Lý Phòng", "rooms",
                               ["Mã Phòng", "Địa điểm", "Loại Phòng", "Tình Trạng", "Sức Chứa", "Giá (VNĐ)"]),
            "Khách Hàng": CRUDFrame(self.content, "Quản lý Khách hàng (CRM)", "customers",
                                    ["Mã KH", "Họ và Tên", "Email", "Số Điện Thoại", "Thành phố", "Tổng chi tiêu"]),
            "Nhân Viên": CRUDFrame(self.content, "Quản lý Nhân sự (HRM)", "employees",
                                   ["Mã NV", "Họ và Tên", "Chức vụ", "Địa điểm", "Số Điện Thoại", "Lương (VNĐ)",
                                    "Trạng thái"]),
            "Thống Kê": StatisticsFrame(self.content)
        }

        # Tạo nút điều hướng Sidebar
        for name in self.frames.keys():
            btn = ctk.CTkButton(self.sidebar, text=name,
                                fg_color="transparent",
                                text_color="#ccc",
                                hover_color="#3a3a50",
                                anchor="w",
                                height=45,
                                font=("Segoe UI", 13, "bold"),
                                command=lambda n=name: self.switch(n))
            btn.pack(pady=5, padx=20, fill="x")

        # FIX LỖI: Gọi hàm show_login thông qua master.master (tức là quay lại HotelApp)
        self.btn_logout = ctk.CTkButton(self.sidebar, text="THOÁT",
                                        fg_color="#444",
                                        hover_color="#555",
                                        text_color="white",
                                        font=("Segoe UI", 12, "bold"),
                                        command=self.logout_clicked)
        self.btn_logout.pack(side="bottom", pady=30, padx=30, fill="x")

        self.switch("Lễ Tân")

    def logout_clicked(self):
        # Vì MainFrame con của Container, Container con của App chính
        # Ta cần gọi ngược lên App chính
        self.master.master.show_login()

    def switch(self, name):
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        if hasattr(self.frames[name], 'load_data'):
            self.frames[name].load_data()

    def update_user(self, name):
        self.lbl_user.configure(text=f"Sếp: {name.upper()}")