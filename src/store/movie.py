from PySide6.QtCore import QObject
from utils import get, singleton
from urllib.parse import quote

@singleton
class MovieList(QObject):
    def __init__(self):
        self.list = []
        self.search_options = [
            {"label": "电影名", "value": "name"},
            {"label": "导演", "value": "director"},
            {"label": "演员", "value": "starring"},
            {"label": "类型", "value": "type"},
            {"label": "国家", "value": "country"}
        ]

    def get_list(self):
        return self.list

    def load_list(self, page):
        res = get(f"/list/{page}")
        self.list += res["data"]["movies"]
        return res["data"]["movies"]

    def get_movie_by_rank(self, rank):
        res = get(f"/movie/{rank}")
        return res["data"]
    
    def get_search_options(self):
        return self.search_options
    
    def search_movie(self, type, text):
        text = quote(text)
        res = get(f"/movie/search?type={type}&text={text}")
        return res["data"]["movies"]
