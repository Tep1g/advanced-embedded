import st7796 #Professor Glower's st7796 driver, renamed for clarity

_RGB_BLUE = st7796.RGB(30, 144, 255)
_RGB_BLACK = st7796.RGB(0, 0, 0)
_RGB_WHITE = st7796.RGB(255,255,255)

_BPM_LABEL = "BPM: "
_BPM_LABEL_X = const(0)
_BPM_Y = const(320)
_BPM_X = _BPM_LABEL_X + 80

_T_LABEL = "T: "
_T_LABEL_X = const(0)
_T_Y = const(280)
_T_X = _T_LABEL_X + 80

_Y_RES = const(320)
_YMIN = const(10)
_YMAX = const(210)
_XMIN = const(15)
NUM_DISPLAY_SAMPLES = const(450)
_XMAX = _XMIN + NUM_DISPLAY_SAMPLES - 1
_MAX_ADC = const(62500)
_MIN_ADC = const(18000)
_SCALE_FACTOR = (_YMAX - _YMIN) / (_MAX_ADC - _MIN_ADC)

class LCD:
    def __init__(self):
        self._bpm_enabled = False
        self._pulse_period_enabled = False
        self._graph_enabled = False
        st7796.Init()
        st7796.Clear(_RGB_BLACK)

    def init_graph(self):
            st7796.Line(_XMIN, (_Y_RES - _YMIN), _XMAX, (_Y_RES - _YMIN), _RGB_WHITE)
            st7796.Line(_XMIN, (_Y_RES - _YMIN), _XMIN, (_Y_RES - _YMAX), _RGB_WHITE)
            self._graph_enabled = True

    def graph_samples(self, samples_u16: list[int]):
        if self._graph_enabled:
            num_samples = len(samples_u16)
            for i in range(0, num_samples):
                x = _XMIN+i
                y = ((samples_u16[i] - _MIN_ADC) * _SCALE_FACTOR)
                y += _YMIN
                st7796.Pixel2(x, (_Y_RES - y), _RGB_BLUE)

    def init_bpm(self):
        st7796.Text2(_BPM_LABEL, _BPM_LABEL_X, (_Y_RES - _BPM_Y), _RGB_WHITE, _RGB_BLACK)
        self._bpm_enabled = True
        
    def set_bpm(self, bpm: float):
        if self._bpm_enabled:
            bpm_string = "{:.2f}".format(bpm)
            st7796.Text2(bpm_string, _BPM_X, (_Y_RES - _BPM_Y), _RGB_WHITE, _RGB_BLACK)

    def init_pulse_period(self):
        st7796.Text2(_T_LABEL, _T_LABEL_X, (_Y_RES - _T_Y), _RGB_WHITE, _RGB_BLACK)
        self._pulse_period_enabled = True

    def set_pulse_period(self, period_us: int):
        if self._pulse_period_enabled:
            period_us_string = "{} us".format(period_us)
            st7796.Text2(period_us_string, _T_X, (_Y_RES - _T_Y), _RGB_WHITE, _RGB_BLACK)