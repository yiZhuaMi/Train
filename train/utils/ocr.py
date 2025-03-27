from paddleocr import PaddleOCR
import cv2
import random
import logging

# 设置日志级别为 ERROR，过滤掉 INFO 和 WARNING 日志
logging.getLogger("ppocr").setLevel(logging.ERROR)
# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)  # CPU/GPU 均可

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