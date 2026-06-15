import os

from mpv import MPV

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from Player.core.MpvStatus import MpvStatus
from Player.core.mediastream import MediaStream
from Player.core.QtMpvStatus import QtMpvStatus
from Player.ui.components.PlayPauseButton import PlayPauseButton
from Player.ui.components.VideoControlBar import VideoControlBar

class VideoControls(QWidget):
    def __init__(self, parent: QWidget, mpv_instance: MPV, status: MpvStatus, stream: MediaStream | None):
        super().__init__(parent=parent)

        # Add mpv_instance and status to self
        self._player = mpv_instance
        self._status = QtMpvStatus(mpv_instance=mpv_instance, parent=self)

        # Define layout
        v_layout = QVBoxLayout(self)

        # Define central play/pause button
        central_play_pause = PlayPauseButton(parent=self, mpv_instance=self._player, status=self._status)

        # Define control bar
        self.control_bar = VideoControlBar(self._player, self._status, self)

        # Add all to layout
        v_layout.addStretch()
        v_layout.addWidget(central_play_pause, alignment=Qt.AlignCenter)
        v_layout.addStretch()
        v_layout.addWidget(self.control_bar)

        # Set all margin to 0
        v_layout.setContentsMargins(0, 0, 0, 0)

    def play_pause(self) -> None:
        self._player.command('cycle', 'pause')