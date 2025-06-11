import numpy as np
import cv2
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt

from .image_model import ImageModel
from .image_view import ImageView
from .annotated_image import AnnotatedImage


class ImageController:
    def __init__(self, model: ImageModel, view: ImageView):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def load_image(self, image_array: np.ndarray):
        self.model.set_image(image_array)
        self.update_image()

    def load_annotated_image(self, image_annotated: AnnotatedImage):
        self.model.set_annoteted_image(image_annotated)
        self.update_annotated_image()

    def update_image(self):
        image_array = self.model.get_image()
        if(image_array is None):
            return
        
        image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w

        q_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.view.display_image(pixmap)

    def update_annotated_image(self):
        annotated_image = self.model.get_annotated_image()
        if(annotated_image is None):
            return
        
        image_rgb = cv2.cvtColor(annotated_image.get_cv_image(), cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w

        q_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        painter = QPainter(q_image)
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(2)
        painter.setPen(pen)

        # 绘制矩形标注
        for q_rect in annotated_image.rect_annotations:
            painter.drawRect(q_rect)

        # 绘制圆圈标注
        for circle_anno in annotated_image.circle_annotations:
            painter.drawEllipse(circle_anno.get_origin(), circle_anno.get_radius(), circle_anno.get_radius())

        # 绘制x标注
        for cross_anno in annotated_image.cross_annotations:
            center = cross_anno.get_center()
            size = cross_anno.get_size()
            painter.drawLine(center.x() - size, center.y() - size, center.x() + size, center.y() + size)
            painter.drawLine(center.x() - size, center.y() + size, center.x() + size, center.y() - size)

        painter.end()

        pixmap = QPixmap.fromImage(q_image)
        self.view.display_image(pixmap)

    def get_view(self) -> ImageView:
        return self.view


_model = ImageModel()
_view = ImageView()
image_controller = ImageController(_model, _view)

