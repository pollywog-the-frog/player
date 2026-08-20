from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QPoint, Signal, Slot
from PySide6.QtWidgets import QFrame, QWidget, QGridLayout

from Player.core.mpv_widgets import MpvDisplay
from Player.ui.components.vid_controls import VideoControls

class DisplayFrame(QFrame):

    doubleClicked = Signal()

    def __init__(self, main_window, mpv_instance, **kwargs) -> None:
        super().__init__(**kwargs)

        self.main_window = main_window

        self._drag_start = QPoint()

        # Set mouse tracking
        self.setMouseTracking(True)

        g_layout = QGridLayout(self)
        g_layout.setContentsMargins(0,0,0,0)

        # Define display
        self.display = MpvDisplay(mpv_instance=mpv_instance, main_window=main_window, parent=self)

        # Define video controls
        self.video_controls = VideoControls(main_window=self.main_window, parent=self, status=self.main_window.qtstatus)

        # Define timers
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(5000)
        self.hide_timer.timeout.connect(self.video_controls.hide)
        self.hide_timer.timeout.connect(self.main_window.nav_bar.conditionalHide)
        self.pauseclick_timer = QElapsedTimer()

        g_layout.addWidget(self.display, 0, 0)
        g_layout.addWidget(self.video_controls, 0, 0)
        
        
        # Set minimum size 16:9 ratio width:height
        self.setMinimumSize(336, 188)

        self.setProperty(
            "is_min_size",
            self.size() == self.minimumSize()
        )

        self.setObjectName('display_frame')

        # Hide video_controls
        self.video_controls.hide()
    
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

        self.video_controls.show()
        self.main_window.nav_bar.show()

        if self.main_window.status.playing:
            self.hide_timer.start()
        # for child in self.children():
        #     if isinstance(child, QWidget):
        #         child.setGeometry(self.rect().adjusted(2, 2, -2, -2))
        return super().resizeEvent(event)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pauseclick_timer.start()
        if event.button() == Qt.LeftButton and not self.isFullWindow():
            self._drag_start = event.globalPosition().toPoint() - self.pos()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.pauseclick_timer.elapsed() < 900:
                self.main_window.controls.cycle_pause()
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        self.video_controls.show()
        self.main_window.nav_bar.show()

        if self.main_window.status.playing:
            self.hide_timer.start()

        if event.buttons() & Qt.LeftButton and not self.isFullWindow():
            self.move(event.globalPosition().toPoint() - self._drag_start)
        return super().mouseMoveEvent(event)