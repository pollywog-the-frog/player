from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QMainWindow
from PySide6.QtCore import Signal

from Player.ui.components.home_button import HomeButton
from Player.ui.components.search_button import SearchButton
from Player.ui.components.direct_url_button import DirectUrlButton

class NavBar(QWidget):
    buttonClicked = Signal()
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = self.window()

        h_layout = QHBoxLayout(self)

        home_button = HomeButton(stack=stack, main_window=main_window)
        search_button = SearchButton(stack=stack, main_window=main_window)
        direct_url_button = DirectUrlButton(stack=stack, main_window=main_window)

        home_button.clicked.connect(self.buttonClicked.emit)
        search_button.clicked.connect(self.buttonClicked.emit)
        direct_url_button.clicked.connect(self.buttonClicked.emit)


        h_layout.addWidget(home_button)
        h_layout.addWidget(search_button)
        h_layout.addWidget(direct_url_button)

        self.setMinimumSize(int(home_button.maximumWidth()*4.5), int(home_button.maximumHeight()*1.5))

    def conditionalHide(self) -> None:
        if self.main_window.displayIsFullWindow():
            self.hide()