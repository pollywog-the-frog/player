import os

import threading

from mpv import MPV

from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton
from PySide6.QtCore import Signal, Slot, QSize
from PySide6.QtGui import QIcon

from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus

class PlayPauseButton(QPushButton):

    def __init__(self, main_window: QMainWindow, status: QtMpvStatus, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._status = status
        self._status.playingChanged.connect(self.update_icon)

        
        self._play_icon = QIcon(os.path.join(os.getenv("SVG_PATH"), "play.svg"))
        self._pause_icon = QIcon(os.path.join(os.getenv("SVG_PATH"), "pause.svg"))

        self.setIconSize(QSize(40,40))
        self.setFixedSize(QSize(70,70))
        self.clicked.connect(main_window.controls.cycle_pause)


    @Slot(bool)
    def update_icon(self, playing) -> None:
        self.setIcon(self._pause_icon if playing else self._play_icon)
