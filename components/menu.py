from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal

menuBar_style = """
    QMenuBar {
        background-color: #fff;
        font-size: 16px;
    }
    QMenu {
        background-color: #fff;
        font-size: 16px;
    }
    QMenu::item {
        background-color: #fff;
    }
    QMenu::item:selected {
        color: #000;
        background-color: #ccc;
    }
"""

class MenuBar(QMenuBar):
    loginSignal = Signal()
    signupSignal = Signal()
    movieSignal = Signal()
    settingSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(menuBar_style)
        self.setFixedHeight(60)
        self.setNativeMenuBar(False)
        self.menuList = {}
        self.menuList["user"] = self.addMenu("用户")
        self.menuList["user"].addAction("登录", self.login)
        self.menuList["user"].addAction("注册", self.signup)
        self.menuList["movie"] = self.addAction("影评", self.movie)
        self.menuList["setting"] = self.addAction("设置", self.setting)

    def login(self):
        self.loginSignal.emit()

    def signup(self):
        self.signupSignal.emit()
    
    def movie(self):
        self.movieSignal.emit()
    
    def setting(self):
        self.settingSignal.emit()
