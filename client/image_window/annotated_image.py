import numpy as np

from PyQt6.QtCore import QRect

class RectAnnotation:
    '''
        矩形标注框
        x: 矩形左上角水平坐标
        y: 矩形左上角垂直坐标
        w: 矩形的宽度
        h: 矩形的高度
    '''
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_qrect(self) -> QRect:
        return QRect(self.x, self.y, self.w, self.h)

class AnnotatedImage:
    def __init__(self, cv_image: np.ndarray):
        self._cv_image = cv_image

        self.train_num_annotations: list[QRect] = []
    
    def add_train_num_annotations(self, train_num_annos: list[RectAnnotation]):
        for rect_anno in train_num_annos:
            self.train_num_annotations.append(rect_anno.to_qrect())

    def get_cv_image(self) -> np.ndarray:
        return self._cv_image
        