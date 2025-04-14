import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from gpt_helper import get_advice_from_openrouter  # 你已有的 GPT 接口模块

WEATHER_API_KEY = "3dae6110dc194587b7e31855251404"  # ✅ 替换为你自己的 key


def get_week_forecast(city):
    try:
        # WeatherAPI 查询 7 天预报
        url = (
            f"https://api.weatherapi.com/v1/forecast.json?"
            f"key={WEATHER_API_KEY}&q={city}&days=7&lang=zh"
        )
        resp = requests.get(url)
        print("🔍 请求URL:", url)
        print("🔍 状态码:", resp.status_code)
        weather_data = resp.json()

        if "forecast" not in weather_data:
            return "❌ 无法获取天气数据（未包含 forecast 字段）", ""

        forecast_days = weather_data["forecast"]["forecastday"]
        forecast_lines = []
        gpt_input = ""

        for day in forecast_days:
            date = day["date"]
            condition = day["day"]["condition"]["text"]
            temp_min = day["day"]["mintemp_c"]
            temp_max = day["day"]["maxtemp_c"]
            line = f"{date}：{condition}，{temp_min:.1f}°C - {temp_max:.1f}°C"
            forecast_lines.append(line)
            gpt_input += line + "\n"

        return "\n".join(forecast_lines), gpt_input

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ 发生错误：{type(e).__name__} - {e}", ""


def show_forecast_window():
    root = tk.Tk()
    root.title("📅 一周天气预报")
    root.geometry("650x500")

    # ✅ 居中窗口（推荐加在每个界面）
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (650 // 2)
    y = (screen_height // 2) - (500 // 2)
    root.geometry(f"650x500+{x}+{y}")
    root.configure(bg="#EAF6FF")

    tk.Label(root, text="未来7天天气预测", font=("Helvetica", 18, "bold"),
             bg="#EAF6FF", fg="#0A3D62").pack(pady=15)

    input_frame = tk.Frame(root, bg="#EAF6FF")
    input_frame.pack()

    tk.Label(input_frame, text="请输入城市名（拼音/英文/中文）:", font=("Arial", 12), bg="#EAF6FF").grid(row=0, column=0)
    city_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    city_entry.grid(row=0, column=1, padx=10)
    city_entry.focus()

    forecast_text = tk.Text(root, height=10, font=("Courier", 11), bg="white")
    forecast_text.pack(padx=20, pady=10, fill=tk.BOTH)

    advice_text = tk.Text(root, height=7, font=("Courier", 11), bg="white")
    advice_text.pack(padx=20, pady=5, fill=tk.BOTH)

    def query_forecast():
        city = city_entry.get().strip()
        if not city:
            messagebox.showwarning("输入错误", "请输入城市名")
            return

        forecast_text.config(state=tk.NORMAL)
        advice_text.config(state=tk.NORMAL)
        forecast_text.delete("1.0", tk.END)
        advice_text.delete("1.0", tk.END)

        forecast_text.insert(tk.END, "🔍 正在查询天气...\n")
        root.update_idletasks()

        forecast_str, gpt_input = get_week_forecast(city)

        forecast_text.delete("1.0", tk.END)
        forecast_text.insert(tk.END, forecast_str)
        forecast_text.config(state=tk.DISABLED)

        if gpt_input:
            advice_text.insert(tk.END, "🤖 正在生成建议...\n")
            root.update_idletasks()
            prompt = (
                f"以下是未来一周 {city} 的天气情况：\n{gpt_input}\n"
                f"请为用户生成一段实用的穿衣建议，可以简要总结温度趋势和重点提醒。"
            )
            suggestion = get_advice_from_openrouter(prompt)
            advice_text.delete("1.0", tk.END)
            advice_text.insert(tk.END, suggestion)
            advice_text.config(state=tk.DISABLED)

    tk.Button(root, text="📅 查询一周天气", font=("Arial", 12), command=query_forecast).pack(pady=10)
    root.bind("<Return>", lambda event: query_forecast())
    root.mainloop()
