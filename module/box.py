import json
from config import config
from module import consts

def _get_scaled_cordi(coordi, offset, origin):
    """
    根据缩放原点调整坐标计算
    新公式：((coordi + offset - origin) * scale) + origin
    """
    return int(((coordi + offset - origin) * config.BOX_SCALE) + origin)

def _get_scaled_len(len):
    """
    根据传入的框高度/宽度常量以及缩放系数进行缩放。
    """
    return int(len * config.BOX_SCALE)  # 增加取整保证坐标精度

class Box:
    """
    定义一个Box类，用于表示一个识别框。
    每个Box对象包含以下属性：
    - name: 框的名称
    - type: 框的类型，枚举类型，可选值为TargetType枚举中的值
    - left: 框的最左坐标
    - top: 框的最顶坐标
    - result: 框的识别结果，默认为空字符串
    """
    def __init__(self, name, type, left, top, result=''):
        self.name = name
        self.type = type
        self.left = left
        self.top = top
        self.result = result

    def get_left(self):
        """
        获取框最左坐标
        """
        return self.left
   
    def get_top(self):
        """
        获取框最顶坐标
        """     
        return self.top

    def get_bottom(self):
        """
        获取框最底坐标
        """
        box_height = self.get_height()
        return int(self.top + box_height)
     
    def get_right(self):
        """
        获取框最右坐标
        """
        box_width = self.get_width()
        return int(self.left + box_width)
    
    def get_result(self):
        """
        获取框的识别结果
        """
        return self.result
    
    def get_width(self):
        """
        根据类型和缩放次数获取框的宽度
        """
        width_mapping = {
            consts.TargetType.TRAIN_NUM: consts.BOX_W_TRAIN_NUM,
            consts.TargetType.LIGHT: consts.BOX_W_LIGHT,
            consts.TargetType.RAIL_LINE: consts.BOX_W_RAIL_LINE,
        }
        box_width = width_mapping.get(self.type, 0)
        width = _get_scaled_len(box_width)
        return width

    def get_height(self):
        """
        根据类型和缩放次数获取框的高度
        """
        height_mapping = {
            consts.TargetType.TRAIN_NUM: consts.BOX_H_TRAIN_NUM,
            consts.TargetType.LIGHT: consts.BOX_H_LIGHT,
            consts.TargetType.RAIL_LINE: consts.BOX_H_RAIL_LINE,
        }
        box_height = height_mapping.get(self.type, 0)
        height = _get_scaled_len(box_height)
        return height

def read_boxes_from_config(config_path):
    """
    从配置文件中读取识别框的配置信息，并返回一个包含Box对象的列表。
    """
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
                      _get_scaled_cordi(box_data["left"], config.BOX_OFFSET_left, config.BOX_ORIGIN_LEFT),
                      _get_scaled_cordi(box_data["top"], config.BOX_OFFSET_top, config.BOX_ORIGIN_TOP))
            boxes.append(box)
        return boxes
    except FileNotFoundError:
        print(f"错误: 未找到配置文件 {config_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_path} 不是有效的 JSON 格式")
        return []
