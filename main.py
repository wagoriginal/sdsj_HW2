import tkinter as tk
from tkinter import messagebox
from weather_api import WeatherFetcher

# 替换成你的AQICN token
API_TOKEN = '1645f94d966773652898a4b91f13a5494f2c97e9'


class WeatherApp:
    def __init__(self, root):
        self.fetcher = WeatherFetcher(API_TOKEN)
        self.root = root
        self.root.title("WeatherNow 天气查询")
        self.root.geometry("400x300")

        self.city_entry = tk.Entry(root, font=('Arial', 14))
        self.city_entry.pack(pady=10)

        self.query_button = tk.Button(root, text="查询天气", command=self.query_weather)
        self.query_button.pack()

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack()

    def query_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("输入错误", "请输入城市名称")
            return

        data = self.fetcher.get_weather(city)
        self.result_text.delete("1.0", tk.END)

        if data:
            self.result_text.insert(tk.END, f"城市: {city}\n")
            self.result_text.insert(tk.END, f"温度: {data['iaqi'].get('t', {}).get('v', 'N/A')}°C\n")
            self.result_text.insert(tk.END, f"湿度: {data['iaqi'].get('h', {}).get('v', 'N/A')}%\n")
            self.result_text.insert(tk.END, f"空气质量指数: {data.get('aqi', 'N/A')}\n")
            self.result_text.insert(tk.END, f"风速: {data['iaqi'].get('w', {}).get('v', 'N/A')} m/s\n")
        else:
            self.result_text.insert(tk.END, "查询失败，可能是城市名错误或网络问题。")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
