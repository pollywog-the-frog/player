from mpv import MPV

class MpvStatus():
    def __init__(self, instance: MPV, on_change=None):
        # Add instance to self
        self._player: MPV = instance

        # Add on_change to self
        self._on_change_prop = on_change

        # Setup observers
        _observe=[
            'time-pos',
            'percent-pos',
            'duration',
            'remaining',
            'pause',
            'volume',
            'core-idle',
            ]
        self._setup_observers(_observe)

    def _setup_observers(self, to_observe) -> None:
        for prop in to_observe:
            self._player.observe_property(prop, self._on_change)

    def _on_change(self, name, val) -> None:
        if self._on_change_prop is not None:
            self._on_change_prop(name, val)
   
    @property
    def playing(self) -> bool:
        return not self._player.pause and not self._player.core_idle

    @property
    def pause(self) -> bool:
        return bool(getattr(self._player, "pause", False))

    @property
    def time_pos(self) -> float:
        return float(getattr(self._player, "time_pos", 0.0) or 0.0)

    @property
    def duration(self) -> float:
        return float(getattr(self._player, "duration", 0.0) or 0.0)

    @property
    def percent_pos(self) -> int:
        return float(getattr(self._player, "percent_pos", 0.0) or 0.0)

    @property
    def remaining(self) -> float:
        return float(getattr(self._player, "remaining", 0.0) or 0.0)

    @property
    def volume(self) -> float:
        return float(getattr(self._player, "volume", 0.0) or 0.0)