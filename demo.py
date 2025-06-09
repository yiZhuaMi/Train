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
from utils.write_result import write_to_excel

def recognize(img):
    """
    识别
    返回识别结果的字符串
    """
    result = None
    if img.box.type == TargetType.TRAIN_NUM or img.box.type == TargetType.TEST:
        result, confidence = ocr.recognize_train_number(img.image)
    elif img.box.type == TargetType.LIGHT:
        result, confidence = light_color.detect_signal_color(img.image)
    elif img.box.type == TargetType.RAIL_LINE:
        result, confidence = light_color.detect_rail_line_color(img.image)

    if result is not None and len(result) > 0:
        # print(f"box:{img.box.name} 识别结果:{result} 置信度:{confidence}")
        return result
    return ""

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
            # 对框中的内容进行截取
            cropped_images = crop_boxes_from_image(frame, boxes)
            frame_result = {}  # 用于存储当前帧的所有结果
            # 遍历截取的图像
            for cropped_img in cropped_images:
                if cropped_img.image.size == 0:
                    continue
                # 识别
                result = recognize(cropped_img)
                # 将结果存入 frame_result 字典
                frame_result[cropped_img.box.name] = {
                    "result_text":result,
                    "image":cropped_img.image
                    }

            print("当前帧的识别结果:", frame_result)
            write_to_excel(config.RESULT_PATH, frame_result)

            # 按给定的 box 进行画框
            cv2.imshow("Window with Boxes", draw_boxes(frame, boxes))
                    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # time.sleep(60)
    
    cv2.destroyAllWindows()