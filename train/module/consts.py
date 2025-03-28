from enum import Enum

# 目标类型
class TargetType(Enum):
    TEST = 0
    TRAIN_NUM = 1
    LIGHT = 2
    RAIL_LINE = 3

# 框尺寸定义
BOX_W_TEST = 100
BOX_H_TEST = 30
BOX_W_TRAIN_NUM = 125
BOX_H_TRAIN_NUM = 23
BOX_W_LIGHT = 15
BOX_H_LIGHT = 15
BOX_W_RAIL_LINE = 10
BOX_H_RAIL_LINE = 10

# 框属性定义
BOX_COLOR = "#00f6ff" #十六进制颜色
BOX_WIDTH = 2

# 信号灯颜色
class LightColor(Enum):
    RED = 1
    GREEN = 2
    WHITE = 3
    RED_2 = 4

# 定义颜色范围 (HSV)
COLOR_RANGES = {
    LightColor.RED: [(0, 100, 100), (10, 255, 255)],  # 红色范围1
    LightColor.RED_2: [(160, 100, 100), (180, 255, 255)],  # 红色范围2
    LightColor.GREEN: [(35, 100, 100), (85, 255, 255)],  # 绿色范围
    LightColor.WHITE: [(0, 0, 200), (180, 50, 255)]  # 白色范围
}