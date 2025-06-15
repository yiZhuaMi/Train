from enum import Enum
from typing import Dict
from dataclasses import dataclass, field

class SectionType(Enum):
    """区间类型枚举"""
    TRACK = "股道"
    FIRST_DEPARTURE = "第一离去"
    SECOND_DEPARTURE = "第二离去"
    FIRST_APPROACH = "第一接近"
    SECOND_APPROACH = "第二接近"
    OTHER = "其他"

class OccupancyType(Enum):
    """占用类型枚举"""
    RED = "红光带占用"
    WHITE = "白光带占用"
    FREE = "空闲"

class LocationType(Enum):
    """所属位置枚举"""
    INTERVAL = "区间"
    STATION = "车站"

class TrainType(Enum):
    """列车类型枚举"""
    PASSENGER = "客车"
    BULLET = "动车"
    FREIGHT = "货车"

class Direction(Enum):
    """运行方向枚举"""
    UP = "上行"
    DOWN = "下行"

class LightLineType(Enum):
    """光带类型枚举"""
    RED = "红"
    WHITE = "白"

class TrackType(Enum):
    """股道类型枚举"""
    MAIN = "接车正线"
    SIDE = "侧线"

class SignalType(Enum):
    """信号机类型枚举"""
    ENTRANCE = "进站信号机"
    EXIT = "出站信号机"
    SECTION_SIGNAL = "区间信号机"

class SignalStatus(Enum):
    """信号机状态枚举"""
    OPEN = "开放"
    CLOSED = "关闭"

# 独立小节
@dataclass
class IndependentSection:
    section_id: int                # 小节编号
    section_type: SectionType      # 小节类型
    occupancy_type: OccupancyType  # 占用类型
    location: LocationType         # 所属位置
    location_id: int # 所在区间或者车站编号


# 光带
@dataclass
class LightLine:
    line_type: LightLineType # 光带类型
    sections: list[IndependentSection] = field(default_factory=list)  # 独立小节集合

# 列车
@dataclass
class Train:
    train_id: int # 车辆编号
    train_number: str               # 车次号
    train_type: TrainType          # 列车类型
    direction: Direction           # 运行方向
    red_light_line: LightLine # 列车红光带

# 股道
@dataclass
class Track:
    track_id: int                 # 股道编号（唯一标识）
    track_number: int             # 股道号（显示用编号）
    station: int            # 所属车站的编号
    direction: Direction          # 方向
    track_type: TrackType         # 股道类型
    sections: list[IndependentSection] = field(default_factory=list) # 股道包含独立小节的有序集合

# 信号机
@dataclass
class Signal:
    signal_id: int # 编号
    signal_type: SignalType # 信号机类型
    status: SignalStatus # 信号机状态

# 车站
@dataclass
class Station:
    station_id: int # 车站编号
    name: str # 车站名称
    entrance_signal: Signal # 进站信号机
    exit_signal: Signal # 出站信号机
    tracks: list[Track] = field(default_factory=list) # 车站内股道集合

# 区间
@dataclass
class Interval:
    interval_id : int # 区间编号
    up_station: Station # 上行车站
    down_station: Station # 下行车站
    sections: list[IndependentSection] = field(default_factory=list) # 区间包含独立小节的有序集合
    signals: list[Signal] = field(default_factory=list) # 区间包含的信号机集合

IntervalDict: Dict[int, Interval] = {}

def init_interval_dict(intervals: list[Interval]):
    """初始化全局区间集合"""
    global IntervalDict
    IntervalDict = {interval.interval_id: interval for interval in intervals}

def get_interval_dict() -> Dict[int, Interval]:
    return IntervalDict
