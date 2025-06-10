from paddleocr import PaddleOCR
import cv2
import numpy as np
import random
import logging
import re
from config import config


# 设置日志级别为 ERROR，过滤掉 INFO 和 WARNING 日志
logging.getLogger("ppocr").setLevel(logging.ERROR)
# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True)  # CPU/GPU 均可


class TrainNumRecognizeResult:
    def __init__(self, all_num:str, all_num_conf:str, train_num:str, train_num_conf:str):
        self.all_num = all_num                  #车牌上的所有字符
        self.all_num_conf = all_num_conf        #所有字符的识别置信度
        self.train_num = train_num              #车牌上的车次号
        self.train_num_conf = train_num_conf    #车次号的识别置信度

        if ' ' in self.train_num:
            self.train_num = max(self.train_num.split(' '), key=len)

        self.time_diff = ''                     #车牌上的晚点时差
        if len(self.all_num) != len(self.train_num):
            index = self.all_num.find(self.train_num)
            if index != -1:
                self.time_diff = (self.all_num[:index] + self.all_num[index + len(self.train_num):]).strip()
        else:
            self.all_num = self.all_num if self.all_num_conf > self.train_num_conf else self.train_num
            self.all_num_conf = self.all_num_conf if self.all_num_conf > self.train_num_conf else self.train_num_conf
            self.train_num = self.train_num if self.train_num_conf > self.all_num_conf else self.all_num
            self.train_num_conf = self.train_num_conf if self.train_num_conf > self.all_num_conf else self.all_num_conf


    def __str__(self):
        return f"TrainNumRecognizeResult(all_num:{self.all_num}, all_num_conf:{self.all_num_conf}, train_num:{self.train_num}, train_num_conf:{self.train_num_conf}, time_diff:{self.time_diff})"


def resize_with_opencv(image, scale_factor=2.0):
    """
    使用OpenCV插值放大图片
    :param image: 输入图片
    :param scale_factor: 放大倍数（例如2.0表示放大2倍）
    :return: 放大后的图像
    """

    # 计算新尺寸
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    new_size = (width, height)

    # 选择插值方法（推荐INTER_CUBIC或INTER_LINEAR）
    resized_img = cv2.resize(
        image,
        new_size,
        interpolation=cv2.INTER_CUBIC  # 其他选项：INTER_LINEAR, INTER_NEAREST, INTER_LANCZOS4
    )

    return resized_img


def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # 中文字符的Unicode范围
    return bool(pattern.search(text))

def clean_string(text):
    # 匹配汉字、字母、数字
    pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')
    # 替换所有非汉字、字母、数字的字符为空
    cleaned_text = pattern.sub('', text)
    return cleaned_text

def get_largest_white_region_bbox(image):
    """
    获取图片中最大的白色区域的外包围框
    :param image: 输入的图像
    :return: 外包围框的坐标 (x, y, x + w, y + h)"
    """
    # 1. 图片转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 二值化处理（假设白色为目标，阈值根据实际情况调整）
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 3. 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    # 4. 找到最大轮廓（白色像素最多的区域）
    largest_contour = max(contours, key=cv2.contourArea)

    # 5. 获取外包围框
    x, y, w, h = cv2.boundingRect(largest_contour)
    bbox = (x, y, x + w, y + h)  # 左上和右下坐标

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # 6. 截取外包围框区域
    cropped = image[y:y + h, x:x + w]

    return bbox, cropped

def recognize_train_number(image):
    image = resize_with_opencv(image)

    # 进行第一次 OCR 识别
    results = ocr.ocr(image, det=False, cls=False)
    if results is None or len(results) == 0:
        return None, 0

    # 遍历 OCR 识别结果
    for idx, line in enumerate(results):
        # 再次检查 line 是否为 None
        if line is None:
            continue
        # 检查 line 是否可迭代
        if not isinstance(line, (list, tuple)):
            continue

        for word_info in line:
            if has_chinese(word_info[0]):
                return clean_string(word_info[0]), word_info[1]

    bbox, cropped_image = get_largest_white_region_bbox(image)
    # cv2.imshow(f"image", image)
    # cv2.imshow(f"cropped_image", cropped_image)
    # cv2.moveWindow("cropped_image", 500, 500)

    if bbox is None:
        return None, 0

    # 检查宽高比是否符合车牌的宽高比范围
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    w_h_ratio = w / float(h)
    # print(f'{results}: {w_h_ratio}')
    if w_h_ratio < config.TRAIN_NUM_WIDTH_HEIGHT_RATIO_LOWER or w_h_ratio > config.TRAIN_NUM_WIDTH_HEIGHT_RATIO_UPPER:
        return "车次号不完整", 0


    # 进行 OCR 识别
    results = ocr.ocr(cropped_image, det=False, cls=False)

    # 检查 results 是否为 None 或者空列表
    if results is None or len(results) == 0:
        return None, 0

    # 遍历 OCR 识别结果
    for idx, line in enumerate(results):
        # 再次检查 line 是否为 None
        if line is None:
            continue
        # 检查 line 是否可迭代
        if not isinstance(line, (list, tuple)):
            continue

        for word_info in line:
            return clean_string(word_info[0]), word_info[1]

        return None, 0



if __name__ == '__main__':
    # 运行检测
    import os
    directory = '../image/num'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            print(file_path)
            print(recognize_train_number(img))

            cv2.waitKey(0)