from PySide6.QtWidgets import QMenuBar
from utils import router
from store import User
from config import MENU_HEIGHT

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
    def __init__(self):
        super().__init__()
        self.user = User()
        self.user.logChangeSignal.connect(self.onLogChange)
        self.setStyleSheet(menuBar_style)
        self.setFixedHeight(MENU_HEIGHT)
        self.setNativeMenuBar(False)
        self.menuList = {}
        self.menuList["user"] = self.addMenu("用户")
        self.menuList["user"].addAction("登录", self.loginPage)
        self.menuList["user"].addAction("注册", self.signupPage)
        self.menuList["movie"] = self.addAction("影评", self.moviePage)

    def userPage(self):
        router.navigate('/user')

    def loginPage(self):
        router.navigate('/login')

    def signupPage(self):
        router.navigate('/signup')
    
    def moviePage(self):
        router.navigate('/movie')

    def adminPage(self):
        router.navigate('/admin')

    def onLogChange(self):
        if self.user.is_login():
            self.menuList["user"].clear()
            self.menuList["user"].setTitle(self.user.username)
            self.menuList["user"].addAction("个人信息", self.userPage)
            self.menuList["user"].addAction("退出登录", self.user.logout)
            if self.user.is_admin():
                self.menuList["admin"] = self.addAction("后台管理", self.adminPage)
            else:
                if "admin" in self.menuList:
                    self.menuList["admin"].deleteLater()
                    del self.menuList["admin"]
        else:
            self.menuList["user"].clear()
            self.menuList["user"].setTitle("用户")
            self.menuList["user"].addAction("登录", self.loginPage)
            self.menuList["user"].addAction("注册", self.signupPage)
            router.navigate('/login')
        self.update()
