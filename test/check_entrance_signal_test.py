import unittest
from unittest.mock import MagicMock, patch
from meta.models import Train, LocationType, SectionType, OccupancyType, Direction, TrackType, SignalStatus, TrainType, LightLine, LightLineType, IndependentSection, Interval, Station, Track, Signal, SignalType, init_interval_dict
from alarm.message import AlarmMsg
from rule.check_entrance_signal import check_interval_signal_over_1

class TestCheckIntervalSignalOver1(unittest.TestCase):
    def setUp(self):
        # 初始化测试数据
        self.trains : list[Train] = [
            Train(
                train_id=1,
                train_number="K123",
                train_type=TrainType.PASSENGER,
                direction=Direction.DOWN,
                red_light_line=LightLine(
                    line_type=LightLineType.RED,
                    sections=[
                        IndependentSection(
                            section_id=1,
                            section_type=SectionType.TRACK,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.STATION,
                            location_id=1,
                        ),
                        IndependentSection(
                            section_id=2,
                            section_type=SectionType.TRACK,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.STATION,
                            location_id=1,
                        )
                    ]
                )
            ),
            Train(
                train_id=2,
                train_number="T456",
                train_type=TrainType.PASSENGER,
                direction=Direction.DOWN,
                red_light_line=LightLine(
                    line_type=LightLineType.RED,
                    sections=[
                        IndependentSection(
                            section_id=3,
                            section_type=SectionType.FIRST_DEPARTURE,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.INTERVAL,
                            location_id=10002,
                        ),
                        IndependentSection(
                            section_id=10001,
                            section_type=SectionType.TRACK,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.STATION,
                            location_id=1,
                        )
                    ]
                )
            ),
            Train(
                train_id=3,
                train_number="Z789",
                train_type=TrainType.PASSENGER,
                direction=Direction.DOWN,
                red_light_line=LightLine(
                    line_type=LightLineType.RED,
                    sections=[
                        IndependentSection(
                            section_id=3,
                            section_type=SectionType.FIRST_DEPARTURE,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.INTERVAL,
                            location_id=10001,
                        ),
                        IndependentSection(
                            section_id=10001,
                            section_type=SectionType.TRACK,
                            occupancy_type=OccupancyType.RED,
                            location=LocationType.STATION,
                            location_id=1,
                        )
                    ]
                )
            )
        ]
        Intervals : list[Interval] = [
            Interval(
                interval_id=10001,
                up_station=Station(
                    station_id=1,
                    name="测试车站1",
                    tracks=[
                        Track(
                            track_id=1,
                            track_number=1,
                            track_type=TrackType.MAIN,
                            station=1,
                            direction=Direction.DOWN
                        ),
                        Track(
                            track_id=2,
                            track_number=3,
                            track_type=TrackType.SIDE,
                            station=1,
                            direction=Direction.DOWN
                        )
                    ],
                    entrance_signal=Signal(
                        signal_id=1,
                        signal_type=SignalType.ENTRANCE,
                        status=SignalStatus.OPEN
                    ),
                    exit_signal=Signal(
                        signal_id=2,
                        signal_type=SignalType.EXIT,
                        status=SignalStatus.CLOSED
                    ),
                ),
                down_station=Station(
                    station_id=2,
                    name="测试车站2",
                    tracks=[
                        Track(
                            track_id=3,
                            track_number=1,
                            track_type=TrackType.MAIN,
                            station=2,
                            direction=Direction.DOWN
                        ),
                        Track(
                            track_id=4,
                            track_number=3,
                            track_type=TrackType.SIDE,
                            station=2,
                            direction=Direction.DOWN
                        )
                    ],
                    entrance_signal=Signal(
                        signal_id=3,
                        signal_type=SignalType.ENTRANCE,
                        status=SignalStatus.CLOSED
                    ),
                    exit_signal=Signal(
                        signal_id=4,
                        signal_type=SignalType.EXIT,
                        status=SignalStatus.CLOSED
                    ),
                ),
                sections=[
                    IndependentSection(
                        section_id=3,
                        section_type=SectionType.FIRST_DEPARTURE,
                        occupancy_type=OccupancyType.RED,
                        location=LocationType.INTERVAL,
                        location_id=10001
                    ),
                    IndependentSection(
                        section_id=4,
                        section_type=SectionType.SECOND_DEPARTURE,
                        occupancy_type=OccupancyType.FREE,
                        location=LocationType.INTERVAL,
                        location_id=10001,
                    ),
                    IndependentSection(
                        section_id=5,
                        section_type=SectionType.OTHER,
                        occupancy_type=OccupancyType.FREE,
                        location=LocationType.INTERVAL,
                        location_id=10001,
                    ),
                    IndependentSection(
                        section_id=6,
                        section_type=SectionType.OTHER,
                        occupancy_type=OccupancyType.FREE,
                        location=LocationType.INTERVAL,
                        location_id=10001,
                    )
                ],
                signals=[
                    Signal(
                        signal_id=5,
                        signal_type=SignalType.SECTION_SIGNAL, 
                        status=SignalStatus.OPEN,
                    ),
                    Signal(
                        signal_id=6,
                        signal_type=SignalType.SECTION_SIGNAL, 
                        status=SignalStatus.OPEN,
                    ),
                    Signal(
                        signal_id=7,
                        signal_type=SignalType.SECTION_SIGNAL, 
                        status=SignalStatus.OPEN,
                    ),
                ]
            )
        ]
        init_interval_dict(Intervals)

    def test_no_occupied_interval(self):
        """测试列车未占用任何区间"""
        result = check_interval_signal_over_1(self.trains)
        self.assertEqual(len(result), 1)

    # def test_invalid_interval_id(self):
    #     """测试无效区间ID"""
    #     self.train.red_light_line.sections = [self.section]
    #     global IntervalDict
    #     IntervalDict = {}
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_less_than_two_signals(self):
    #     """测试区间信号机不足两架"""
    #     self.interval.signals = [MagicMock()]
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_in_first_departure(self):
    #     """测试列车处于第一离去"""
    #     self.section.section_type = SectionType.FIRST_DEPARTURE
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_red_light_occupied(self):
    #     """测试区间红光带被占用"""
    #     self.section.section_type = SectionType.NORMAL
    #     self.interval.sections[0].occupancy_type = OccupancyType.RED
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_no_main_track(self):
    #     """测试前方车站无接车进路"""
    #     self.station.tracks = []
    #     self.interval.up_station = self.station
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_track_not_white_occupied(self):
    #     """测试前方车站接车进路非空闲"""
    #     self.track.sections[0].occupancy_type = OccupancyType.RED
    #     self.interval.up_station = self.station
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

    # def test_signal_closed(self):
    #     """测试进站信号灯未开放"""
    #     self.section.section_type = SectionType.NORMAL
    #     self.interval.sections[0].occupancy_type = OccupancyType.WHITE
    #     self.interval.up_station = self.station
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0].train_number, "T123")
    #     self.assertIn("前方车站进站信号灯未开放", result[0].message)

    # def test_signal_open(self):
    #     """测试进站信号灯开放"""
    #     self.station.entrance_signal.status = SignalStatus.OPEN
    #     self.section.section_type = SectionType.NORMAL
    #     self.interval.sections[0].occupancy_type = OccupancyType.WHITE
    #     self.interval.up_station = self.station
    #     self.train.red_light_line.sections = [self.section]
    #     result = check_interval_signal_over_1([self.train])
    #     self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()