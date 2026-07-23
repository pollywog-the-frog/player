from PySide6.QtWidgets import QWidget, QStackedWidget, QMainWindow, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt
from Player.core.mediastream import MediaStream
import mpv
from Player.core.mpv_widgets import MpvWidget
from Player.ui.components.nav_bar import NavBar
from Player.ui.components.search_button import SearchButton
from Player.ui.components.direct_url_button import DirectUrlButton

class PlayerPage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow) -> None:
        super().__init__()

        # Define stack and main_window
        self.stack = stack
        self.main_window = main_window

        # Initialize media stream to None type
        self.stream = None
        
        # Define layout
        self.v_layout = QVBoxLayout(self)

        # Define display
        #self.display = MpvWidget(parent=self, stream=self.stream)

        # Add widgets to layout
        #self.v_layout.addWidget(self.display)

        # Set margins to zero
        self.v_layout.setContentsMargins(0,0,0,0)

    def initalize_media(self, stream: MediaStream) -> None:
        self.stream = stream
        self.main_window.display.stop()
        self.main_window.display.video_controls.control_bar.initializeMetaData(stream)
        
    def play_all(self) -> None:
        if self.stream.audio_url:
            self.main_window.display.play_all(self.stream.video_url, self.stream.audio_url)
        else:
            self.main_window.display.play_video(self.stream.video_url)

    def play_video(self) -> None:
        self.main_window.display.play_video(self.stream.video_url)

    def play_audio(self) -> None:
        if self.stream.audio_url:
            self.main_window.display.play_audio(self.stream.audio_url)

    @property
    def playing(self):
        return self.main_window.display.status.playing


