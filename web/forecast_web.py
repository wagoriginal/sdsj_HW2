from pywebio.input import input
from pywebio.output import (
    put_markdown, put_text, put_warning, put_success,
    put_scrollable, put_code, put_column, put_buttons,
    clear, put_html, put_row, put_table
)
import requests
from gpt_helper import get_advice_from_openrouter

WEATHER_API_KEY = "3dae6110dc194587b7e31855251404"

def forecast_weather_app():
    clear()
    put_markdown("### 📅 **一周天气预报**")
    put_html('<hr>')

    city = input("🌍 请输入城市名（拼音 / 英文 ）：")
    put_markdown(f"#### 📍 正在查询 {city} 的未来7天天气...")

    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=7&lang=zh"
    try:
        resp = requests.get(url)
        data = resp.json()
        if "error" in data:
            put_warning(f"❌ API错误：{data['error'].get('message', '未知错误')}")
            return
        if "forecast" not in data:
            put_warning("❌ 响应中未包含 forecast 字段")
            return

        lines = []
        gpt_input = ""
        for day in data["forecast"]["forecastday"]:
            date = day["date"]
            cond = day["day"]["condition"]["text"]
            tmin = day["day"]["mintemp_c"]
            tmax = day["day"]["maxtemp_c"]
            line = f"{date}：{cond}，{tmin:.1f}°C - {tmax:.1f}°C"
            lines.append([f"📅 {date}", f"{cond}", f"🌡 {tmin:.1f}°C - {tmax:.1f}°C"])
            gpt_input += f"{line}\n"

        put_markdown("### 📈 天气概览")
        put_table(header=["日期", "天气", "温度区间"], tdata=lines)

        put_markdown("### 🤖 穿衣建议")
        put_text("正在生成建议...请稍候...")
        prompt = (
            f"以下是未来一周 {city} 的天气情况：\n{gpt_input}\n"
            f"请为用户生成一段清晰、简洁、实用的穿衣建议（早晚温差 / 是否带伞 / 适合衣物）"
        )
        suggestion = get_advice_from_openrouter(prompt)

        put_success(suggestion.strip())

    except Exception as e:
        put_warning(f"❌ 异常：{type(e).__name__} - {e}")
