import os
import sys
from PIL import Image
from module.box import Box
from module import consts

def crop_image(input_path, box):
    try:
        if not isinstance(box, Box):
            print("错误: 输入参数不是Box类型")
            return
        # 打开图像
        image = Image.open(input_path)
        # 截取矩形区域
        cropped_image = image.crop((box.get_left(), box.get_top(), box.get_right(), box.get_bottom()))
        # 直接打开截取后的图像
        cropped_image.show()
        print("已成功截取图像并打开查看")
    except FileNotFoundError:
        print(f"错误: 未找到文件 {input_path}")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")    