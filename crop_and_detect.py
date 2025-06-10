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
    
    # 新增视频文件读取
    video_path = "resources/test_tdcs.mp4"  # 根据实际文件类型调整扩展名
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0  # 新增帧计数器
    
    # 在进入循环前创建可调整大小的窗口
    cv2.namedWindow("Window with Boxes", cv2.WINDOW_NORMAL)
    
    # 新增鼠标回调函数绑定
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"点击坐标: ({x}, {y})")
    cv2.setMouseCallback("Window with Boxes", mouse_callback)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # 视频读取结束
            
        # 裁剪出黑底
        if frame is not None:
            frame = frame[80:960, 10:4500]  # numpy切片格式 [y_start:y_end, x_start:x_end]

        frame_count += 1  # 更新帧计数
        print(frame_count)
        
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

            # print("当前帧的识别结果:", frame_result)
            # write_to_excel(config.RESULT_PATH, frame_result)

            # 按给定的 box 进行画框
            displayed_frame = draw_boxes(frame, boxes)
            # 在左下角添加绿色文字 (坐标单位：像素)
            text = f"FRAME: {frame_count}"
            cv2.putText(displayed_frame, 
                       text, 
                       (30, displayed_frame.shape[0] - 30),  # X=30, Y=高度-30
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1.0,  # 字体大小
                       (0, 255, 0),  # BGR绿色
                       2)  # 线宽
            
            # 获取实际帧尺寸并调整窗口
            h, w = displayed_frame.shape[:2]
            cv2.resizeWindow("Window with Boxes", w, h)
            
            cv2.imshow("Window with Boxes", displayed_frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    
    # 新增资源释放
    cap.release()
    cv2.destroyAllWindows()