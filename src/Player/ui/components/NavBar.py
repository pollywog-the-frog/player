from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QMainWindow

from Player.ui.components.HomeButton import HomeButton
from Player.ui.components.SearchButton import SearchButton
from Player.ui.components.DirectUrlButton import DirectUrlButton
from Player.ui.components.NavButton import NavButton

class NavBar(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow, parent: QWidget | None = None):
        super().__init__(parent)

        self.stack = stack
        self.main_window = main_window

        h_layout = QHBoxLayout(self)

        home_button = HomeButton(stack=self.stack, main_window=self.main_window)
        search_button = SearchButton(stack=self.stack, main_window=self.main_window)
        direct_url_button = DirectUrlButton(stack=self.stack, main_window=self.main_window)

        h_layout.addWidget(home_button)
        h_layout.addWidget(search_button)
        h_layout.addWidget(direct_url_button)

        self.setMinimumSize(int(home_button.maximumWidth()*4.5), int(home_button.maximumHeight()*1.5))