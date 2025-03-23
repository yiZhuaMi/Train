from module import consts

# 定义一个框类，用于存放框的类型、最顶坐标、最左坐标
class Box:
    def __init__(self, type, left, top):
        self.type = type
        self.left = left
        self.top = top
    # 获取框最左坐标
    def get_left(self):
        return self.left
    # 获取框最顶坐标
    def get_top(self):
        return self.top
    # 获取框最底坐标
    def get_bottom(self):
        if self.type == consts.BoxType.TRAIN_NUM:
            return self.top + consts.BOX_H_TRAIN_NUM
        elif self.type == consts.BoxType.LIGHT:
            return self.top + consts.BOX_H_LIGHT
        elif self.type == consts.BoxType.RAIL_LINE:
            return self.top + consts.BOX_H_RAIL_LINE
     # 获取框最右坐标
    def get_right(self):
        if self.type == consts.BoxType.TRAIN_NUM:
            return self.left + consts.BOX_W_TRAIN_NUM
        elif self.type == consts.BoxType.LIGHT:
            return self.left + consts.BOX_W_LIGHT
        elif self.type == consts.BoxType.RAIL_LINE:
            return self.left + consts.BOX_W_RAIL_LINE