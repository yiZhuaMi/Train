from utils.crop_boxes import crop_boxes_from_image
from module.box import read_boxes_from_config
from module.croped_image import CroppedImage
from utils.draw_boxes import draw_boxes
from PIL import Image
import cv2
from utils.window_capture import WindowCapture

if __name__ == "__main__":
    # 读取框信息
    boxes = read_boxes_from_config("config/boxes.json")

    capturer = WindowCapture("桌面控制 152 576 447 9")
    
    while True:
        frame = capturer.get_frame()
        if frame is not None:            
            # 按给定的 box 进行画框
            cv2.imshow("Window with Boxes", draw_boxes(frame, boxes))
            # 对框中的内容进行截取
            cropped_images = crop_boxes_from_image(frame, boxes)
            # 打开新窗口显示框中的内容
            for i, cropped_img in enumerate(cropped_images):
                if cropped_img.image.size != 0:
                    cv2.imshow(f"{cropped_img.target_type} {i + 1}", cropped_img.image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()