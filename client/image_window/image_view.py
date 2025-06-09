from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageView(QWidget):
    def __init__(self):
        super().__init__()
        self.image_label = QLabel("图像未加载")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
    
    def display_image(self, pixmap: QPixmap):
        if pixmap.isNull():
            self.image_label.setText("图像为空")
        else:
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation    
                )
            )
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.controller:
            self.controller.update_image()