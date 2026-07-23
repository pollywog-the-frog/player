from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QSlider

from mpv import MPV

class VideoSlider(QSlider): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMaximum(10**8)

        self.sliderReleased.connect(self._on_release)


    def _on_release(self):
        self.window().controls.seek(self.value()/(self.maximum()/10**2))