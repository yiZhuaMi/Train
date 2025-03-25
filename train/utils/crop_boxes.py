from PIL import Image
from module.box import Box
from module.croped_image import CroppedImage
import numpy as np

def crop_boxes_from_image(image, boxes):
    """
    从图像中截取多个框，并返回截取后的图像列表。
    """
    cropped_images = []
    # 检查 image 是否为 numpy.ndarray 类型
    if isinstance(image, np.ndarray):
        for box in boxes:
            left = box.get_left()
            top = box.get_top()
            right = box.get_right()
            bottom = box.get_bottom()
            # 使用 numpy 切片进行截取
            cropped_image = CroppedImage(box, image[top:bottom, left:right])
            cropped_images.append(cropped_image)
    else:
        # 保留原有的 PIL.Image 处理逻辑
        for box in boxes:
            cropped_image = CroppedImage(image.crop((box.get_left(), box.get_top(), box.get_right(), box.get_bottom())), 
                                         box.type)
            cropped_images.append(cropped_image)
    return cropped_images