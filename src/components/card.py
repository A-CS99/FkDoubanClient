from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm
from utils import get_image
from urllib.parse import quote
from config import SERVER_HOST, SERVER_PORT, SERVER_BASE_URL

demo_movie = {
    "rank": 0,
    "name": "正在加载中...",
    "director": "xxx",
    "starring": "xxx",
    "type": "xx",
    "country": "xx",
    "release_date": "xxxx-xx-xx",
    "rating": 0,
    "comments_user": 99999,
    "coverUrl": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp"
}

class RankLabel(QLabel):
    def __init__(self, rank):
        super().__init__()
        self.setFixedWidth(30)
        self.setFixedHeight(30)
        self.setText(str(rank))
        self.setStyleSheet('background-color: #ccc; font-size: 15px; color: #fff; border-radius: 15px;')
        self.setAlignment(Qt.AlignCenter)

class CoverLabel(QLabel):
    def __init__(self, img_path, width=100, height=150):
        super().__init__()
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        img_path = quote(img_path)
        if not img_path.startswith("http"):
            img_path = f'http://{SERVER_HOST}:{SERVER_PORT}{SERVER_BASE_URL}{img_path}'
        image = get_image(img_path)
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        pixmap = pixmap.scaled(width, height)
        self.setPixmap(pixmap)

class ElidedLabel(QLabel):
    def __init__(self, text, max_width):
        super().__init__()
        self.max_width = max_width
        self.setAlignment(Qt.AlignLeft)
        self.setText(text)

    def setText(self, text):
        metrics = self.fontMetrics()
        elided_text = metrics.elidedText(text, Qt.ElideRight, self.max_width)
        super().setText(elided_text)

class FullStarLabel(QLabel):
    def __init__(self, size=15):
        super().__init__()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        pixmap = QPixmap('src/assets/full_star.png')
        pixmap = pixmap.scaled(size, size)
        self.setPixmap(pixmap)

class HalfStarLabel(QLabel):
    def __init__(self, size=15):
        super().__init__()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        pixmap = QPixmap('src/assets/half_star.png')
        pixmap = pixmap.scaled(size, size)
        self.setPixmap(pixmap)

class NoStarLabel(QLabel):
    def __init__(self, size=15):
        super().__init__()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        pixmap = QPixmap('src/assets/no_star.png')
        pixmap = pixmap.scaled(size, size)
        self.setPixmap(pixmap)

