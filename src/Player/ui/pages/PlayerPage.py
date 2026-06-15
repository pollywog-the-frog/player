from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt
from Player.core.mediastream import MediaStream
import mpv
from Player.ui.components.MpvWidget import MpvWidget
from Player.ui.components.NavBar import NavBar
from Player.ui.components.HomeButton import HomeButton
from Player.ui.components.SearchButton import SearchButton
from Player.ui.components.DirectUrlButton import DirectUrlButton

class PlayerPage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow) -> None:
        super().__init__()

        # Define stack and main_window
        self.stack = stack
        self.main_window = main_window

        # Initialize media stream to None type
        self.stream = None

        # Define layout
        v_layout = QVBoxLayout(self)

        # Define display
        self.display = MpvWidget(parent=self, stream=self.stream)

        # Add widgets to layout
        v_layout.addWidget(self.display)

        # Throw the nav_bar on top
        nav_bar = NavBar(stack=self.stack, main_window=self.main_window, parent=self)

    def initalize_media(self, stream: MediaStream) -> None:
        self.stream = stream
        self.display.stop()
        self.display.video_controls.control_bar.initializeMetaData(stream)
        
    def play_all(self) -> None:
        if self.stream.audio_url:
            self.display.play_all(self.stream.video_url, self.stream.audio_url)
        else:
            self.display.play_video(self.stream.video_url)

    def play_video(self) -> None:
        self.display.play_video(self.stream.video_url)

    def play_audio(self) -> None:
        if self.stream.audio_url:
            self.display.play_audio(self.stream.audio_url)


