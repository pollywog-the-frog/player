from PySide6.QtCore import Qt, QPoint, Signal, Slot
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout

from Player.core.mpv_widgets import MpvDisplay

class DisplayFrame(QFrame):

    doubleClicked = Signal()

    def __init__(self, main_window, mpv_instance, **kwargs) -> None:
        super().__init__(**kwargs)

        self.main_window = main_window

        self._drag_start = QPoint()

        v_layout = QVBoxLayout(self)

        # Define display
        self.display = MpvDisplay(mpv_instance=mpv_instance, main_window=main_window, parent=self)

        v_layout.addWidget(self.display)

        v_layout.setContentsMargins(0,0,0,0)
        
        # Set minimum size 16:9 ratio width:height
        self.setMinimumSize(336, 188)

        self.setProperty(
            "is_min_size",
            self.size() == self.minimumSize()
        )

        self.setObjectName('display_frame')
    
    def isFullWindow(self) -> bool:
        return self.main_window.rect() == self.rect()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        return super().mouseDoubleClickEvent(event)

    def resizeEvent(self, event):
        self.setProperty(
            "is_min_size",
            self.size() == self.minimumSize()
        )
        self.style().unpolish(self)
        self.style().polish(self)
        # for child in self.children():
        #     if isinstance(child, QWidget):
        #         child.setGeometry(self.rect().adjusted(2, 2, -2, -2))
        return super().resizeEvent(event)
            
    def mousePressEvent(self, event):
        self.main_window.controls.cycle_pause()
        if event.button() == Qt.LeftButton and not self.isFullWindow():
            self._drag_start = event.globalPosition().toPoint() - self.pos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and not self.isFullWindow():
            self.move(event.globalPosition().toPoint() - self._drag_start)
        return super().mouseMoveEvent(event)