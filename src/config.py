PROJECT_NAME = "PyDouban - 豆瓣电影 TOP250(桌面版)"
SCREEN_SIZE = {"width": 1707, "height": 1067}
MENU_HEIGHT = 60
ENV = "prod"  # "dev" or "prod"
__dev = {
    "host": "127.0.0.1",
    "port": 4523,
    "base_url": "/m1/4537752-0-default"
}
__prod = {
    "host": "154.8.151.96",
    "port": 80,
    "base_url": "/douban/api"
}
SERVER_HOST = __prod["host"] if ENV == "prod" else __dev["host"]
SERVER_PORT = __prod["port"] if ENV == "prod" else __dev["port"]
SERVER_BASE_URL = __prod["base_url"] if ENV == "prod" else __dev["base_url"]