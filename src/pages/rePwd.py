from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from components import InputWidget
from store import User, UserError
from utils import router


class RePwdWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.logChangeSignal.connect(self.update)
            
        title_label = QLabel("修改密码")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; ")

        tip_label = QLabel("注意：修改密码后需要重新登录")
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setStyleSheet("font-size: 16px; color: #4d5156; ")

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
        
        self.old_pwd_input = InputWidget("原密码", "请输入原密码")
        self.new_pwd_input = InputWidget("新密码", "请输入新密码")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(tip_label)
        layout.addWidget(self.old_pwd_input)
        layout.addWidget(self.new_pwd_input)
        layout.addWidget(button_widget)        
        self.setLayout(layout)

    def submit(self):
        old_pwd = self.old_pwd_input.get_value()
        new_pwd = self.new_pwd_input.get_value()
        if old_pwd == "":
            self.old_pwd_input.alert("请输入原密码")
            return
        if new_pwd == "":
            self.new_pwd_input.alert("请输入新密码")
            return
        self.user = User()
        success, res = self.user.change_password(old_pwd, new_pwd)
        if success:
            router.navigate('/login')
        else:
            if res == UserError.PASSWORD_FORMAT_ERROR:
                self.new_pwd_input.alert("密码格式错误")
            elif res == UserError.PASSWORD_ERROR:
                self.old_pwd_input.alert("原密码错误")
            elif res == UserError.USER_NOT_FOUND:
                self.old_pwd_input.alert("用户不存在")
        self.update()