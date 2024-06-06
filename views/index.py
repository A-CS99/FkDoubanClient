from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class IndexWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("首页")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px;")
        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.setLayout(self.layout)
