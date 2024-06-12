PROJECT_NAME = "PyDouban - 豆瓣电影 TOP250(桌面版)"
SCREEN_SIZE = {"width": 1707, "height": 1067}
MENU_HEIGHT = 60
ENV = "prod"  # "dev" or "prod"
SERVER_HOST = "127.0.0.1" if ENV == "dev" else "154.8.151.96"
SERVER_PORT = 4523 if ENV == "dev" else 80
SERVER_BASE_URL = "/m1/4537752-0-default" if ENV == "dev" else "/douban/api"