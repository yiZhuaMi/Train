import cv2
import numpy as np
from config import config

def detect_signal_color(image):
    """
    image 为cv2.imread返回的图片矩阵
    """
    # 转换为 HSV 颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_counts = {}

    # 检测每种颜色并统计像素数量
    for color, (lower, upper) in config.COLOR_RANGES.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        color_counts[color] = np.sum(mask)  # 统计该颜色的像素总数

    # 找到占比最多的颜色
    dominant_color = max(color_counts, key=color_counts.get)
    detected_color = None
    for color_name in config.LIGHT_COLOR_NAMES:
        if color_name in dominant_color:
            detected_color = color_name
            break
    return detected_color


if __name__ == '__main__':
    # 运行检测
    import os
    directory = '../image'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            print(file_path)
            print(detect_signal_color(img))
