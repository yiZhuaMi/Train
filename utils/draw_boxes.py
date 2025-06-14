from PIL import Image, ImageDraw
import numpy as np
from module import consts
from config import config

def draw_boxes(image, boxes, color=consts.BOX_COLOR, width=consts.BOX_WIDTH):
    """
    在给定图像上画出给定的多个框。
    """
    # 将 numpy.ndarray 转换为 PIL.Image 对象
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    draw = ImageDraw.Draw(image)

    for box in boxes:
        # 获取框的坐标
        left = box.get_left()
        top = box.get_top()
        right = box.get_right()
        bottom = box.get_bottom()
        # 绘制矩形框
        draw.rectangle((left, top, right, bottom), outline=hex_to_rgb(color), width=width)
    
    # 绘制缩放原点标记
    origin_left = config.BOX_ORIGIN_LEFT
    origin_top = config.BOX_ORIGIN_TOP
    marker_size = 10  # 标记的大小
    marker_color = (0, 0, 255)  # 标记的颜色，这里设置为红色
    draw.rectangle((origin_left - marker_size, origin_top - marker_size, origin_left + marker_size, origin_top + marker_size), outline=marker_color, width=2)

    # 将 PIL.Image 对象转换回 numpy.ndarray
    image = np.array(image)
    
    return image

def hex_to_rgb(hex_color):
    """
    将十六进制颜色值转换为 RGB 元组。
    :param hex_color: 十六进制颜色值，如 "#RRGGBB"
    :return: RGB 元组，如 (R, G, B)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
