from mpv import MPV

from datetime import timedelta

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, Slot

from Player.core.QtMpvStatus import QtMpvStatus
from Player.core.mediastream import MediaStream

class VideoControlBar(QWidget):
    def __init__(self, mpv_instance: MPV, status: QtMpvStatus, stream: MediaStream, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self._player = mpv_instance
        self._status = status
        self._stream = stream

        # Defin v_layout
        v_layout = QVBoxLayout(self)

        # Define title
        self.title = QLabel(self._stream.title if hasattr(self._stream, 'title') else "No title available")

        # Define slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMaximum(10**8)

        # Connect signals
        self._status.percent_posChanged.connect(self.setSliderValue)
        self._status.time_posChanged.connect(self.updateStatusLabel)

        # Define status label
        self.status_label = QLabel("0.00/0.00")


        v_layout.addWidget(self.title)
        v_layout.addWidget(self.slider)
        v_layout.addWidget(self.status_label)

    @Slot(float)
    def setSliderValue(self, val: float) -> None:
        self.slider.setValue(int(val * 10**6))

    @Slot(float)
    def updateStatusLabel(self, val: float):
        td = timedelta(seconds=val)
        self.status_label.setText(f"{(td.seconds // 3600):02d}:{((td.seconds % 3600) // 60):02d}:{(td.seconds % 60):02d}.{(td.microseconds // 10000):02d}/{timedelta(seconds=self._stream.duration) if hasattr(self._stream, "duration") else "-.--"}")

    def initializeMetaData(self, stream: MediaStream) -> None:
        self._stream = stream
        self.title.setText(self._stream.title if hasattr(self._stream, 'title') else "No title available")
        self.status_label.setText(f"0.00/{timedelta(seconds=self._stream.duration) if hasattr(self._stream, "duration") else "--:--:--"}")