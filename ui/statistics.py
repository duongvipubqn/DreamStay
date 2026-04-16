import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import db
from config import *

# Tắt cảnh báo font của Matplotlib để sếp đỡ nhức mắt
import logging

logging.getLogger('matplotlib.font_manager').disabled = True


class StatisticsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)
        ctk.CTkLabel(self, text="Báo Cáo Doanh Thu & Hiệu Suất", font=("Georgia", 24, "bold"),
                     text_color=COLOR_NAVY).pack(pady=15)
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=10)

    def load_data(self):
        for widget in self.chart_container.winfo_children(): widget.destroy()

        # Thiết lập font mặc định an toàn cho Matplotlib
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Tahoma', 'Verdana']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.patch.set_facecolor(COLOR_CREAM)
        ax1.set_facecolor(COLOR_WHITE)

        db.cursor.execute("SELECT location, SUM(amount) FROM revenue_history GROUP BY location")
        data = db.cursor.fetchall()
        locs = [r[0] for r in data] if data else ["Trống"]
        amounts = [r[1] for r in data] if data else [0]
        ax1.bar(locs, amounts, color=COLOR_GOLD)
        ax1.set_title("Doanh thu khu vực", fontweight="bold")
        ax1.tick_params(axis='x', rotation=30)

        db.cursor.execute("SELECT status, COUNT(*) FROM rooms GROUP BY status")
        status_data = db.cursor.fetchall()
        labels = [r[0] for r in status_data] if status_data else ["Trống"]
        sizes = [r[1] for r in status_data] if status_data else [100]
        colors = [COLOR_NAVY, COLOR_GOLD, "#bdc3c7", "#7f8c8d"]
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
        ax2.set_title("Tình trạng phòng", fontweight="bold")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)