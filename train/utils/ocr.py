from paddleocr import PaddleOCR
import cv2

# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)  # CPU/GPU 均可

def recognize_train_number(image_path):
    # 1. 图像预处理
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # 二值化（根据实际调整阈值）

    # 2. OCR 识别
    result = ocr.ocr(thresh, cls=True)
    texts = [line[0][1][0] for line in result]
    return texts