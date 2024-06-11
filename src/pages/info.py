from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from store import User
from utils import router

# 用户信息页面
class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.logChangeSignal.connect(self.update)
        secret_phone = self.user.phone[:3] + "****" + self.user.phone[7:]
        title_label = QLabel("个人信息")
        title_label.setStyleSheet("font-size: 64px; ")

        divider_line = QLabel()
        divider_line.setFixedHeight(2)
        divider_line.setStyleSheet("background-color: #ccc; max-width: 800px;")

        user_widget = QWidget()
        user_label = QLabel(f"用户名：{self.user.username}")
        user_label.setAlignment(Qt.AlignLeft)
        user_label.setStyleSheet("font-size: 24px; color: #4d5156;")
        user_renameBtn = QPushButton("修改用户名")
        user_renameBtn.setStyleSheet("font-size: 16px; color: #0078d4; border: 0; background-color: #fff; ")
        user_renameBtn.setCursor(Qt.PointingHandCursor)
        user_renameBtn.clicked.connect(self.onRename)
        user_layout = QHBoxLayout()
        user_layout.setAlignment(Qt.AlignLeft)
        user_layout.setSpacing(20)
        user_layout.addWidget(user_label)
        user_layout.addWidget(user_renameBtn)
        user_widget.setLayout(user_layout)

        phone_widget = QWidget()
        phone_label = QLabel(f"手机号：{secret_phone}")
        phone_label.setAlignment(Qt.AlignLeft)
        phone_label.setStyleSheet("font-size: 24px; color: #4d5156;")
        phone_layout = QHBoxLayout()
        phone_layout.setAlignment(Qt.AlignLeft)
        phone_layout.setSpacing(20)
        phone_layout.addWidget(phone_label)
        phone_widget.setLayout(phone_layout)

        pwd_widget = QWidget()
        pwd_label = QLabel("密码：********")
        pwd_label.setAlignment(Qt.AlignLeft)
        pwd_label.setStyleSheet("font-size: 24px; color: #4d5156;")
        rePwd_button = QPushButton("修改密码")
        rePwd_button.setStyleSheet("font-size: 16px; color: #0078d4; border: 0; background-color: #fff; ")
        rePwd_button.setCursor(Qt.PointingHandCursor)
        rePwd_button.clicked.connect(self.onRePwd)
        pwd_layout = QHBoxLayout()
        pwd_layout.setAlignment(Qt.AlignLeft)
        pwd_layout.setSpacing(20)
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(rePwd_button)
        pwd_widget.setLayout(pwd_layout)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.addWidget(title_label)
        layout.addWidget(divider_line)
        layout.addWidget(user_widget)
        layout.addWidget(phone_widget)
        layout.addWidget(pwd_widget)
        self.setStyleSheet("margin: 20px;")
        self.setLayout(layout)
        self.update()

    def onRename(self):
        router.navigate('/rename')

    def onRePwd(self):
        router.navigate('/rePwd')
