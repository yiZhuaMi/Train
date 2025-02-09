# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

# 创建主窗口
root = tk.Tk()
root.title("盯控系统")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置主窗口的大小
root.geometry(f"{screen_width}x{screen_height}")

# 划分上模块
top_frame = tk.Frame(root, borderwidth=2, relief="solid")  # 添加边框线
top_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=10)
top_frame.config(height=int(screen_height * 3 / 5))

# 创建一个 Canvas 作为滚动条的容器
canvas = tk.Canvas(top_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建一个滚动条
scrollbar = ttk.Scrollbar(top_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# 配置 Canvas 的 xview 方法
canvas.configure(xscrollcommand=scrollbar.set)

# 打开视频文件
cap = cv2.VideoCapture('v1.mp4')

# 读取第一帧
ret, frame = cap.read()
if ret:
    # 将 OpenCV 图像转换为 PIL 图像
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image=img)

    # 创建一个 Frame 作为视频的容器
    video_frame = tk.Frame(canvas, borderwidth=2, relief="solid")  # 添加边框线
    video_label = tk.Label(video_frame, image=photo)
    video_label.image = photo
    video_label.pack()

    canvas.create_window((0, 0), window=video_frame, anchor=tk.NW)

    # 绑定滚动条事件
    def on_configure(event):
        # 更新 Canvas 的滚动区域
        canvas.configure(scrollregion=canvas.bbox("all"))

    video_frame.bind("<Configure>", on_configure)

# 创建左下模块（输出）的函数
def create_left_bottom_module(parent_frame, width):
    left_bottom_frame = tk.Frame(parent_frame, borderwidth=2, relief="solid")
    left_bottom_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    left_bottom_frame.config(width=width)

    # 创建垂直滚动条
    left_scrollbar = ttk.Scrollbar(left_bottom_frame, orient=tk.VERTICAL)
    left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建文本框用于显示多行内容
    left_text = tk.Text(left_bottom_frame, yscrollcommand=left_scrollbar.set)
    left_text.pack(fill=tk.BOTH, expand=True)

    # 关联滚动条和文本框
    left_scrollbar.config(command=left_text.yview)

    # 模拟添加多行内容
    for i in range(50):
        left_text.insert(tk.END, f"输出行 {i}\n")

    return left_bottom_frame

# 创建右下模块（车次表）的函数
def create_right_bottom_module(parent_frame):
    right_bottom_frame = tk.Frame(parent_frame, borderwidth=2, relief="solid")
    right_bottom_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 创建垂直滚动条
    right_scrollbar = ttk.Scrollbar(right_bottom_frame, orient=tk.VERTICAL)
    right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建文本框用于显示多行内容
    right_text = tk.Text(right_bottom_frame, yscrollcommand=right_scrollbar.set)
    right_text.pack(fill=tk.BOTH, expand=True)

    # 关联滚动条和文本框
    right_scrollbar.config(command=right_text.yview)

    # 模拟添加多行内容
    for i in range(50):
        right_text.insert(tk.END, f"车次表行 {i}\n")

    return right_bottom_frame

# 划分下模块
bottom_frame = tk.Frame(root, borderwidth=2, relief="solid")  # 添加边框线
bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10)

# 创建左下和右下模块
create_left_bottom_module(bottom_frame, int(screen_width / 2))
create_right_bottom_module(bottom_frame)

# 运行主循环
root.mainloop()

# 释放视频捕获对象
cap.release()