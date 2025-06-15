from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

from image_window.annotated_image import AnnotatedImage, RectAnnotation, CircleAnnotation, CrossAnnotation

import os
import cv2
import sys



class MainWindow(QMainWindow):
    def __init__(self, video_path: str):
        super().__init__()
        from image_window.image_controller import image_controller
        from warning_window.warning_window_controller import warning_window_controller

        self._image_controller = image_controller
        self._warning_window_controller = warning_window_controller

        self.setWindowTitle("控制中心")
        self.resize(1000, 700)

        # 设置工具栏（可添加动作）
        toolbar = QToolBar("工具栏")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # 示例：添加一个动作按钮
        example_action = QAction("示例操作", self)
        toolbar.addAction(example_action)

        

        # 添加视图为中心组件
        h_container = QWidget()
        layout_h = QHBoxLayout()
        v_container = QWidget()
        layout_v = QVBoxLayout()
        layout_v.addWidget(self._image_controller.get_view())  
        layout_v.addWidget(self._warning_window_controller.get_view())
        v_container.setLayout(layout_v)
        layout_h.addWidget(v_container)
        h_container.setLayout(layout_h)

        self.setCentralWidget(h_container)

        self.video_cap = cv2.VideoCapture(video_path)
        if self.video_cap.isOpened:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self._show_next_image)
            self.timer.start(1000)

        self.index = 0

    def _show_next_image(self):
        if not self.video_cap.isOpened:
            return

        ret, frame = self.video_cap.read()
        if not ret:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.index = 0

        image_annotated = AnnotatedImage(frame)
        image_annotated.add_rect_annotations([RectAnnotation(500, 350, 50, 50)])
        image_annotated.add_circle_annotations([CircleAnnotation(1000, 1000, 10)])
        image_annotated.add_cross_annotations([CrossAnnotation(1200, 800, 10)])
        self._image_controller.load_annotated_image(image_annotated)

        self._warning_window_controller.append_warning(f"读取到了视频第{self.index}帧")
        self.index += 1

    def run(self):
        self.show()
        self._show_next_image()



def client_main():
    app = QApplication(sys.argv)

    window = MainWindow("./images_for_test/video.mp4")
    window.run()

    sys.exit(app.exec())

if __name__ == "__main__":
    client_main()
