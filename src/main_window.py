from PySide6.QtWidgets import QMainWindow
from components import MenuBar
from config import SCREEN_SIZE
from store import User
from utils import router
from pages import IndexWidget, LoginWidget, SignupWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.resize(SCREEN_SIZE["width"], SCREEN_SIZE["height"])
        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)
        self.setWindowTitle("Python课设-影评管理系统")
        self.setStyleSheet("background-color: #fff;")
        router.bind_routes({
            '/': IndexWidget,
            '/login': LoginWidget,
            '/signup': SignupWidget,
            '/movie': IndexWidget
        })
        router.navigateSignal.connect(self.onNavigate)
        if self.user.is_login():
            router.navigate('/movie')
        else:
            router.navigate('/login')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def onNavigate(self):
        self.setCentralWidget(router.get_cur_page())
        self.update()
