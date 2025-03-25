from config import config
from utils import ocr
from utils.crop_boxes import crop_boxes_from_image
from module.box import read_boxes_from_config
from module.consts import TargetType
from utils.draw_boxes import draw_boxes
import cv2
from utils.window_capture import WindowCapture

def recognize(img):
    # 识别
    text = ocr.recognize_train_number(img.image)
    
    res=f"box:{img.box.name} 识别结果:{text}"
    # print(res)
    if text is not None:
        cv2.imshow(f"{res}", img.image)

if __name__ == "__main__":
    # 读取框信息
    boxes = read_boxes_from_config(config.BOX_CONFIG_PATH)

    capturer = WindowCapture(config.CAPTURE_WINDOW_NAME)
    
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
    
    cv2.destroyAllWindows()