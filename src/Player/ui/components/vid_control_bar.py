from mpv import MPV

from datetime import timedelta

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, Slot

from Player.core.qtmpvstatus import QtMpvStatus
from Player.core.mediastream import MediaStream
from Player.ui.components.vid_slider import VideoSlider

class VideoControlBar(QWidget):

    def __init__(self, status: QtMpvStatus, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._status = status
        self._stream = None

        # Defin v_layout
        v_layout = QVBoxLayout(self)

        # Define title
        self.title = QLabel(self._stream.title if hasattr(self._stream, 'title') else "No title available")

        # Define slider
        self.slider = VideoSlider(main_window=main_window, parent=self, orientation=Qt.Horizontal)

        # Connect signals
        self._status.percent_posChanged.connect(self.setSliderValue)
        self._status.time_posChanged.connect(self.updateStatusLabel)

        # Define status label
        self.status_label = QLabel("00:00:00.00/--:--:--")


        v_layout.addWidget(self.title)
        v_layout.addWidget(self.slider)
        v_layout.addWidget(self.status_label)
        
        self.setAttribute(Qt.WA_StyledBackground, True)

    @Slot(float)
    def setSliderValue(self, val: float) -> None:
        if self.slider.isSliderDown():
            return
        self.slider.blockSignals(True)
        self.slider.setValue(int(val * (self.slider.maximum()/10**2)))
        self.slider.blockSignals(False)

    @Slot(float)
    def updateStatusLabel(self, val: float):
        td = timedelta(seconds=val)
        self.status_label.setText(f"{(td.seconds // 3600):02d}:{((td.seconds % 3600) // 60):02d}:{(td.seconds % 60):02d}.{(td.microseconds // 10000):02d}/{timedelta(seconds=self._stream.duration) if hasattr(self._stream, "duration") else "-.--"}")

    def initializeMetaData(self, stream: MediaStream) -> None:
        self._stream = stream
        self.title.setText(self._stream.title if hasattr(self._stream, 'title') else "No title available")
        self.status_label.setText(f"00:00:00.00/{timedelta(seconds=self._stream.duration) if hasattr(self._stream, "duration") else "--:--:--"}")