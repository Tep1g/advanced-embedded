import st7796 #Professor Glower's st7796 driver, renamed for clarity
from beep import Beeper

_RGB_BLACK = st7796.RGB(0,0,0)
_RGB_WHITE = st7796.RGB(255, 255, 255)
_MINUTE_TO_MS = const(60_000)
_BPM_LABEL = const("BPM: ")
_LABEL_X = const(120)
_X_TEXT = const(200)
_Y_TEXT = const(160)

class LCD:
    def __init__(self, beeper: Beeper):
        self._beeper = beeper
        self._current_bpm = ""
        st7796.Init()
        st7796.Clear(_RGB_BLACK)
        st7796.Text2(_BPM_LABEL, _LABEL_X, _Y_TEXT, _RGB_WHITE, _RGB_BLACK)

    def update_display(self):
        quiet_period_ms = self._beeper.quiet_period_ms
        if quiet_period_ms > 0:
            bpm = str(round(_MINUTE_TO_MS / quiet_period_ms))
        else:
            bpm = "Inf"

        if self._current_bpm != bpm:
            clear_string = " " * len(self._current_bpm)
            st7796.Text2(clear_string, _X_TEXT, _Y_TEXT, _RGB_WHITE, _RGB_BLACK)
            st7796.Text2(bpm, _X_TEXT, _Y_TEXT, _RGB_WHITE, _RGB_BLACK)

        self._current_bpm = bpm