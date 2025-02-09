# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# 创建主窗口
root = tk.Tk()
root.title("简单的桌面应用")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置主窗口的大小
root.geometry(f"{screen_width}x{screen_height}")

# 划分上模块
top_frame = tk.Frame(root)
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

# 创建一个 Frame 作为轨道图的容器
track_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=track_frame, anchor=tk.NW)

# 绑定滚动条事件
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

track_frame.bind("<Configure>", on_configure)

# 在轨道图中添加一些示例内容
for i in range(20):
    tk.Label(track_frame, text=f"轨道图内容 {i}").pack(side=tk.LEFT, padx=10)

# 划分下模块
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10)

# 划分左下模块（输出）
left_bottom_frame = tk.Frame(bottom_frame)
left_bottom_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
left_bottom_frame.config(width=int(screen_width / 2))

# 在左下模块中添加标签
tk.Label(left_bottom_frame, text="输出").pack(pady=20)

# 划分右下模块（车次表）
right_bottom_frame = tk.Frame(bottom_frame)
right_bottom_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 在右下模块中添加标签
tk.Label(right_bottom_frame, text="车次表").pack(pady=20)

# 运行主循环
root.mainloop()