import os

from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from Player.ui.components.abstract_skip_button import AbstractSkipButton

class ForwardButton(AbstractSkipButton):

    def __init__(self, main_window: QMainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._icon = QIcon(os.path.join(os.getenv("SVG_PATH"), "arrow-uturn-right.svg"))
        self.setIcon(self._icon)
        self.clicked.connect(lambda : main_window.controls.seek(10))
