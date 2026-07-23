from PySide6.QtWidgets import QMainWindow, QPushButton, QStackedWidget
from PySide6.QtCore import Slot
from PySide6.QtGui import QMouseEvent

from Player.core.mediastream import MediaStream
from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus
from Player.core.mpv_widgets import MpvDisplay

class NowPlaying(QPushButton):
    def __init__(self, status: MpvStatus, qtstatus: QtMpvStatus, stack: QStackedWidget, main_window: QMainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stack = stack
        self.main_window = main_window
        self.status = status

        self.display = self.main_window.player_page.display

        self.stack.currentChanged.connect(self.cycle_show)
        qtstatus.playingChanged.connect(self.cycle_show)
        self.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_window.player_page))
        self.hide()

    def initalize_media(self, stream: MediaStream) -> None:
        self.stream = stream
        self.display.stop()
        self.display.video_controls.control_bar.initializeMetaData(stream)

    
    @Slot()
    def cycle_show(self):
        if self.status.file_loaded:
            if self.isHidden() and not self.stack.currentWidget() is self.main_window.player_page:
                self.show()
            elif self.isVisible() and not self.stack.currentWidget() is self.main_window.player_page:
                pass
            else:
                self.hide()

    def mousePressEvent(self, event: QMouseEvent):
        self.stack.setCurrentWidget(self.main_window.player_page)
        return super().mousePressEvent(event)