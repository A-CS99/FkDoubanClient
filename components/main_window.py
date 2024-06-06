from PySide6.QtWidgets import QMainWindow
from components.menu import MenuBar
from config import SCREEN_SIZE
from views.login import LoginWidget
from views.index import IndexWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(SCREEN_SIZE["width"], SCREEN_SIZE["height"])
        self.menuBar = MenuBar()
        self.menuBar.loginSignal.connect(self.login)
        self.menuBar.movieSignal.connect(self.movie)
        self.setMenuBar(self.menuBar)
        self.setWindowTitle("Python课设-影评管理系统")
        self.setStyleSheet("background-color: #fff;")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def login(self):
        self.setCentralWidget(LoginWidget())

    def movie(self):
        self.setCentralWidget(IndexWidget())
