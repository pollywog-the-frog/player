import os

from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

class HomePage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow):
        super().__init__()

        # Add the stack and main_window
        self.stack = stack
        self.main_window = main_window

        # Define the horizantal layout
        h_layout = QHBoxLayout(self)

        # Define list container
        container = QWidget()
        
        # Define the vertical layout
        v_layout = QVBoxLayout(container)

        # Add the stack
        self.stack = stack

        # Define buttons
        ytsearch_button = QPushButton(QIcon(os.path.join(os.getenv("SVG_PATH"), "magnifying-glass.svg")), "Search Youtube for media")
        ytsearch_button.setIconSize(QSize(35,35))
        ytsearch_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_window.ytsearch_page))
        direct_url_button = QPushButton(QIcon(os.path.join(os.getenv("SVG_PATH"), "link.svg")), "Enter a direct URL to media")
        direct_url_button.setIconSize(QSize(35,35))
        direct_url_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_window.direct_url_page))

        # Add buttons to v_layout
        v_layout.addWidget(ytsearch_button)
        v_layout.addWidget(direct_url_button)

        # Add container to h_layout
        h_layout.addStretch(1)
        h_layout.addWidget(container, 1)
        h_layout.addStretch(1)