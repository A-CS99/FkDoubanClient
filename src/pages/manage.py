from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QPushButton, QDialog
from PySide6.QtCore import Qt
from config import SCREEN_SIZE, MENU_HEIGHT
from store import MovieList, User
from utils import router

HEADER_HEIGHT = 70
CONTENT_HEIGHT = SCREEN_SIZE["height"] - MENU_HEIGHT - HEADER_HEIGHT - 120

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(HEADER_HEIGHT)
        layout = QHBoxLayout()
        self.setLayout(layout)

        left_label = QLabel('用户管理')
        left_label.setAlignment(Qt.AlignLeft)
        left_label.setStyleSheet('font-size: 32px; font-weight: bold; margin-left: 10px; margin-bottom: 5px;')

        right_label = QLabel('欢迎您，管理员！')
        right_label.setAlignment(Qt.AlignRight)
        right_label.setStyleSheet('font-size: 32px; font-weight: bold; margin-left: 10px; margin-bottom: 5px;')

        layout.addWidget(left_label)
        layout.addWidget(right_label)

class ConfirmDialog(QDialog):
    def __init__(self, message, onConfirm):
        super().__init__()
        self.setFixedSize(300, 150)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(message)
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 20px; margin-top: 20px; margin-bottom: 20px;')
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        cancel_button = QPushButton('取消')
        cancel_button.setFixedWidth(100)
        cancel_button.setStyleSheet('font-size: 16px; color: #00f; border: 0; background-color: #fff; ')
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.close)
        confirm_button = QPushButton('确定')
        confirm_button.setFixedWidth(100)
        confirm_button.setStyleSheet('font-size: 16px; color: #f00; border: 0; background-color: #fff; ')
        confirm_button.setCursor(Qt.PointingHandCursor)
        def onConfirmClick():
            onConfirm()
            self.close()
        confirm_button.clicked.connect(onConfirmClick)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)

class UserWidget(QWidget):
    def __init__(self, user_info):
        super().__init__()
        self.user = User()
        self.user_info = user_info
        self.setFixedWidth(SCREEN_SIZE['width'] - 20)
        self.setFixedHeight(100)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        id_label = QLabel(f'{user_info["id"]}')
        id_label.setFixedWidth(100)
        id_label.setStyleSheet('font-size: 16px; margin-left: 10px;')
        name_label = QLabel(user_info['username'])
        name_label.setFixedWidth(200)
        name_label.setStyleSheet('font-size: 24px; font-weight: bold; margin-left: 10px;')
        role_label = QLabel()
        role_label.setFixedSize(100, 30)
        role_label.setAlignment(Qt.AlignCenter)
        role_style = 'font-size: 16px; font-weight: bold; color: #fff; margin-left: 10px; padding: 5px; border-radius: 15px;'
        if user_info['isAdmin']:
            role_label.setText('管理员')
            role_label.setStyleSheet(f'{role_style} background-color: #f00;')
        else:
            role_label.setText('用户')
            role_label.setStyleSheet(f'{role_style} background-color: #00f;')
        role_label.setFixedWidth(100)

        buttons_widget = QWidget()
        buttons_widget.setFixedWidth(500)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_layout.setSpacing(10)
        buttons_widget.setLayout(buttons_layout)

        delete_button = QPushButton("删除用户")
        delete_button.setStyleSheet("font-size: 16px; color: #f00; border: 0; background-color: #fff; ")
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.clicked.connect(self.onDelete)
        if not user_info['isAdmin']:
            upgrate_button = QPushButton("设为管理员")
            upgrate_button.setStyleSheet("font-size: 16px; color: #00f; border: 0; background-color: #fff; ")
            upgrate_button.setCursor(Qt.PointingHandCursor)
            upgrate_button.clicked.connect(self.onUpgrate)
            buttons_layout.addWidget(upgrate_button)
        buttons_layout.addWidget(delete_button)

        layout.addWidget(id_label)
        layout.addWidget(name_label)
        layout.addWidget(role_label)
        layout.addWidget(buttons_widget)
        self.setLayout(layout)
    
    def onDelete(self):
        dialog = ConfirmDialog('确定删除该用户吗？', self.onDeleteConfirm)
        dialog.exec()

    def onDeleteConfirm(self):
        self.user.delete_user(self.user_info['id'])
        router.navigate('/admin')

    def onUpgrate(self):
        dialog = ConfirmDialog('确定将该用户设为管理员吗？', self.onUpgrateConfirm)
        dialog.exec()

    def onUpgrateConfirm(self):
        self.user.add_admin(self.user_info['id'])
        router.navigate('/admin')

class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.movie_list = MovieList()
        self.setFixedHeight(CONTENT_HEIGHT)
        
        self.user = User()
        if not self.user.is_admin():
            router.navigate('/')
            return
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(CONTENT_HEIGHT)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget = QWidget()
        self.list_layout = QVBoxLayout()
        self.list_layout.setAlignment(Qt.AlignTop)
        list_widget.setLayout(self.list_layout)
        self.scroll_area.setWidget(list_widget)

        self.init_user_list()

        layout.addWidget(self.scroll_area)

    def init_user_list(self):
        success, users = self.user.get_all_users()
        if not success:
            return
        for user in users:
            user_widget = UserWidget(user)
            self.list_layout.addWidget(user_widget)

class Divider(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(1)
        self.setStyleSheet('background-color: #ccc;')

class ManageWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(HeaderWidget())
        layout.addWidget(Divider())
        layout.addWidget(ContentWidget())
        self.setLayout(layout)
