from paddleocr import PaddleOCR
import cv2
import numpy as np
import random
import logging

# 设置日志级别为 ERROR，过滤掉 INFO 和 WARNING 日志
logging.getLogger("ppocr").setLevel(logging.ERROR)
# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)  # CPU/GPU 均可


def find_vertical_divide(binary_img):
    """通过垂直投影找到背景分界线"""
    # 统计每列白色像素数量
    col_white = np.sum(binary_img == 255, axis=0)
    # 找到变化最剧烈的位置
    diff = np.abs(np.diff(col_white))
    divide_pos = np.argmax(diff) + 1  # 补偿差分偏移
    return divide_pos


def recognize_split_text(image):
    # 1. 灰度化+二值化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 2. 动态查找分界线
    divide_x = find_vertical_divide(binary)

    # 3. 分割左右区域
    left = binary[:, :divide_x]
    right = binary[:, divide_x:]

    cv2.imshow(f"binary", binary)
    cv2.imshow(f"left", left)
    cv2.imshow(f"right", right)

    print(ocr.ocr(binary, cls=True))
    # 4. 自适应颜色处理
    def process_side(side):
        # 自动判断是否需要颜色反转
        if np.mean(side) > 127:  # 背景偏白
            side = cv2.bitwise_not(side)
        return side

    right = process_side(right)
    # 5. 分别识别
    all_texts = []
    for side, pos in [(left, "left"), (right, "right")]:
        processed = process_side(side)
        cv2.imshow(f"processed_{pos}", processed)
        result = ocr.ocr(side, cls=True)
        print(result)
        if result and result[0]:
            texts = [line[0][1][0] for line in result]
            print(f"{pos} side found:", texts)
            all_texts.extend(texts)

    return all_texts

def recognize_train_number(image):
    # 1. 预处理图像
    # random_number = random.randint(1, 1000000)
    # cv2.imshow(str(random_number), image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度化
    # cv2.imshow(str(random_number+1), gray)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # 二值化（根据实际调整阈值）
    # cv2.imshow(str(random_number+2), thresh)

    # 2. OCR 识别
    result = ocr.ocr(gray, cls=True)
    # 检查 result 是否为空
    if isinstance(result, list) and len(result) == 1 and result[0] is None:
        return [], []
    else:
        texts = []
        confidences = []
        for line in result:
            # 提取识别出的文本
            text = line[0][1][0]
            texts.append(text)
            # 提取识别结果的置信度
            confidence = line[0][1][1]
            confidences.append(confidence)
        return texts, confidences

if __name__ == '__main__':
    # 运行检测
    import os
    directory = '../image/num'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            print(file_path)
            print(recognize_split_text(img))

    cv2.waitKey(0)