class RatingWidget(QWidget):
    def __init__(self, rating):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        rating_label = QLabel(f"{rating}")
        rating_label.setStyleSheet('color: #ffac2d; font-size: 14px; font-weight: bold; margin-left: 5px;')
        
        temp_rating = rating / 2
        no_star_num = int((5 - temp_rating) // 1)
        while temp_rating >= 1:
            full_star = FullStarLabel(15)
            layout.addWidget(full_star)
            temp_rating -= 1
        if temp_rating > 0:
            if temp_rating >= 0.5:
                full_star = FullStarLabel(15)
                layout.addWidget(full_star)
            else:
                half_star = HalfStarLabel(15)
                layout.addWidget(half_star)
        for _ in range(no_star_num):
            no_star = NoStarLabel(15)
            layout.addWidget(no_star)
        layout.addWidget(rating_label)
        self.setLayout(layout)

class InfoWidget(QWidget):
    def __init__(self, movie):
        super().__init__()
        self.setFixedWidth(210)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        movie = self.cut_short(movie)
        name = ElidedLabel(movie["name"], 140)
        name.setStyleSheet('font-size: 16px; font-weight: bold; margin-bottom: 10px;')
        director = ElidedLabel(f"导演: {movie['director']}", 200)
        starring = ElidedLabel(f"主演: {movie['starring']}", 200)
        release_country_type = ElidedLabel(f"{movie['release_date'][:4]} / {movie['country']} / {movie['type']}", 200)
        rating = RatingWidget(movie['rating'])
        comments_user = ElidedLabel(f"{movie['comments_user']}人参与评价", 200)

        layout.addWidget(name)
        layout.addWidget(director)
        layout.addWidget(starring)
        layout.addWidget(release_country_type)
        layout.addWidget(rating)
        layout.addWidget(comments_user)

        self.setLayout(layout)
    
    def cut_short(self, movie):
        return {
            "name": movie["name"],
            "director": movie["director"],
            "starring": movie["starring"],
            "type": movie["type"].replace("/", " "),
            "country": movie["country"],
            "release_date": movie["release_date"],
            "rating": movie["rating"],
            "comments_user": movie["comments_user"]
        }

class CardWidget(QWidget):
    def __init__(self, movie=demo_movie):
        super().__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(400)
        self.movie = movie
        layout = QHBoxLayout()

        rank = RankLabel(movie["rank"])
        cover = CoverLabel(movie["coverUrl"], 100, 150)
        info = InfoWidget(movie)

        layout.addWidget(rank)
        layout.addWidget(cover)
        layout.addWidget(info)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            dialog = MovieDialog(self.movie)
            dialog.exec()
        
class DetailWidget(QWidget):
    def __init__(self, movie):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        name = QLabel(f"{movie['name']}")
        name.setStyleSheet('font-size: 20px; font-weight: bold;')
        director = QLabel(f"导演: {movie['director']}")
        writer = QLabel(f"编剧: {movie['writer']}")
        starring = QLabel(f"主演: {movie['starring']}")
        type = QLabel(f"类型: {movie['type']}")
        country = QLabel(f"制片国家/地区: {movie['country']}")
        language = QLabel(f"语言: {movie['language']}")
        release_date = QLabel(f"上映日期: {movie['release_date']}")
        run_time = QLabel(f"片长: {movie['run_time']}分钟")
        imdb_href = QLabel(f"IMDb: {movie['imdb_href']}")
        
        layout.addWidget(name)
        layout.addWidget(director)
        layout.addWidget(writer)
        layout.addWidget(starring)
        layout.addWidget(type)
        layout.addWidget(country)
        layout.addWidget(language)
        layout.addWidget(release_date)
        layout.addWidget(run_time)
        layout.addWidget(imdb_href)

        self.setLayout(layout)

class SideRatingWidget(QWidget):
    def __init__(self, rating, comments_user, star_ratio):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        rating_widget = RatingWidget(rating)
        comments_user_label = QLabel(f"{comments_user}人参与评价")
        comments_user_label.setStyleSheet('font-size: 12px;')
        # 绘制横向柱状图
        zh_font = fm.FontProperties(fname='src/assets/SIMHEI.ttf')
        x = ['5星', '4星', '3星', '2星', '1星']
        y = star_ratio
        fig = plt.figure(figsize=(4, 2))
        ax = fig.add_subplot(111)
        bars = ax.barh(x, y, color='#ffac2d')
        ax.set_yticklabels(x, fontproperties=zh_font)
        # 在柱子顶部显示百分比值
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{width:.1%}', ha='left', va='center', color='black')
        # 隐藏边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        canvas = FigureCanvas(fig)

        layout.addWidget(rating_widget)
        layout.addWidget(comments_user_label)
        layout.addWidget(canvas)

        self.setLayout(layout)

class MovieDialog(QDialog):
    def __init__(self, movie=demo_movie):
        super().__init__()
        self.setWindowTitle(f"电影详情 - {movie['name']}")
        self.setFixedWidth(1100)
        self.setFixedHeight(800)
        self.setStyleSheet('background-color: #fff;')

        layout = QVBoxLayout()

        movie_widget = QWidget()
        movie_widget.setFixedHeight(400)
        movie_layout = QHBoxLayout()
        movie_widget.setLayout(movie_layout)

        cover = CoverLabel(movie["coverUrl"], 200, 300)
        detail = DetailWidget(movie)
        rating = SideRatingWidget(movie["rating"], movie["comments_user"], movie["star_ratio"])

        movie_layout.addWidget(cover)
        movie_layout.addWidget(detail)
        movie_layout.addWidget(rating)
        movie_layout.setSpacing(10)
        movie_layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(movie_widget)
        self.setLayout(layout)