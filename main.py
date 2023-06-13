import tkinter as tk
from tkinter import messagebox
from threading import Thread
from voice import playScore
from behavior import detectSmoking

# 创建主窗口
window = tk.Tk()
window.title("课程项目")

# 创建左右两个Frame
left_frame = tk.Frame(window)
left_frame.pack(side="left")
right_frame = tk.Frame(window)
right_frame.pack(side="right")

# 在左侧Frame中添加组件
tk.Label(left_frame, text="请输入名字").pack()

entry_name = tk.Entry(left_frame)
entry_name.pack()

score_var = tk.StringVar()

def announce_score():
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("错误", "请输入名字")
        return
    score = playScore(name)
    score_var.set(f"{name}的成绩是{score}分")

tk.Button(left_frame, text="播报成绩", command=announce_score).pack()

# 添加显示成绩的Label
tk.Label(left_frame, textvariable=score_var).pack()

def start_smoking_detection():
    Thread(target=detectSmoking).start()

tk.Button(left_frame, text="检测是否吸烟", command=start_smoking_detection).pack()

# 在右侧Frame中添加Label用于显示摄像头画面
# （注意：这里仅创建了Label，还需要您自己实现从摄像头获取画面并更新Label的功能）
label_camera = tk.Label(right_frame)
label_camera.pack()

# 运行主循环
window.mainloop()
