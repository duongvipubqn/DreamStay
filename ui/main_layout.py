import customtkinter as ctk
from config import *
from .reception import ReceptionFrame
from .crud_frame import CRUDFrame
from .statistics import StatisticsFrame


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        self.master = master

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=COLOR_NAVY, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

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

        ctk.CTkLabel(self.sidebar, text="", height=20).pack()

        for name in self.frames.keys():
            btn = ctk.CTkButton(self.sidebar, text=f"  {name}",
                                fg_color="transparent",
                                text_color="#ccc",
                                hover_color="#3a3a50",
                                anchor="w",
                                height=45,
                                font=("Segoe UI", 13, "bold"),
                                command=lambda n=name: self.switch(n))
            btn.pack(pady=2, padx=15, fill="x")

        ctk.CTkButton(self.sidebar, text="  Đăng Xuất",
                      fg_color="transparent", text_color="#e74c3c",
                      anchor="w", height=45, font=("Segoe UI", 13, "bold"),
                      command=self.logout_clicked).pack(side="bottom", pady=20, padx=15, fill="x")

        self.switch("Lễ Tân")

    def logout_clicked(self):
        self.master.master.show_login()

    def switch(self, name):
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        if hasattr(self.frames[name], 'load_data'):
            self.frames[name].load_data()

    def update_user(self, name):
        pass