import cv2
import numpy as np
from module import consts

def detect_main_color(image, color_range:dict):
    """
            image 为cv2.imread返回的图片矩阵
            返回占比多且离中心近的颜色
            """
    # 转换为 HSV 颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 获取图像中心坐标
    height, width = image.shape[:2]
    center_x, center_y = width // 2, height // 2

    color_scores = {}

    # 检测每种颜色并计算加权得分
    for color, (lower, upper) in color_range.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # 获取该颜色所有像素的坐标
        y_coords, x_coords = np.where(mask > 0)

        # 如果没有该颜色的像素，跳过
        if len(x_coords) == 0:
            color_scores[color] = 0
            continue

        # 计算这些像素到中心的平均距离
        distances = np.sqrt((x_coords - center_x) ** 2 + (y_coords - center_y) ** 2)
        avg_distance = np.mean(distances)

        # 计算该颜色的像素数量
        pixel_count = len(x_coords)

        # 计算得分：像素数量越多得分越高，平均距离越近得分越高
        # 距离平方，使靠近中心的像素更有优势
        score = pixel_count / (avg_distance ** 2 + 1)
        color_scores[color] = score

    # 找到得分最高的颜色
    if not color_scores:
        return None

    dominant_color = max(color_scores, key=color_scores.get)

    return dominant_color.name, color_scores[dominant_color]

def detect_signal_color(image):
    return detect_main_color(image, consts.SIGNAL_COLOR_RANGES)


def detect_rail_line_color(image):
    return detect_main_color(image, consts.RAIL_LINE_COLOR_RANGES)

if __name__ == '__main__':
    # 运行检测
    import os
    directory = '../image/rail_line_hsv'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            print(file_path)
            print(detect_rail_line_color(img))
