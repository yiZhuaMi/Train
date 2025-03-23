from utils.image_crop import crop_image
from module.box import Box
from module import consts

if __name__ == "__main__":
    # 图像路径
    input_image_path = "/Users/high_beauty/Documents/帅哥/铁路项目/train/resources/WX20250323.png"
    crop_image(input_image_path, Box(consts.BoxType.TRAIN_NUM, 111, 185))
