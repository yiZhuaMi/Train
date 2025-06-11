from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QFont, QTextCursor


class WarningWindowView(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("SimSun", 10))
        self.text_edit.setStyleSheet("border: none;")

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def append_warning(self, text: str):
        self.text_edit.append(text)
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        