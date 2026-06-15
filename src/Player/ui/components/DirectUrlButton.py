import os

from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow

from Player.ui.components.NavButton import NavButton

class DirectUrlButton(NavButton):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow,  parent: QWidget | None = None):
        super().__init__(stack=stack, main_window=main_window, nav_to='direct_url_page', icon=os.path.join(os.getenv("SVG_PATH"), "link.svg"), parent=parent)