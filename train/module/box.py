import json
from module import consts

# 定义一个框类，用于存放框的类型、最顶坐标、最左坐标
class Box:
    def __init__(self, name, type, left, top):
        self.name = name
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
        if self.type == consts.TargetType.TRAIN_NUM:
            return self.top + consts.BOX_H_TRAIN_NUM
        elif self.type == consts.TargetType.LIGHT:
            return self.top + consts.BOX_H_LIGHT
        elif self.type == consts.TargetType.RAIL_LINE:
            return self.top + consts.BOX_H_RAIL_LINE
     # 获取框最右坐标
    def get_right(self):
        if self.type == consts.TargetType.TRAIN_NUM:
            return self.left + consts.BOX_W_TRAIN_NUM
        elif self.type == consts.TargetType.LIGHT:
            return self.left + consts.BOX_W_LIGHT
        elif self.type == consts.TargetType.RAIL_LINE:
            return self.left + consts.BOX_W_RAIL_LINE
        
def read_boxes_from_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            boxes_data = json.load(f)
        boxes = []
        for box_data in boxes_data:
            # 将配置文件中的类型字符串转换为对应的枚举值
            if box_data["type"] == "TRAIN_NUM":
                box_type = consts.TargetType.TRAIN_NUM
            elif box_data["type"] == "LIGHT":
                box_type = consts.TargetType.LIGHT
            elif box_data["type"] == "RAIL_LINE":
                box_type = consts.TargetType.RAIL_LINE
            else:
                print(f"未知的框类型: {box_data['type']}，跳过该框")
                continue
            box = Box(box_data["name"], box_type, int(box_data["left"]), int(box_data["top"]))
            boxes.append(box)
        return boxes
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_path} 不是有效的 JSON 格式")
        return []
