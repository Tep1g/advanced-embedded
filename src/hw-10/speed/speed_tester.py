import st7796
from gps6m import GPS6M
from machine import Pin, Timer

_READ_PERIOD_MS = const(100)

_RGB_BLACK = st7796.RGB(0, 0, 0)
_RGB_WHITE = st7796.RGB(255, 255, 255)

class SpeedTester:
    def __init__(self, gps: GPS6M, start_button: Pin, stop_button: Pin):
        self._gps = gps
        self._top_speeds = [0.0, 0.0, 0.0]
        self._recording_top_speed = 0.0
        st7796.Init()
        st7796.Clear(_RGB_BLACK)
        self._start_button = start_button
        self._stop_button = stop_button
        self._read_timer = Timer()
        self._start_button.irq(trigger=Pin.IRQ_FALLING, handler=self._start_handler)
        self._stop_button.irq(trigger=Pin.IRQ_FALLING, handler=self._stop_handler)

    def _start_handler(self, pin: Pin):
        self._read_timer.init(mode=Timer.PERIODIC, period=_READ_PERIOD_MS, callback=self._read_handler)

    def _stop_handler(self, pin: Pin):
        self._read_timer.deinit()
        lowest_top_speed = min(self._top_speeds)
        index = self._top_speeds.index(lowest_top_speed)
        if self._recording_top_speed > self._top_speeds[index]:
            self._top_speeds[index] = self._recording_top_speed

        # Reset top speed for the next recording
        self._recording_top_speed = 0.0
        self._update_lcd()

    def _update_lcd(self):
        offset = 0
        for i in range(len(self._top_speeds)):
            st7796.Text2("     ", 0, offset, _RGB_WHITE, _RGB_BLACK)
            speed_str = str(self._top_speeds[i])
            st7796.Text2(speed_str, 0, offset, _RGB_WHITE, _RGB_BLACK)

            offset += 50

    def _read_handler(self, timer: Timer):
        speed = self._gps.try_read_speed_m_per_s()
        if speed > self._recording_top_speed:
            self._recording_top_speed = speed