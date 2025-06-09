import numpy as np
import cv2
from PyQt6.QtGui import QImage, QPixmap

from .image_model import ImageModel
from .image_view import ImageView


class ImageController:
    def __init__(self, model: ImageModel, view: ImageView):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def load_image(self, image_array: np.ndarray):
        self.model.set_image(image_array)
        self.update_image()

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

    def get_view(self) -> ImageView:
        return self.view

def construct_image_controller() -> ImageController:
    model = ImageModel()
    view = ImageView()
    return ImageController(model, view)
