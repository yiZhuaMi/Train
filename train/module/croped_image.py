class CroppedImage:
    def __init__(self, image, target_type):
        """
        初始化 CroppedImage 类的实例。

        :param image: 裁剪后的图像数据
        :param target_type: 框的类型，应为 TargetType 枚举中的一个值
        """
        self.image = image
        self.target_type = target_type
