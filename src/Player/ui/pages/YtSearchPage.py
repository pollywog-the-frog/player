from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow

from Player.ui.components.NavBar import NavBar

class YTSearchPage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow):
        super().__init__()

        self.stack = stack
        self.main_window = main_window
        nav_bar = NavBar(stack=self.stack, main_window=self.main_window, parent=self)