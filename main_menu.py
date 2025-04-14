import tkinter as tk
from realtime_ui import show_realtime_window
from forecast_ui import show_forecast_window


def launch_main_menu():
    root = tk.Tk()
    root.title("🌤 WeatherNow - 智能天气助手")
    root.geometry("650x500")

    # ✅ 居中窗口（推荐加在每个界面）
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (650 // 2)
    y = (screen_height // 2) - (500 // 2)
    root.geometry(f"650x500+{x}+{y}")
    root.configure(bg="#EAF6FF")

    tk.Label(root, text="WeatherNow 智能天气助手", font=("Helvetica", 18, "bold"), bg="#EAF6FF", fg="#0A3D62").pack(
        pady=20)
    tk.Label(root, text="请选择你要进行的操作：", font=("Arial", 13), bg="#EAF6FF").pack(pady=10)

    btn_frame = tk.Frame(root, bg="#EAF6FF")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="☀️ 实时天气建议", font=("Arial", 12), width=20,
              command=lambda: [root.destroy(), show_realtime_window()]).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="📅 一周天气预报", font=("Arial", 12), width=20,
              command=lambda: [root.destroy(), show_forecast_window()]).grid(row=0, column=1, padx=10)

    root.mainloop()


if __name__ == "__main__":
    launch_main_menu()
