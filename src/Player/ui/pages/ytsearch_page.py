from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow

from Player.ui.components.nav_bar import NavBar

class YTSearchPage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow):
        super().__init__()

        self.stack = stack
        self.main_window = main_window