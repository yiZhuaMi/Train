import cv2
import numpy as np
from mss import mss
import time

# 设置截图区域（左上角x, 左上角y, 宽度, 高度）
monitor = {"top": 100, "left": 100, "width": 800, "height": 600}

# 创建mss对象
sct = mss()

# 帧率统计相关变量
start_time = time.time()
fps = 0

def process_frame(frame):
    """在此处添加自定义的图像处理逻辑"""
    # 示例：转换为灰度图
    # return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

while True:
    # 截取屏幕
    sct_img = sct.grab(monitor)
    
    # 转换为numpy数组
    frame = np.array(sct_img)
    
    # 颜色空间转换（MSS返回的是BGRA格式）
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    # 处理帧
    processed_frame = process_frame(frame)
    
    # 计算帧率
    fps = 1 / (time.time() - start_time)
    start_time = time.time()
    
    # 显示帧率
    cv2.putText(processed_frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # 显示画面
    cv2.imshow("Screen Capture", processed_frame)
    
    # 退出条件（按ESC退出）
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()