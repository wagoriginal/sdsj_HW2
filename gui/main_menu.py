import tkinter as tk
from realtime_ui import show_realtime_window
from forecast_ui import show_forecast_window


def launch_main_menu():
    root = tk.Tk()
    root.title("🌤 WeatherNow - 智能天气助手")
    root.geometry("650x500")
    root.resizable(False, False)

    # ✅ 居中窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (650 // 2)
    y = (screen_height // 2) - (500 // 2)
    root.geometry(f"650x500+{x}+{y}")
    root.configure(bg="#EAF6FF")

    # ✅ 标题区
    title_label = tk.Label(
        root, text="🌤 WeatherNow 智能天气助手",
        font=("Segoe UI", 22, "bold"),
        fg="#0A3D62", bg="#EAF6FF"
    )
    title_label.pack(pady=(40, 10))

    subtitle_label = tk.Label(
        root, text="请选择你要进行的操作：",
        font=("Arial", 13),
        bg="#EAF6FF", fg="#333333"
    )
    subtitle_label.pack(pady=(0, 30))

    # ✅ 按钮区域
    btn_frame = tk.Frame(root, bg="#EAF6FF")
    btn_frame.pack()

    button_style = {
        "font": ("Arial", 13),
        "width": 20,
        "height": 2,
        "bg": "#ffffff",
        "fg": "#0A3D62",
        "bd": 0,
        "relief": "flat",
        "activebackground": "#d6ecff",
        "cursor": "hand2"
    }

    realtime_btn = tk.Button(
        btn_frame, text="☀️ 实时天气建议",
        command=lambda: [root.destroy(), show_realtime_window()],
        **button_style
    )
    realtime_btn.grid(row=0, column=0, padx=20)

    forecast_btn = tk.Button(
        btn_frame, text="📅 一周天气预报",
        command=lambda: [root.destroy(), show_forecast_window()],
        **button_style
    )
    forecast_btn.grid(row=0, column=1, padx=20)

    footer = tk.Label(
        root, text="© 2025 WeatherNow 智能助手",
        font=("Arial", 9), bg="#EAF6FF", fg="#888888"
    )
    footer.pack(side="bottom", pady=15)

    root.mainloop()


if __name__ == "__main__":
    launch_main_menu()
