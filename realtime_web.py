# realtime_web.py

from pywebio.input import input
from pywebio.output import (
    put_markdown, put_text, put_warning, clear,
    put_success, put_html
)
from weather_api import WeatherFetcher
from gpt_helper import get_advice_from_openrouter

API_TOKEN = "1645f94d966773652898a4b91f13a5494f2c97e9"  #

def realtime_weather_app():
    clear()
    put_markdown("## ☀️ 实时天气查询")
    put_html('<hr>')
    city = input("🌍 请输入城市名（拼音/英文）:")

    fetcher = WeatherFetcher(API_TOKEN)
    data = fetcher.get_weather(city)

    clear()
    put_markdown(f"### 📍 当前城市：**{city}**")

    if data:
        temp = data['iaqi'].get('t', {}).get('v', 'N/A')
        humidity = data['iaqi'].get('h', {}).get('v', 'N/A')
        wind = data['iaqi'].get('w', {}).get('v', 'N/A')
        aqi = data.get('aqi', 'N/A')
        update_time = data.get('time', {}).get('s', 'N/A')

        put_markdown("### 🌡 实时天气状况")
        put_text(f"🌡 温度：{temp}°C")
        put_text(f"💧 湿度：{humidity}%")
        put_text(f"🌬 风速：{wind} m/s")
        put_text(f"🧪 空气质量指数 AQI：{aqi}")
        put_text(f"📅 更新时间：{update_time}")

        put_markdown("### 🤖 穿衣建议")
        put_text("正在生成建议，请稍候...")

        prompt = (
            f"当前天气：温度 {temp}°C，湿度 {humidity}% ，风速 {wind} m/s ，AQI 为 {aqi}。\n"
            f"请给出简洁实用的穿衣与出行建议。"
        )

        suggestion = get_advice_from_openrouter(prompt)
        put_success(suggestion.strip())
    else:
        put_warning("❌ 查询失败，可能是城市名错误或网络问题。")
