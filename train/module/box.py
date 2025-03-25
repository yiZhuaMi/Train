import json
from config import config
from module import consts

# 定义一个框类，用于存放框的名称、类型、最左坐标、最顶坐标、识别结果
class Box:
    def __init__(self, name, type, left, top, result=''):
        self.name = name
        self.type = type
        self.left = left
        self.top = top
        self.result = result
    # 获取框最左坐标
    def get_left(self):
        return self.left
    # 获取框最顶坐标
    def get_top(self):
        return self.top
    # 获取框最底坐标
    def get_bottom(self):
        if self.type == consts.TargetType.TEST:
            bottom = consts.BOX_H_TEST*config.BOX_SCALE
        elif self.type == consts.TargetType.TRAIN_NUM:
            bottom = consts.BOX_H_TRAIN_NUM*config.BOX_SCALE
        elif self.type == consts.TargetType.LIGHT:
            bottom = consts.BOX_H_LIGHT*config.BOX_SCALE
        elif self.type == consts.TargetType.RAIL_LINE:
            bottom = consts.BOX_H_RAIL_LINE*config.BOX_SCALE
        return int(self.top + bottom)
     # 获取框最右坐标
    def get_right(self):
        if self.type == consts.TargetType.TEST:
            right = consts.BOX_W_TEST*config.BOX_SCALE
        elif self.type == consts.TargetType.TRAIN_NUM:
            right = consts.BOX_W_TRAIN_NUM*config.BOX_SCALE
        elif self.type == consts.TargetType.LIGHT:
            right = consts.BOX_W_LIGHT*config.BOX_SCALE
        elif self.type == consts.TargetType.RAIL_LINE:
            right = consts.BOX_W_RAIL_LINE*config.BOX_SCALE
        return int(self.left + right)
    # 获取框的识别结果
    def get_result(self):
        return self.result
        
def read_boxes_from_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            boxes_data = json.load(f)
        boxes = []
        for box_data in boxes_data:
            # 将配置文件中的类型字符串转换为对应的枚举值
            if box_data["type"] == "TEST":
                box_type = consts.TargetType.TEST
            elif box_data["type"] == "TRAIN_NUM":
                box_type = consts.TargetType.TRAIN_NUM
            elif box_data["type"] == "LIGHT":
                box_type = consts.TargetType.LIGHT
            elif box_data["type"] == "RAIL_LINE":
                box_type = consts.TargetType.RAIL_LINE
            else:
                print(f"未知的框类型: {box_data['type']}，跳过该框")
                continue
            # 创建 Box 对象并添加到列表中
            box = Box(box_data["name"], 
                      box_type,
                      int(box_data["left"]+config.BOX_OFFSET_left*config.BOX_SCALE), 
                      int(box_data["top"]+config.BOX_OFFSET_top*config.BOX_SCALE))
            boxes.append(box)
        return boxes
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_path} 不是有效的 JSON 格式")
        return []
