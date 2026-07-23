import os

from mpv import MPV

from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus
from Player.ui.components.playpausebutton import PlayPauseButton
from Player.ui.components.vid_control_bar import VideoControlBar

class VideoControls(QWidget):
    def __init__(self, main_window: QMainWindow, status: QtMpvStatus, **kwargs):
        super().__init__(**kwargs)

        # Add status to self
        self._status = status

        # Define layout
        v_layout = QVBoxLayout(self)

        # Define central play/pause button
        central_play_pause = PlayPauseButton(main_window=main_window, parent=self, status=self._status)

        # Define control bar
        self.control_bar = VideoControlBar(status=self._status, parent=self)

        # Add all to layout
        v_layout.addStretch()
        v_layout.addWidget(central_play_pause, alignment=Qt.AlignCenter)
        v_layout.addStretch()
        v_layout.addWidget(self.control_bar)

        # Set all margin to 0
        v_layout.setContentsMargins(0, 0, 0, 0)