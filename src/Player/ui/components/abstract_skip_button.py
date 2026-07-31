from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon


class AbstractSkipButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setIconSize(QSize(30,30))
        self.setFixedSize(QSize(52.5,52.5))