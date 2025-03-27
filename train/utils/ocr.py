from paddleocr import PaddleOCR
import cv2
import numpy as np
import random

# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # CPU/GPU 均可

def recognize_and_crop(image):
    image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # 进行 OCR 识别
    results = ocr.ocr(image, cls=True)

    extracted_text = []

    # 遍历 OCR 识别结果
    for idx, line in enumerate(results):
        for word_info in line:
            bbox, (text, confidence) = word_info[0], word_info[1]
            x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
            x_max, y_max = int(bbox[2][0]), int(bbox[2][1])

            # 截取文字区域
            cropped_img = image[y_min:y_max, x_min:x_max]
            recognize_split_text(cropped_img)
            cv2.imshow(text, cropped_img)
            cv2.imshow(f"origin_{text}", image)

            # 记录识别结果
            extracted_text.append(text)
            print(f"识别文字: {text}, 置信度: {confidence:.2f}")

    return extracted_text

def find_vertical_divide(binary_img, window_size=5):
    # 计算灰度直方图
    hist = cv2.calcHist([binary_img], [0], None, [256], [0, 256])

    # 找到黑色和白色的主峰（去掉低频干扰）
    main_colors = np.argsort(hist.ravel())[-2:]  # 选两个出现最多的灰度值

    # 计算每列接近哪个主色
    col_mean = np.mean(binary_img, axis=0)
    color_diff = np.abs(col_mean - main_colors[0]) - np.abs(col_mean - main_colors[1])

    # 找到变化最大的地方
    diff = np.abs(np.diff(color_diff))
    boundary_col = np.argmax(diff)

    return boundary_col


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

        cv2.imshow(f"side_{pos}_{all_texts}", side)

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
    print('result:',result)
    # 检查 result 是否为空
    if isinstance(result, list) and len(result) == 1 and result[0] is None:
        texts = []
    else:
        texts = [line[0][1][0] for line in result]
    
    return texts

if __name__ == '__main__':
    # 运行检测
    import os
    directory = '../image/num'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)
            print(file_path)
            print(recognize_and_crop(img))

    cv2.waitKey(0)