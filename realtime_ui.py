from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from weather_api import WeatherFetcher
from gpt_helper import get_advice_from_openrouter
from PIL import Image, ImageTk


def show_realtime_window():
    API_TOKEN = '1645f94d966773652898a4b91f13a5494f2c97e9'

    class WeatherApp:
        def __init__(self, root):
            self.fetcher = WeatherFetcher(API_TOKEN)
            self.root = root
            self.root.title("🌤 WeatherNow - 实时天气助手")
            root.geometry("650x500")

            # ✅ 居中窗口（推荐加在每个界面）
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width // 2) - (650 // 2)
            y = (screen_height // 2) - (500 // 2)
            root.geometry(f"650x500+{x}+{y}")
            self.root.configure(bg="#EAF6FF")

            # 标题
            title = tk.Label(root, text="WeatherNow 实时天气 & 智能建议", font=("Helvetica", 20, "bold"),
                             bg="#EAF6FF", fg="#0A3D62")
            title.pack(pady=15)

            # 输入区域
            input_frame = tk.Frame(root, bg="#EAF6FF")
            input_frame.pack()

            tk.Label(input_frame, text="请输入城市名（中文或英文）:", font=("Arial", 13), bg="#EAF6FF").grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=5)
            self.city_entry = tk.Entry(input_frame, font=("Arial", 13), width=20)
            self.city_entry.grid(row=0, column=1, padx=5)
            self.city_entry.focus()

            self.query_button = ttk.Button(input_frame, text="🌍 查询", command=self.query_weather)
            self.query_button.grid(row=0, column=2, padx=10)

            # 结果显示区域
            result_frame = tk.Frame(root, bg="#EAF6FF")
            result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

            # 天气信息文本框
            self.weather_label = tk.Label(result_frame, text="🌦 天气信息", font=("Arial", 12, "bold"), bg="#EAF6FF")
            self.weather_label.grid(row=0, column=0, sticky="w", padx=10)

            self.weather_text = tk.Text(result_frame, height=8, font=("Courier", 11), bg="#ffffff", wrap=tk.WORD)
            self.weather_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
            self.weather_text.config(state=tk.DISABLED)

            # 智能建议文本框
            self.advice_label = tk.Label(result_frame, text="🧠 穿衣与出行建议", font=("Arial", 12, "bold"),
                                         bg="#EAF6FF")
            self.advice_label.grid(row=2, column=0, sticky="w", padx=10)

            self.advice_text = tk.Text(result_frame, height=6, font=("Courier", 11), bg="#ffffff", wrap=tk.WORD)
            self.advice_text.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
            self.advice_text.config(state=tk.DISABLED)

            # 布局伸缩配置
            result_frame.grid_rowconfigure(1, weight=1)
            result_frame.grid_rowconfigure(3, weight=1)
            result_frame.grid_columnconfigure(0, weight=1)

            # 绑定回车键
            self.root.bind("<Return>", lambda event: self.query_weather())

        def query_weather(self):
            city = self.city_entry.get().strip()
            if not city:
                messagebox.showwarning("输入错误", "请输入城市名称")
                return

            self.weather_text.config(state=tk.NORMAL)
            self.advice_text.config(state=tk.NORMAL)
            self.weather_text.delete("1.0", tk.END)
            self.advice_text.delete("1.0", tk.END)
            self.weather_text.insert(tk.END, "🔍 正在查询天气...\n")
            self.advice_text.insert(tk.END, "🤖 正在生成建议...\n")
            self.root.update_idletasks()

            data = self.fetcher.get_weather(city)

            if data:
                temp = data['iaqi'].get('t', {}).get('v', 'N/A')
                hum = data['iaqi'].get('h', {}).get('v', 'N/A')
                wind = data['iaqi'].get('w', {}).get('v', 'N/A')
                aqi = data.get('aqi', 'N/A')
                time = data.get('time', {}).get('s', 'N/A')

                weather_summary = (
                    f"📍 城市: {city}\n"
                    f"🌡 温度: {temp}°C\n"
                    f"💧 湿度: {hum}%\n"
                    f"🌬 风速: {wind} m/s\n"
                    f"🧪 空气质量指数 (AQI): {aqi}\n"
                    f"📅 更新时间: {time}\n"
                )

                self.weather_text.delete("1.0", tk.END)
                self.weather_text.insert(tk.END, weather_summary)
                self.weather_text.config(state=tk.DISABLED)

                # 获取 GPT 建议
                advice_prompt = f"城市：{city}，温度：{temp}℃，湿度：{hum}%，风速：{wind}m/s，空气质量指数：{aqi}"
                suggestion = get_advice_from_openrouter(advice_prompt)

                self.advice_text.delete("1.0", tk.END)
                self.advice_text.insert(tk.END, suggestion)
                self.advice_text.config(state=tk.DISABLED)
            else:
                self.weather_text.delete("1.0", tk.END)
                self.advice_text.delete("1.0", tk.END)
                self.weather_text.insert(tk.END, "❌ 查询失败，城市名可能有误，或网络连接问题。")
                self.weather_text.config(state=tk.DISABLED)
                self.advice_text.config(state=tk.DISABLED)

    root = tk.Tk()
    root.geometry("650x500")

    # ✅ 居中窗口（推荐加在每个界面）
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (650 // 2)
    y = (screen_height // 2) - (500 // 2)
    root.geometry(f"650x500+{x}+{y}")
    root.title("☀️ 实时天气查询")
    app = WeatherApp(root)
    root.mainloop()
