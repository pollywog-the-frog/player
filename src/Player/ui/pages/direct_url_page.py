from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QMainWindow, QSizePolicy

from Player.core.mediastream import MediaStream

class DirectURLPage(QWidget):
    def __init__(self, stack: QStackedWidget, main_window: QMainWindow):
        super().__init__()

        # Define stack and main_window
        self.stack = stack
        self.main_window = main_window

        # Define vertical layout
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(1)

        # Define label and input field
        label = QLabel('Enter a URL')
        self.input = QLineEdit()

        # Define button container and layout
        button_container = QWidget()
        button_h_layout = QHBoxLayout(button_container)

        # Define buttons
        play_all_button = QPushButton("Play all")
        play_all_button.clicked.connect(lambda: self.submit("all"))
        play_video_button = QPushButton("Play video (muted)")
        play_video_button.clicked.connect(lambda: self.submit("video"))
        play_audio_button = QPushButton("Play audio")
        play_audio_button.clicked.connect(lambda: self.submit("audio"))

        # Set button size policys
        play_all_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        play_video_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        play_audio_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Set button names for styling
        play_all_button.setObjectName("play_button")
        play_video_button.setObjectName("play_button")
        play_audio_button.setObjectName("play_button")

        # Add buttons to container
        button_h_layout.addWidget(play_all_button)
        button_h_layout.addWidget(play_video_button)
        button_h_layout.addWidget(play_audio_button)

        # Add label, input field, and container to v_layout
        v_layout.addWidget(label)
        v_layout.addWidget(self.input)
        v_layout.addWidget(button_container)

        # Set v_layout margins
        v_layout.setContentsMargins(50,250,50,50)

    def submit(self, option: str) -> None:
        # Get input
        url = self.input.text()

        # Define stream
        stream = MediaStream(url)
        
        # Initialize media on display and controls
        self.main_window.display_frame.video_controls.control_bar.initializeMetaData(stream)
        self.main_window.controls.initalize_media(stream)

        self.main_window.cycle_display_show(True)

        # Start playing
        getattr(self.main_window.controls, f"play_{option}")()
