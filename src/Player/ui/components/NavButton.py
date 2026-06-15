from PySide6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QPushButton
from PySide6.QtGui import QIcon

class NavButton(QPushButton):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow, nav_to: str, icon: str,  parent: QWidget | None = None):
        super().__init__(parent)

        self.setFixedSize(44, 44)
        self.setIcon(QIcon(icon))
        self.clicked.connect(lambda: stack.setCurrentWidget(getattr(main_window, f"{nav_to}")))
        
