from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from config import SCREEN_SIZE, MENU_HEIGHT
from store import MovieList, User
from components import CardWidget

HEADER_HEIGHT = 70
FOOTER_HEIGHT = 50
CONTENT_HEIGHT = SCREEN_SIZE["height"] - MENU_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - 2 - 120

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(HEADER_HEIGHT)
        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel('PyDouban - 豆瓣电影 TOP250(桌面版)')
        label.setStyleSheet('font-size: 32px; font-weight: bold; margin-left: 10px; margin-bottom: 5px;')
        layout.addWidget(label)

class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(FOOTER_HEIGHT)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        source_label = QLabel('数据来源:  豆瓣电影 TOP250')
        link_label = QLabel('(https://movie.douban.com/top250)')
        source_label.setStyleSheet('font-size: 14px;')
        link_label.setStyleSheet('font-size: 14px; color: #00f; text-decoration: underline; margin-left: 5px;')
        group_label = QLabel('制作团队:  Python程序设计小组')
        group_label.setStyleSheet('font-size: 14px; margin-left: 20px;')
        member_label = QLabel('成员:  菅佳玥、贺佳明、徐云天')
        member_label.setStyleSheet('font-size: 14px; margin-left: 20px;')
        layout.addWidget(source_label)
        layout.addWidget(link_label)
        layout.addWidget(group_label)
        layout.addWidget(member_label)

class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.movie_list = MovieList()
        self.setFixedHeight(CONTENT_HEIGHT)
        
        self.user = User()
        if not self.user.is_login():
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            warn_label = QLabel('请先登录')
            warn_label.setStyleSheet('font-size: 32px; font-weight: bold;')
            warn_label.setAlignment(Qt.AlignCenter)
            warn_label2 = QLabel('登录后方可查看电影列表')
            warn_label2.setStyleSheet('font-size: 32px; font-weight: bold;')
            warn_label2.setAlignment(Qt.AlignCenter)
            layout.addWidget(warn_label)
            layout.addWidget(warn_label2)
            self.setLayout(layout)
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
        list_layout = QVBoxLayout()
        list_layout.setAlignment(Qt.AlignTop)
        list_widget.setLayout(list_layout)
        self.scroll_area.setWidget(list_widget)

        self.page = 1
        self.load_more()
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.onScroll)

        layout.addWidget(self.scroll_area)

    def onScroll(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar.value() == scroll_bar.maximum():
            self.load_more()
    
    def load_more(self):
        self.page += 1
        movies = self.movie_list.load_list(self.page)
        row_index = 0
        row_widget = None
        for movie in movies:
            if row_index % 3 == 0:
                card_widget = CardWidget(movie)
                row_widget = QWidget()
                row_layout = QHBoxLayout()
                row_widget.setLayout(row_layout)
                row_layout.addWidget(card_widget)
                self.scroll_area.widget().layout().addWidget(row_widget)
                row_index = 1
            else:
                card_widget = CardWidget(movie)
                row_layout.addWidget(card_widget)
                row_index += 1

class Divider(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(1)
        self.setStyleSheet('background-color: #ccc;')

class IndexWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(HeaderWidget())
        layout.addWidget(Divider())
        layout.addWidget(ContentWidget())
        layout.addWidget(Divider())
        layout.addWidget(FooterWidget())
        self.setLayout(layout)
