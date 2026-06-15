import os

import threading

from mpv import MPV

from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import Signal, Slot, QSize
from PySide6.QtGui import QIcon

from Player.core.MpvStatus import MpvStatus
from Player.core.QtMpvStatus import QtMpvStatus

class PlayPauseButton(QPushButton):

    def __init__(self, mpv_instance: MPV, status: QtMpvStatus, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self._player = mpv_instance
        self._status = status
        self._status.playingChanged.connect(self.update_icon)

        
        self._play_icon = QIcon(os.path.join(os.getenv("SVG_PATH"), "play.svg"))
        self._pause_icon = QIcon(os.path.join(os.getenv("SVG_PATH"), "pause.svg"))

        self.setIconSize(QSize(40,40))
        self.setFixedSize(QSize(70,70))
        self.clicked.connect(self.play_pause)


    def play_pause(self) -> None:
        self._player.command('cycle', 'pause')


    @Slot(bool)
    def update_icon(self, playing) -> None:
        self.setIcon(self._pause_icon if playing else self._play_icon)
