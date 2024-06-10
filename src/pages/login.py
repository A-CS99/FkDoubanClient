from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from components import InputWidget
from store import User, UserError
from utils import router


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.loginSignal.connect(self.update)
            
        title_label = QLabel("登录")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; ")

        submit_button = QPushButton("确认")
        submit_button.setStyleSheet("font-size: 16px; background-color: #0078d4; color: #fff; border: none; border-radius: 5px;")
        submit_button.setFixedHeight(40)
        submit_button.setFixedWidth(100)
        submit_button.clicked.connect(self.submit)
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(submit_button)
        button_widget.setLayout(button_layout)
        

        self.phone_input = InputWidget("手机号", "请输入手机号")
        self.password_input = InputWidget("密码", "请输入密码")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button_widget)        
        self.setLayout(layout)

    def submit(self):
        phone = self.phone_input.get_value()
        password = self.password_input.get_value()
        if phone == "":
            self.phone_input.alert("请输入手机号")
            return
        if password == "":
            self.password_input.alert("请输入密码")
            return
        self.user = User()
        success, res = self.user.login(phone, password)
        if success:
            router.navigate('/')
        else:
            if res == UserError.PHONE_FORMAT_ERROR:
                self.phone_input.alert("手机号格式错误")
            elif res == UserError.PASSWORD_FORMAT_ERROR:
                self.password_input.alert("密码格式错误")
            elif res == UserError.PASSWORD_ERROR:
                self.password_input.alert("用户名或密码错误")
            elif res == UserError.USER_NOT_FOUND:
                self.phone_input.alert("用户不存在")
        self.update()