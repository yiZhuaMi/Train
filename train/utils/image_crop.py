from PIL import Image
from module.box import Box

def crop_boxes(image, boxes):
    for box in boxes:
        if not isinstance(box, Box):
            print("错误: 列表中的元素不是Box类型，跳过该元素")
            continue
        # 截取矩形区域
        cropped_image = image.crop((box.get_left(), box.get_top(), box.get_right(), box.get_bottom()))
        # 直接打开截取后的图像
        cropped_image.show()
