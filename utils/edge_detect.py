import cv2

# 1. 读取图像
image = cv2.imread('resources/test4.jpg')  # 替换为实际图片路径

# 检查图像是否成功读取
if image is None:
    print("无法读取图像，请检查图片路径是否正确。")
else:
    # 2. 图像预处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 3. 轮廓检测
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化计数器
    index = 0
    for contour in contours:
        # 4. 获取外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        # 5. 裁切图像
        cropped_image = image[y:y + h, x:x + w]
        # 修改窗口名称，包含序号
        cv2.imshow(f'cropped_image_{index}.jpg', cropped_image)  
        # 计数器加 1
        index += 1

    # 等待按键关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()