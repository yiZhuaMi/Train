import time
from config import config
from utils import ocr
from utils import light_color
from utils.crop_boxes import crop_boxes_from_image
from module.box import read_boxes_from_config
from module.consts import TargetType
from utils.draw_boxes import draw_boxes
import cv2
from utils.window_capture import WindowCapture
import sys

def recognize(img):
    """
    识别
    """
    if img.box.type == TargetType.TRAIN_NUM or img.box.type == TargetType.TEST:
        # 识别
        text, confidence = ocr.recognize_train_number(img.image)
        res=f"box:{img.box.name} 识别结果:{text} 置信度:{confidence}"
        if text is not None and len(text) > 0:
            print(res)

    elif img.box.type == TargetType.LIGHT:
        result = light_color.detect_signal_color(img.image)
        res = f"box:{img.box.name} 识别结果:{result}"
        if result is not None and len(result) > 0:
            print(res)

    # 返回map，key：name，value：识别结果

if __name__ == "__main__":
    # 读取框信息
    boxes = read_boxes_from_config(config.BOX_CONFIG_PATH)

    window_name = None
    if sys.platform.startswith("win"):
        window_name = config.CAPTURE_WIN_WINDOW_NAME
    elif sys.platform.startswith("darwin"):
        window_name = config.CAPTURE_MAC_WINDOW_NAME

    capturer = WindowCapture(window_name)
    
    while True:
        frame = capturer.get_frame()
        if frame is not None:            
            # 按给定的 box 进行画框
            cv2.imshow("Window with Boxes", draw_boxes(frame, boxes))
            # 对框中的内容进行截取
            cropped_images = crop_boxes_from_image(frame, boxes)
            # 遍历截取的图像
            for i, cropped_img in enumerate(cropped_images):
                if cropped_img.image.size == 0:
                    continue
                # 识别
                recognize(cropped_img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # time.sleep(60)
    
    cv2.destroyAllWindows()