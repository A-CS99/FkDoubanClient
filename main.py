import sys
from PySide6.QtWidgets import QApplication
from components.main_window import MainWindow

if __name__ == '__main__':
    # 创建应用程序
    app = QApplication(sys.argv)
    # 创建窗口
    window = MainWindow()
    window.show()
    app.exit(app.exec())