import threading

from mpv import MPV

from PySide6.QtCore import QObject, Signal, Slot

from Player.core.MpvStatus import MpvStatus

class QtMpvStatus(QObject):

    playingChanged = Signal(bool)
    pauseChanged = Signal(bool)
    time_posChanged = Signal(float)
    percent_posChanged = Signal(float)

    def __init__(self, mpv_instance: MPV, parent=None):
        super().__init__(parent)

        self._status = MpvStatus(
            instance=mpv_instance,
            on_change=self._on_change
        )
        

    def _on_change(self, name, val) -> None:
        print(f"\033[94m{name}, {val}\033[0m")
        if name == 'pause' or name == 'core-idle':
            self.playingChanged.emit(self._status.playing)
        elif name == 'percent-pos':
            self.percent_posChanged.emit(val)
        elif name == 'time-pos':
            self.time_posChanged.emit(val)
