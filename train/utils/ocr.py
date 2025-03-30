from paddleocr import PaddleOCR
import cv2
import numpy as np
import random
import logging


# 设置日志级别为 ERROR，过滤掉 INFO 和 WARNING 日志
logging.getLogger("ppocr").setLevel(logging.ERROR)
# 初始化 OCR（启用方向分类和轻量级模型）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)  # CPU/GPU 均可


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


def extract_text_from_white_bg(image):
    # 扩大图像
    image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # 读取图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化：让白色背景变白，黑色文字保持
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # cv2.imshow(f"binary", binary)

    # **形态学腐蚀**（断开薄弱连接）
    # erosion_size = 3
    # kernel = np.ones((erosion_size, erosion_size), np.uint8)
    # eroded = cv2.erode(binary, kernel, iterations=1)

    # 进行连通区域分析
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    # 找到面积最大的白色簇（跳过背景）
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    # 创建新图像，只保留最大簇
    largest_cluster = np.zeros_like(binary)
    largest_cluster[labels == largest_label] = 255  # 仅保留最大簇

    # cv2.imshow(f"largest_cluster", largest_cluster)

    # 创建掩码：只保留白色背景部分
    # mask = cv2.inRange(binary, 230, 255)
    # cv2.imshow(f"mask", mask)

    # 过滤掉非白色背景的区域
    # filtered_image = cv2.bitwise_and(binary, binary, mask=mask)
    #
    # cv2.imshow(f"filtered_image", filtered_image)

    # 使用 PaddleOCR 进行识别
    result = ocr.ocr(largest_cluster, cls=True)

    # 输出识别结果
    for line in result:
        if line is None:
            return None, None

        for word_info in line:
            text, confidence = word_info[1][0], word_info[1][1]
            # print(f"识别到: {text} (置信度: {confidence})")
            return text, confidence

    return None, None


def recognize_train_number(image):
    # 扩大图像
    image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # 进行 OCR 识别
    results = ocr.ocr(image, cls=True)

    # 检查 results 是否为 None 或者空列表
    if results is None or len(results) == 0:
        return None

    # 遍历 OCR 识别结果
    for idx, line in enumerate(results):
        # 再次检查 line 是否为 None
        if line is None:
            continue
        # 检查 line 是否可迭代
        if not isinstance(line, (list, tuple)):
            continue
        for word_info in line:
            bbox, (text, confidence) = word_info[0], word_info[1]
            x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
            x_max, y_max = int(bbox[2][0]), int(bbox[2][1])

            # 截取文字区域
            cropped_img = image[y_min:y_max, x_min:x_max]
            train_num, train_num_conf = extract_text_from_white_bg(cropped_img)

            if train_num is None:
                return None

            # cv2.imshow(text, cropped_img)
            # cv2.imshow(f"origin_{text}", image)

            # 记录识别结果
            # extracted_text.append(text)
            # print(f"识别文字: {text}, 置信度: {confidence:.2f}")
            return TrainNumRecognizeResult(text, confidence, train_num, train_num_conf)

    return None


def recognize_train_number_old(image):
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
        return "", 0
    
    # 只取第一个识别结果
    line = result[0]
    text = line[0][1][0]
    confidence = line[0][1][1]
    return text, confidence

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