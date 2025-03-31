from module import consts
# box配置文件路径
BOX_CONFIG_PATH = "config/boxes3x.json"

# 检测结果文件路径
RESULT_PATH = "output/result.xlsx"

# 要捕获的窗口标题
#Mac下
CAPTURE_MAC_WINDOW_NAME =  "桌面控制 152 576 447 9"
#Win下
CAPTURE_WIN_WINDOW_NAME =  "152 576 447 9"

# 远程窗口缩小倍数
REDUCE_TIMES = consts.ReduceTimes.THREE

# box坐标配置偏移
BOX_OFFSET_left = 0
BOX_OFFSET_top = 0
# box尺寸缩放比例
BOX_SCALE = 1
# 新增缩放原点配置（默认左上角）
BOX_ORIGIN_LEFT = 15  # 水平方向缩放原点
BOX_ORIGIN_TOP = 305   # 垂直方向缩放原点

# Window 窗口缩放比
WIN_WINDOW_SCALE_W = 1.5
WIN_WINDOW_SCALE_H = 1.5