import numpy as np

from PyQt6.QtCore import QRect, QPoint

class RectAnnotation:
    '''
        矩形标注框, 用于标注车次号
        x: 矩形左上角水平坐标
        y: 矩形左上角垂直坐标
        w: 矩形的宽度
        h: 矩形的高度
    '''
    def __init__(self, x: int, y: int, w: int, h: int):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def to_qrect(self) -> QRect:
        return QRect(self._x, self._y, self._w, self._h)

class CircleAnnotation:
    '''
        圆圈标注框， 用于标注信号灯
        x: 圆心水平坐标
        y: 圆心垂直坐标
        r: 半径
    '''
    def __init__(self, x: int, y: int, r: int):
        self._x = x
        self._y = y
        self._r = r
    
    def get_origin(self) -> QPoint:
        return QPoint(self._x, self._y)
    
    def get_radius(self) -> int:
        return self._r

class CrossAnnotation:
    '''
        x标注框， 用于标注股道线
        x: x中心水平坐标
        y: x中心垂直坐标
        r: 半径
    '''
    def __init__(self, x: int, y: int, size: int):
        self._x = x
        self._y = y
        self._size = size
    
    def get_center(self) -> QPoint:
        return QPoint(self._x, self._y)
    
    def get_size(self) -> int:
        return self._size

class AnnotatedImage:
    def __init__(self, cv_image: np.ndarray):
        self._cv_image = cv_image

        self.rect_annotations: list[QRect] = []
        self.circle_annotations: list[CircleAnnotation] = []
        self.cross_annotations: list[CrossAnnotation] = []

    
    def add_rect_annotations(self, rect_annos: list[RectAnnotation]):
        for rect_anno in rect_annos:
            self.rect_annotations.append(rect_anno.to_qrect())

    def add_circle_annotations(self, circle_annos: list[CrossAnnotation]):
        self.circle_annotations.extend(circle_annos)

    def add_cross_annotations(self, cross_annos: list[CrossAnnotation]):
        self.cross_annotations.extend(cross_annos)

    def get_cv_image(self) -> np.ndarray:
        return self._cv_image
        