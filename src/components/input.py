from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt

class InputWidget(QWidget):
    def __init__(self, label, placeholder):
        super().__init__()
        self.placeholder = placeholder
        self.setStyleSheet("font-size: 16px;")
        input_label = QLabel(label)
        input_label.setAlignment(Qt.AlignRight)
        input_label.setFixedHeight(20)
        input_label.setFixedWidth(100)

        self.input_edit = QLineEdit()
        self.input_edit.setFixedHeight(30)
        self.input_edit.setFixedWidth(300)
        self.input_edit.setAlignment(Qt.AlignLeft)
        self.input_edit.setPlaceholderText(placeholder)
        self.input_edit.focusInEvent = self._onFocusIn
        self.input_edit.focusOutEvent = self._onFocusOut

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(input_label)
        layout.addWidget(self.input_edit)
        widget.setLayout(layout)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.setLayout(layout)

    def get_value(self):
        return self.input_edit.text()
    
    def alert(self, message=""):
        self.input_edit.setStyleSheet("border: 1px solid red;")
        self.input_edit.setText(message)

    def _onFocusIn(self, event):
        self.input_edit.setStyleSheet("color: #000; border: 0.5px solid #e6e6e6; border-bottom: 0.5px solid #0078d4;")
        self.input_edit.setText("")

    def _onFocusOut(self, event):
        self.input_edit.setStyleSheet("border: 1px solid #e6e6e6; color: #ccc;")