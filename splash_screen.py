import tkinter as tk
from PIL import Image, ImageTk
import time

from main_menu import launch_main_menu  # 自动进入主菜单界面


def show_main_app():
    splash.destroy()
    launch_main_menu()


# --- 创建启动界面 ---
splash = tk.Tk()
splash.title("加载中")
splash.geometry("650x500")
splash.overrideredirect(True)

# 居中显示
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (650 // 2)
y = (screen_height // 2) - (500 // 2)
splash.geometry(f"650x500+{x}+{y}")

# 加载背景图
bg_image = Image.open("splash_bg.png").resize((650, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(splash, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas = tk.Canvas(splash, width=650, height=500, highlightthickness=0)
canvas.pack()

bg_img = ImageTk.PhotoImage(Image.open("splash_bg.png").resize((650, 500)))
canvas.create_image(0, 0, anchor="nw", image=bg_img)

canvas.create_text(325, 120, text="🌤 WeatherNow", fill="black", font=("Segoe UI", 22, "bold"))
canvas.create_text(325, 220, text="实时天气与智能建议系统", fill="black", font=("Segoe UI", 12))
canvas.create_text(325, 320, text="正在加载，请稍候...", fill="black", font=("Arial", 10))

# 设置2秒后进入主程序
splash.after(2000, show_main_app)
splash.mainloop()
