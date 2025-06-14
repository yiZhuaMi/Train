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
import glob

# 在文件顶部添加常量引用
from module.consts import (
    BOX_W_TRAIN_NUM, BOX_H_TRAIN_NUM,
    BOX_W_LIGHT, BOX_H_LIGHT,
    BOX_W_RAIL_LINE, BOX_H_RAIL_LINE
)

# 在 main 代码前添加全局变量
current_box = None  # 存储当前框状态：{"left": x, "top": y, "width": w, "height": h}
box_type_index = 0  # 0:车次框 1:信号灯框 2:轨道线框
box_step = 1        # 方向键移动步长

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
    # 自动读取config/boxes目录下所有json文件
    boxes = read_boxes_from_config(glob.glob(config.BOX_CONFIG_PATHS, recursive=True))
    
    # 新增视频文件读取
    video_path = "resources/test_tdcs.mp4"  # 根据实际文件类型调整扩展名
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0  # 新增帧计数器
    
    # 在进入循环前创建可调整大小的窗口
    cv2.namedWindow("Window with Boxes", cv2.WINDOW_NORMAL)
    
    def mouse_callback(event, x, y, flags, param):
        # if event == cv2.EVENT_LBUTTONDOWN:
        #     print(f"点击坐标: ({x}, {y})")
        global current_box, box_type_index
        if event == cv2.EVENT_LBUTTONDOWN:
            # 使用当前类型索引对应的尺寸
            type_sizes = [
                (BOX_W_TRAIN_NUM, BOX_H_TRAIN_NUM),
                (BOX_W_LIGHT, BOX_H_LIGHT),
                (BOX_W_RAIL_LINE, BOX_H_RAIL_LINE)
            ]
            current_width, current_height = type_sizes[box_type_index]
            
            current_box = {
                "left": x,
                "top": y,
                "width": current_width,
                "height": current_height
            }
    cv2.setMouseCallback("Window with Boxes", mouse_callback)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # 视频读取结束
            
        # 裁剪出黑底
        if frame is not None:
            frame = frame[config.TOP_START:config.TOP_END, 
                          config.LEFT_START:config.LEFT_END]

        frame_count += 1  # 更新帧计数
        # print(frame_count)
        
        if frame is not None:            
            # 对框中的内容进行截取
            cropped_images = crop_boxes_from_image(frame, boxes)
            frame_result = {}  # 用于存储当前帧的所有结果
            # 遍历截取的图像
            for cropped_img in cropped_images:
                if cropped_img.image.size == 0:
                    continue
            #     # 识别
            #     result = recognize(cropped_img)
            #     # 将结果存入 frame_result 字典
            #     frame_result[cropped_img.box.name] = {
            #         "result_text":result,
            #         "image":cropped_img.image
            #         }

            # # print("当前帧的识别结果:", frame_result)
            # write_to_excel(config.RESULT_PATH, frame_result)

            #------------------------------------帧加工----------------------------------------
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

            #------------------------------------选框交互----------------------------------------
            # 处理按键输入
            key = cv2.waitKeyEx(10)  # 使用 waitKeyEx 获取扩展键码
            
            # 处理框体操作
            if current_box:
                # 切换尺寸类型
                if key == ord('n') or key == ord('N'):
                    box_type_index = (box_type_index + 1) % 3
                    type_sizes = [
                        (BOX_W_TRAIN_NUM, BOX_H_TRAIN_NUM),
                        (BOX_W_LIGHT, BOX_H_LIGHT),
                        (BOX_W_RAIL_LINE, BOX_H_RAIL_LINE)
                    ]
                    current_box["width"], current_box["height"] = type_sizes[box_type_index]

                # 处理方向键移动
                h, w = displayed_frame.shape[:2]
                if key == 63232:  # 上键 ↑ (Mac)
                    current_box["top"] = max(0, current_box["top"] - box_step)
                elif key == 63233:  # 下键 ↓ (Mac)
                    current_box["top"] = min(h - current_box["height"], current_box["top"] + box_step)
                elif key == 63234:  # 左键 ← (Mac)
                    current_box["left"] = max(0, current_box["left"] - box_step)
                elif key == 63235:  # 右键 → (Mac)
                    current_box["left"] = min(w - current_box["width"], current_box["left"] + box_step)
                
                # 绘制当前框
                cv2.rectangle(displayed_frame,
                            (current_box["left"], current_box["top"]),
                            (current_box["left"] + current_box["width"],
                             current_box["top"] + current_box["height"]),
                            (0, 255, 0), 1)
                
                # 在框下方添加坐标信息（Y坐标下移20像素）
                info_text = f"X:{current_box['left']} Y:{current_box['top']} W:{current_box['width']} H:{current_box['height']}"
                cv2.putText(displayed_frame, info_text,
                           (current_box["left"], current_box["top"] + current_box["height"] + 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

                # 回车确认
                if key == 13:  # 回车键
                    print(f"当前框坐标: Left={current_box['left']} Top={current_box['top']} "
                          f"尺寸: {current_box['width']}x{current_box['height']}")
                    current_box = None

            #----------------------------------------------------------------------------
            
            cv2.imshow("Window with Boxes", displayed_frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    
    # 新增资源释放
    cap.release()
    cv2.destroyAllWindows()
