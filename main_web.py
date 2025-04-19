# main_web.py
from pywebio.input import actions
from pywebio.output import put_markdown, put_html, clear
from pywebio import start_server
from realtime_web import realtime_weather_app
from forecast_web import forecast_weather_app

def main():
    clear()
    put_markdown("## 🌤 WeatherNow 智能天气助手")
    put_html("<hr>")
    put_markdown("欢迎使用网页版天气助手，请选择你要执行的功能：")

    action = actions(label="请选择功能：", buttons=[
        {"label": "☀️ 实时天气 + 建议", "value": "realtime"},
        {"label": "📅 一周天气预报 + 建议", "value": "forecast"},
    ])

    clear()
    if action == "realtime":
        realtime_weather_app()
    elif action == "forecast":
        forecast_weather_app()

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
