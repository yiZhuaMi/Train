from meta.models import Train, LocationType, SectionType, OccupancyType, Direction, TrackType, SignalStatus
from meta.models import get_interval_dict
from alarm.message import AlarmMsg


def check_interval_signal_over_1(trains: list[Train]) -> list[AlarmMsg]:
    AlarmMsgList: list[AlarmMsg] = []
    for train in trains:
        # 获取红光带所有独立小节
        sections = train.red_light_line.sections
        
        interval_id = 0
        in_first_departure = False
        in_first_departure_section_id = 0
        for section in sections:
            if section.location != LocationType.INTERVAL:
                # 不在区间的列车该报警检测可忽略
                continue
            interval_id = section.location_id
            if section.section_type == SectionType.FIRST_DEPARTURE:
                in_first_departure = True
                in_first_departure_section_id = section.section_id
                break
            
        if interval_id == 0:
            print(f"列车 {train.train_number} 未占用任何区间\n")
            continue
        
        # 添加空值检查
        IntervalDict = get_interval_dict()
        if interval_id not in IntervalDict or not IntervalDict[interval_id]:
            print(f"列车 {train.train_number} 关联无效区间 ID: {interval_id}\n")
            continue
        interval = IntervalDict[interval_id]

        # 检查区间是否有两架及以上信号机
        if len(interval.signals) < 2:
            print(f"列车 {train.train_number} 占用区间 {interval.interval_id} 信号机不足两架\n")
            continue

        if not in_first_departure:
            # 检测列车是否在第一离去
            print(f"列车 {train.train_number} 未处于第一离去\n")
            continue

        # 检查区间小节是否均被红光带占用
        is_red_occ = False
        for section in interval.sections:
            # 需要排除当前车辆的红光带
            if section.section_id == in_first_departure_section_id:
                continue
            if section.occupancy_type == OccupancyType.RED:
                print(f"列车 {train.train_number} 占用区间 {interval.interval_id} 红光带 {section.section_id} 已被占用\n")
                is_red_occ = True
                break
        if is_red_occ:
            continue
        
        station = interval.down_station
        if train.direction == Direction.UP:
            station = interval.up_station
        # 检查前方车站接车进路是否空闲（均被白光带占用）
        main_track = None
        for track in station.tracks:
            if track.track_type == TrackType.MAIN and track.direction == train.direction:
                main_track = track
        if main_track == None:
            print(f"列车 {train.train_number} 占用区间 {interval.interval_id} 前方车站接车进路未找到\n")
            continue

        is_white_occ = True
        for section in main_track.sections:
            if section.occupancy_type != OccupancyType.WHITE:
                print(f"列车 {train.train_number} 占用区间 {interval.interval_id} 前方车站接车进路非空闲\n")
                is_white_occ = False
        if not is_white_occ:
            continue

        # 判断进站信号灯是否开放
        if station.entrance_signal.status == SignalStatus.CLOSED:
            print(f"列车 {train.train_number} 占用区间 {interval.interval_id} 前方车站进站信号灯未开放\n")
            # 需要报警
            # TODO 增加报警信息的返回
            alarm_msg = AlarmMsg(train.train_number, f"列车 {train.train_number} 占用区间 {interval.interval_id} 前方车站进站信号灯未开放")
            AlarmMsgList.append(alarm_msg)

    print(AlarmMsgList)
    return AlarmMsgList
