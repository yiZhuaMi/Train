from enum import Enum

# 目标类型
class TargetType(Enum):
    TEST = 0
    TRAIN_NUM = 1
    LIGHT = 2
    RAIL_LINE = 3

# 远程窗口缩小倍数
class ReduceTimes(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

# 框尺寸定义

BOX_W_TRAIN_NUM = 120
BOX_H_TRAIN_NUM = 70

# 缩小4次
BOX_W_TEST_4 = 100
BOX_H_TEST_4 = 30
BOX_W_TRAIN_NUM_4 = 90
BOX_H_TRAIN_NUM_4 = 20
BOX_W_LIGHT_4 = 15
BOX_H_LIGHT_4 = 15
BOX_W_RAIL_LINE_4 = 10
BOX_H_RAIL_LINE_4 = 10
# 缩小3次
BOX_W_TEST_3 = 160
BOX_H_TEST_3 = 40
BOX_W_TRAIN_NUM_3 = 120
BOX_H_TRAIN_NUM_3 = 27
BOX_W_LIGHT_3 = 18
BOX_H_LIGHT_3 = 18
BOX_W_RAIL_LINE_3 = 13
BOX_H_RAIL_LINE_3 = 13    
# 缩小2次
BOX_W_TEST_2 = 400
BOX_H_TEST_2 = 120
BOX_W_TRAIN_NUM_2 = 360
BOX_H_TRAIN_NUM_2 = 80
BOX_W_LIGHT_2 = 60
BOX_H_LIGHT_2 = 60
BOX_W_RAIL_LINE_2 = 40
BOX_H_RAIL_LINE_2 = 40
# 缩小1次
BOX_W_TEST_1 = 800
BOX_H_TEST_1 = 240
BOX_W_TRAIN_NUM_1 = 720
BOX_H_TRAIN_NUM_1 = 160
BOX_W_LIGHT_1 = 120
BOX_H_LIGHT_1 = 120
BOX_W_RAIL_LINE_1 = 80
BOX_H_RAIL_LINE_1 = 80

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
SIGNAL_COLOR_RANGES = {
    LightColor.RED: [(0, 100, 100), (10, 255, 255)],  # 红色范围1
    LightColor.RED_2: [(160, 100, 100), (180, 255, 255)],  # 红色范围2
    LightColor.GREEN: [(35, 100, 100), (85, 255, 255)],  # 绿色范围
    LightColor.WHITE: [(0, 0, 200), (180, 50, 255)]  # 白色范围
}

# 轨道线颜色
class RailLineColor(Enum):
    RED = 1
    WHITE = 2
    RED_2 = 3
    GRAY = 4

# 定义颜色范围 (HSV)
RAIL_LINE_COLOR_RANGES = {
    RailLineColor.RED: [(0, 196, 1), (120, 255, 130)],  # 红色范围1
    RailLineColor.WHITE: [(0, 0, 21), (0, 0, 190)],  # 白色范围
    RailLineColor.GRAY: [(0, 80, 1), (118, 255, 108)]  # 灰色范围
}
