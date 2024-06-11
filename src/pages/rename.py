from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from components import InputWidget
from store import User, UserError
from utils import router

class RenameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.logChangeSignal.connect(self.update)
            
        title_label = QLabel("修改用户名")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; ")

        submit_button = QPushButton("确认")
        submit_button.setStyleSheet("font-size: 16px; background-color: #0078d4; color: #fff; border: none; border-radius: 5px;")
        submit_button.setCursor(Qt.PointingHandCursor)
        submit_button.setFixedHeight(40)
        submit_button.setFixedWidth(100)
        submit_button.clicked.connect(self.submit)
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(submit_button)
        button_widget.setLayout(button_layout)
        
        self.username_input = InputWidget("用户名", "请输入新用户名")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(button_widget)        
        self.setLayout(layout)

    def submit(self):
        username = self.username_input.get_value()
        if username == "":
            self.username_input.alert("请输入用户名")
            return
        self.user = User()
        success, res = self.user.rename(username)
        if success:
            router.navigate('/user')
        else:
            if res == UserError.USERNAME_FORMAT_ERROR:
                self.username_input.alert("用户名格式错误")
            elif res == UserError.USER_NOT_FOUND:
                self.username_input.alert("用户不存在")
        self.update()