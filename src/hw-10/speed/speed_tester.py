from gps6m import GPS6M
from machine import Pin, Timer

_READ_PERIOD_MS = const(100)

class SpeedTester:
    def __init__(self, gps: GPS6M, start_button: Pin, stop_button: Pin):
        self._gps = gps
        self._top_speeds = [0.0, 0.0, 0.0]
        self._recording_top_speed = 0.0
        self._start_button = start_button
        self._stop_button = stop_button
        self._read_timer = Timer()
        self._start_button.irq(trigger=Pin.IRQ_FALLING, handler=self._start_handler)
        self._stop_button.irq(trigger=Pin.IRQ_FALLING, handler=self._stop_handler)

    def _start_handler(self, pin: Pin):
        self._read_timer.init(mode=Timer.PERIODIC, period=_READ_PERIOD_MS, callback=self._read_handler)

    def _stop_handler(self, pin: Pin):
        self._read_timer.deinit()
        for i in range(len(self._top_speeds)):
            if self._recording_top_speed > self._top_speeds[i]:
                self._top_speeds[i] = self._recording_top_speed
                break

        # Reset top speed for the next recording
        self._recording_top_speed = 0.0

    def _read_handler(self, timer: Timer):
        speed = self._gps.read_speed_m_per_s()
        if speed > self._recording_top_speed:
            self._recording_top_speed = speed