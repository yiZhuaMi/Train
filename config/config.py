from module import consts
# box配置文件路径
BOX_CONFIG_PATHS = "config/boxes/**/*.json"

# 检测结果文件路径
RESULT_PATH = "output/result.xlsx"

# TDCS画面裁剪区域
TOP_START = 80 #决定原点
TOP_END = 960
LEFT_START = 10 #决定原点
LEFT_END = 4500

# 要捕获的窗口标题
#Mac下
CAPTURE_MAC_WINDOW_NAME =  "桌面控制 152 576 447 9"
#Win下
CAPTURE_WIN_WINDOW_NAME =  "152 576 447 9"

# box坐标配置偏移
BOX_OFFSET_left = 0
BOX_OFFSET_top = 0
# box尺寸缩放比例
BOX_SCALE = 1
# 新增缩放原点配置（默认左上角）
BOX_ORIGIN_LEFT = 0  # 水平方向缩放原点
BOX_ORIGIN_TOP = 0   # 垂直方向缩放原点

# 车次宽高比上限
TRAIN_NUM_WIDTH_HEIGHT_RATIO_UPPER = 4.7
# 车次宽高比下限
TRAIN_NUM_WIDTH_HEIGHT_RATIO_LOWER = 3.9