from utils.image_crop import crop_boxes, crop_boxes
from module.box import read_boxes_from_config
from utils.image_draw import draw_boxes
from PIL import Image

if __name__ == "__main__":
    # 打开图像
    try:
        input_path = "resources/WX20250323.png"
        image = Image.open(input_path)
    except FileNotFoundError:
        print(f"错误: 未找到文件{input_path}")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")    

    # 读取框信息
    boxes = read_boxes_from_config("config/boxes.json")
    # 截取框
    crop_boxes(image, boxes)
    # 绘制框
    draw_boxes(image, boxes)
