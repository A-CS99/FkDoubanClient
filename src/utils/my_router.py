# router.py
from PySide6.QtCore import QObject, Signal
from utils import singleton

@singleton
class Router(QObject):
    navigateSignal = Signal()

    def __init__(self):
        super().__init__()
        self.curPage = None

    def bind_routes(self, routes):
        self.routes = routes
    
    def get_cur_page(self):
        return self.curPage

    def navigate(self, route):
        if route in self.routes:
            if self.routes[route] is not self.curPage:
                self.curPage = self.routes[route]()
            self.navigateSignal.emit()

router = Router()