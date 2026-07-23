from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout

from Player.core.mpv_widgets import MpvDisplay

class DisplayFrame(QFrame):

    doubleClicked = Signal()

    def __init__(self, main_window, **kwargs) -> None:
        super().__init__(**kwargs)

        self.main_window = main_window

        self._drag_start = QPoint()
        v_layout = QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        # # Define display
        # self.display = MpvDisplay(main_window=main_window, parent=self)
        
        # Set minimum size 16:9 ratio width:height
        self.setMinimumSize(336, 188)

        self.setProperty(
            "is_min_size",
            self.size() == self.minimumSize()
        )

        self.setObjectName('display_frame')

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        return super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        self.main_window.controls.cycle_pause()
        return super().mousePressEvent(event)

    def resizeEvent(self, event):
        # for child in self.children():
        #     if isinstance(child, QWidget):
        #         child.setGeometry(self.rect().adjusted(2, 2, -2, -2))
        self.setProperty(
            "is_min_size",
            self.size() == self.minimumSize()
        )
        self.style().unpolish(self)
        self.style().polish(self)
        return super().resizeEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.globalPosition().toPoint() - self.pos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_start)
        return super().mouseMoveEvent(event)