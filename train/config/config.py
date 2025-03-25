import sys

# box配置文件路径
BOX_CONFIG_PATH = "config/boxes.json"
# 要捕获的窗口标题
#Mac下
CAPTURE_MAC_WINDOW_NAME =  "桌面控制 152 576 447 9"
#Win下
CAPTURE_WIN_WINDOW_NAME =  "152 576 447 9"

# box坐标配置偏移
BOX_OFFSET_left = 730
BOX_OFFSET_top = 85
# box尺寸缩放比例
BOX_SCALE = 1.01

# 定义颜色范围 (HSV)
COLOR_RANGES = {
    "red": [(0, 100, 100), (10, 255, 255)],  # 红色范围1
    "red2": [(160, 100, 100), (180, 255, 255)],  # 红色范围2
    "green": [(35, 100, 100), (85, 255, 255)],  # 绿色范围
    "white": [(0, 0, 200), (180, 50, 255)]  # 白色范围
}

# 信号灯的颜色名
LIGHT_COLOR_NAMES = ["red", "green", "white"]

# Window 窗口缩放比
WIN_WINDOW_SCALE_W = 1.5
WIN_WINDOW_SCALE_H = 1.5