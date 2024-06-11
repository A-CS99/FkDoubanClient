from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from components import InputWidget
from store import User, UserError
from utils import router

class SignupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.logChangeSignal.connect(self.update)
            
        title_label = QLabel("注册")
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
        
        self.user_input = InputWidget("用户名", "请输入用户名")
        self.phone_input = InputWidget("手机号", "请输入手机号")
        self.password_input = InputWidget("密码", "请输入密码")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button_widget)        
        self.setLayout(layout)

    def submit(self):
        user_name = self.user_input.get_value()
        phone = self.phone_input.get_value()
        password = self.password_input.get_value()
        if user_name == "":
            self.user_input.alert("请输入用户名")
            return
        if phone == "":
            self.phone_input.alert("请输入手机号")
            return
        if password == "":
            self.password_input.alert("请输入密码")
            return
        self.user = User()
        success, res = self.user.register(user_name, phone, password)
        if success:
            router.navigate('/login')
        else:
            if res == UserError.USERNAME_FORMAT_ERROR:
                self.user_input.alert("用户名格式错误")
            elif res == UserError.PHONE_FORMAT_ERROR:
                self.phone_input.alert("手机号格式错误")
            elif res == UserError.PASSWORD_FORMAT_ERROR:
                self.password_input.alert("密码格式错误")
            elif res == UserError.USER_EXIST:
                self.user_input.alert("用户名已存在")
        self.update()