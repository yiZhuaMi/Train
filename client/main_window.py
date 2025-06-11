from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

from image_window.annotated_image import AnnotatedImage, RectAnnotation

import os
import cv2
import sys



class MainWindow(QMainWindow):
    def __init__(self, folder_path: str):
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

        self.image_folder = folder_path
        self.image_files = [f for f in os.listdir(folder_path)
                            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))]
        self.image_files.sort()  # 可选：按文件名排序
        self.current_index = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._show_next_image)
        self.timer.start(1000)

    def _show_next_image(self):
        if not self.image_files:
            return

        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
        cv_image = cv2.imread(image_path)
        image_annotated = AnnotatedImage(cv_image)
        image_annotated.add_train_num_annotations([RectAnnotation(500, 350, 50, 50)])
        self._image_controller.load_annotated_image(image_annotated)

        self.current_index = (self.current_index + 1) % len(self.image_files)
        print(image_path)
        self._warning_window_controller.append_warning(image_path)

    def run(self):
        self.show()
        self._show_next_image()



def client_main():
    app = QApplication(sys.argv)

    window = MainWindow("./images_for_test")
    window.run()

    sys.exit(app.exec())

if __name__ == "__main__":
    client_main()
