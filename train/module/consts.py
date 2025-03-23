from enum import Enum

# 框类型
class BoxType(Enum):
    TRAIN_NUM = 1
    LIGHT = 2
    RAIL_LINE = 3

# 框尺寸定义
BOX_W_TRAIN_NUM = 125
BOX_H_TRAIN_NUM = 25
BOX_W_LIGHT = 10
BOX_H_LIGHT = 10
BOX_W_RAIL_LINE = 3
BOX_H_RAIL_LINE = 3

