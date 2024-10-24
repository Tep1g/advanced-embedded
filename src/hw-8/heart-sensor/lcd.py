from lib import st7796 #Professor Glower's st7796 driver, renamed for clarity

_RGB_BLUE = st7796.RGB(30, 144, 255)
_RGB_BLACK = st7796.RGB(0, 0, 0)
_RGB_WHITE = st7796.RGB(255,255,255)

_BPM_LABEL = "BPM: "
_BPM_LABEL_X = const()
_BPM_Y = const()
_BPM_X = _BPM_LABEL_X + 80

_T_LABEL = "T: "
_T_LABEL_X = const()
_T_Y = const()
_T_X = _T_LABEL_X + 80

_YMIN = const(10)
_YMAX = const(210)
_XMIN = const(50)
_NUM_DISPLAY_SAMPLES = const(180)
_XMAX = _XMIN + _NUM_DISPLAY_SAMPLES - 1
_MAX_U16 = const(65535)
_SCALE_FACTOR = (_YMAX - _YMIN) / _MAX_U16

class LCD:
    def __init__(self):
        self.bpm_enabled = False
        self.pulse_period_enabled = False
        self._current_bpm_string = ""
        self._current_pulse_period_string = ""
        self._sample_index = 0
        st7796.Init()
        st7796.Clear(_RGB_BLACK)
        st7796.Text2(_BPM_LABEL, _BPM_LABEL_X, _BPM_Y, _RGB_WHITE, _RGB_BLACK)

    def init_graph(self):
        st7796.Line(_XMIN, _YMIN, _XMAX, _YMIN, _RGB_WHITE)
        st7796.Line(_XMIN, _YMIN, _XMIN, _YMAX, _RGB_WHITE)

    def update_graph(self, sample_u16: float):
        x = _XMIN+self._sample_index
        y = sample_u16 * _SCALE_FACTOR
        st7796.Pixel2(x, y, _RGB_BLACK)
        st7796.Pixel2(x, y, _RGB_BLUE)
        
        self._sample_index = ((self._sample_index + 1) % _NUM_DISPLAY_SAMPLES)

    def init_bpm(self):
        st7796.Text2(_BPM_LABEL, _BPM_LABEL_X, _BPM_Y, _RGB_WHITE, _RGB_BLACK)
        self.bpm_enabled = True
        
    def update_bpm(self, bpm: float):
        clear_string = " " * len(self._current_bpm_string)
        self._current_bpm_string = "{:.2f}".format(bpm)
        st7796.Text2(clear_string, _BPM_X, _BPM_Y, _RGB_WHITE, _RGB_BLACK)
        st7796.Text2(self._current_bpm_string, _BPM_X, _BPM_Y, _RGB_WHITE, _RGB_BLACK)

    def init_pulse_period(self):
        st7796.Text2(_T_LABEL, _T_LABEL_X, _T_Y, _RGB_WHITE, _RGB_BLACK)
        self.pulse_period_enabled = True

    def update_pulse_period(self, period_s: str):
        clear_string = " " * len(self._current_pulse_period_string)
        self._current_bpm_string = period_s
        st7796.Text2(clear_string, _T_X, _T_Y, _RGB_WHITE, _RGB_BLACK)
        st7796.Text2(self._current_bpm_string, _T_X, _T_Y, _RGB_WHITE, _RGB_BLACK)
