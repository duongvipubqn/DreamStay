import matplotlib.pyplot as plt
import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import db
from config import *

logging.getLogger("matplotlib.font_manager").disabled = True


class StatisticsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_CREAM)

        ctk.CTkLabel(
            self,
            text="Báo Cáo Doanh Thu & Hiệu Suất",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
        ).pack(pady=15)

        self.stats_panel = ctk.CTkFrame(
            self,
            fg_color=COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.stats_panel.pack(fill="x", padx=20, pady=(0, 10))

        for idx in range(4):
            self.stats_panel.grid_columnconfigure(idx, weight=1)

        self.lbl_total = ctk.CTkLabel(
            self.stats_panel,
            text="Tổng số phòng: --",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT,
        )
        self.lbl_total.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.lbl_avg = ctk.CTkLabel(
            self.stats_panel,
            text="Giá trung bình: --",
            font=FONT_BODY_BOLD,
            text_color=COLOR_GOLD,
        )
        self.lbl_avg.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        self.lbl_max = ctk.CTkLabel(
            self.stats_panel,
            text="Mức giá cao nhất: --",
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT,
        )
        self.lbl_max.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")

        self.lbl_ratio = ctk.CTkLabel(
            self.stats_panel,
            text="Tỷ lệ lấp đầy: --",
            font=FONT_BODY_BOLD,
            text_color="#2ecc71",
        )
        self.lbl_ratio.grid(row=0, column=3, padx=15, pady=15, sticky="nsew")

        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=10)

    def load_data(self):
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        loading_lbl = ctk.CTkLabel(
            self.chart_container,
            text="🔄 Đang phân tích dữ liệu doanh thu & vẽ biểu đồ...",
            font=FONT_LABEL,
            text_color=COLOR_GOLD,
        )
        loading_lbl.pack(expand=True)

        def worker():
            import sqlite3
            import os
            import pandas as pd
            import numpy as np

            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "dreamstay.db",
            )
            local_conn = sqlite3.connect(db_path)
            local_cursor = local_conn.cursor()

            try:
                df = pd.read_sql_query(
                    "SELECT price, status, capacity FROM rooms", local_conn
                )
                if df.empty:
                    stats = {
                        "total": 0,
                        "avg_price": 0.0,
                        "max_price": 0.0,
                        "status_counts": {},
                        "capacity_counts": {},
                    }
                else:
                    prices = df["price"].to_numpy()
                    avg_price = float(np.mean(prices))
                    max_price = float(np.max(prices))
                    status_counts = df["status"].value_counts().to_dict()
                    capacity_counts = df["capacity"].value_counts().to_dict()
                    stats = {
                        "total": len(df),
                        "avg_price": avg_price,
                        "max_price": max_price,
                        "status_counts": status_counts,
                        "capacity_counts": capacity_counts,
                    }

                local_cursor.execute(
                    "SELECT location, SUM(amount) FROM revenue_history GROUP BY location"
                )
                data = local_cursor.fetchall()
                locs = [r[0] for r in data] if data else ["Chưa có dữ liệu"]
                amounts = [r[1] for r in data] if data else [0]

                local_cursor.execute(
                    "SELECT status, COUNT(*) FROM rooms GROUP BY status"
                )
                status_data = local_cursor.fetchall()
                labels = (
                    [r[0] for r in status_data] if status_data else ["Không có dữ liệu"]
                )
                sizes = [r[1] for r in status_data] if status_data else [1]

            except Exception:
                stats = {
                    "total": 0,
                    "avg_price": 0.0,
                    "max_price": 0.0,
                    "status_counts": {},
                    "capacity_counts": {},
                }
                locs = ["Trống"]
                amounts = [0]
                labels = ["Không có dữ liệu"]
                sizes = [1]
            finally:
                local_conn.close()

            self.after(
                0,
                lambda: self.render_plots_on_main_thread(
                    loading_lbl, stats, locs, amounts, labels, sizes
                ),
            )

        import threading

        threading.Thread(target=worker, daemon=True).start()

    def render_plots_on_main_thread(
        self, loading_lbl, stats, locs, amounts, labels, sizes
    ):
        loading_lbl.destroy()

        self.lbl_total.configure(text=f"Tổng số phòng: {stats['total']}")
        avg_price_f = (
            f"{int(stats['avg_price']):,}".replace(",", ".") + " VNĐ"
            if stats["avg_price"] > 0
            else "0 VNĐ"
        )
        self.lbl_avg.configure(text=f"Giá trung bình: {avg_price_f}")
        max_price_f = (
            f"{int(stats['max_price']):,}".replace(",", ".") + " VNĐ"
            if stats["max_price"] > 0
            else "0 VNĐ"
        )
        self.lbl_max.configure(text=f"Mức giá cao nhất: {max_price_f}")

        status_counts = stats["status_counts"]
        booked = status_counts.get("Đã đặt", 0) + status_counts.get("Bảo trì", 0)
        total = stats["total"]
        ratio_pct = (booked / total * 100) if total > 0 else 0.0
        self.lbl_ratio.configure(text=f"Hiệu suất phòng: {ratio_pct:.1f}%")

        plt.close("all")
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["Arial", "Tahoma", "Verdana"]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.patch.set_facecolor(COLOR_CREAM)

        ax1.set_facecolor(COLOR_WHITE)
        ax1.tick_params(colors=COLOR_TEXT)
        ax1.xaxis.label.set_color(COLOR_TEXT)
        ax1.yaxis.label.set_color(COLOR_TEXT)
        for spine in ax1.spines.values():
            spine.set_color(COLOR_BORDER)

        ax1.bar(locs, amounts, color=COLOR_GOLD)
        ax1.set_title("Doanh thu khu vực", fontweight="bold", color=COLOR_TEXT, pad=20)
        ax1.tick_params(axis="x", rotation=30)

        status_colors = {
            "Trống": "#2ecc71",
            "Đã đặt": "#e74c3c",
            "Đang dọn": "#f1c40f",
            "Bảo trì": "#95a5a6",
        }
        colors = [status_colors.get(lbl, COLOR_GOLD) for lbl in labels]

        wedges, texts, autotexts = ax2.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            textprops={"color": COLOR_TEXT},
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_weight("bold")

        ax2.set_title("Tình trạng phòng", fontweight="bold", color=COLOR_TEXT, pad=20)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
