from PIL import ImageDraw
from module import consts

def draw_boxes(image, boxes, color=consts.BOX_COLOR, width=consts.BOX_WIDTH):
    """
    在给定图像上画出给定的多个框。

    :param input_image_path: 输入图像的路径
    :param box: Box 类的实例，包含框的位置信息
    :param output_image_path: 输出图像的路径，如果为 None，则直接显示图像
    :param color: 框的颜色，默认为红色
    :param width: 框的线条宽度，默认为 2
    """

    draw = ImageDraw.Draw(image)

    for box in boxes:
        # 获取框的坐标
        left = box.get_left()
        top = box.get_top()
        right = box.get_right()
        bottom = box.get_bottom()
        # 绘制矩形框
        draw.rectangle((box.get_left(), 
                        box.get_top(), 
                        box.get_right(), 
                        box.get_bottom()), 
                        outline=color, 
                        width=width)
    # 显示图像
    image.show()