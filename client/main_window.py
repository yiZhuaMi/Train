from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

import os
import cv2
import sys

from image_window.image_controller import construct_image_controller

class MainWindow(QMainWindow):
    def __init__(self, folder_path: str):
        super().__init__()
        self.setWindowTitle("控制中心")
        self.resize(1000, 700)

        # 设置工具栏（可添加动作）
        toolbar = QToolBar("工具栏")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # 示例：添加一个动作按钮
        example_action = QAction("示例操作", self)
        toolbar.addAction(example_action)

        self.image_controller = construct_image_controller()

        # 添加视图（图像显示）为中心组件
        container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.image_controller.get_view())  # 未来可以添加更多控件到 layout 左右
        container.setLayout(layout)

        self.setCentralWidget(container)

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
        self.image_controller.load_image(cv_image)

        self.current_index = (self.current_index + 1) % len(self.image_files)

    def run(self):
        self._show_next_image()
        self.show()



def client_main():
    app = QApplication(sys.argv)

    window = MainWindow("./images_for_test")
    window.run()

    sys.exit(app.exec())

def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("测试窗口")
    window.resize(400, 300)

    label = QLabel("你好 PyQt6", window)
    label.setGeometry(100, 100, 200, 50)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    client_main()
