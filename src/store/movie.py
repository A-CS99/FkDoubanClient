from PySide6.QtCore import QObject
from utils import get, singleton

@singleton
class MovieList(QObject):
    def __init__(self):
        self.list = []

    def get_list(self):
        return self.list

    def load_list(self, page):
        res = get(f"/list/{page}")
        self.list += res["data"]["movies"]
        return res["data"]["movies"]

    def get_movie_by_rank(self, rank):
        res = get(f"/movie/{rank}")
        return res["data"]