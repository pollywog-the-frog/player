from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus
from Player.ui.components.playpausebutton import PlayPauseButton
from Player.ui.components.forward_button import ForwardButton
from Player.ui.components.backward_button import BackwardButton
from Player.ui.components.vid_control_bar import VideoControlBar

class VideoControls(QWidget):
    def __init__(self, main_window: QMainWindow, status: QtMpvStatus, **kwargs):
        super().__init__(**kwargs)

        # Add status to self
        self._status = status

        # Define v_layout
        v_layout = QVBoxLayout(self)

        # Define button_container
        button_container = QWidget(self)

        # Define h_layout
        h_layout = QHBoxLayout(button_container)

        # Define central buttons
        central_play_pause = PlayPauseButton(main_window=main_window, parent=self, status=self._status)
        forward_button = ForwardButton(main_window=main_window, parent=self)
        backward_button = BackwardButton(main_window=main_window, parent=self)

        # Add buttons to h_layout
        h_layout.addStretch()
        h_layout.addWidget(backward_button)
        h_layout.addWidget(central_play_pause)
        h_layout.addWidget(forward_button)
        h_layout.addStretch()

        # Set h_layout spacing
        h_layout.setSpacing(20)

        # Define control bar
        self.control_bar = VideoControlBar(status=self._status, main_window=main_window, parent=self)

        # Add all to v_layout
        v_layout.addStretch()
        v_layout.addWidget(button_container, alignment=Qt.AlignCenter)
        v_layout.addStretch()
        v_layout.addWidget(self.control_bar)

        # Set all margin to 0
        v_layout.setContentsMargins(0, 0, 0, 0)