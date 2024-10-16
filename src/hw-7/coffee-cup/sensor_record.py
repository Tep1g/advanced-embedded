import time
import st7796
from machine import Timer
from sensor import ds18x20_init

_ONEWIRE_GPIO = const(4)
_SAMPLE_PERIOD_MS = const(1000)
_NUM_SAMPLES = const(120)

_BLUE_RGB = st7796.RGB(30, 144, 255)
_BLACK_RGB = st7796.RGB(0, 0, 0)
_WHITE_RGB = st7796.RGB(255,255,255)

_YMIN = const(10)
_YMAX = const(210)
_Y0 = ((_YMAX - _YMIN) / 2) + _YMIN
_XMIN = const(50)

class SensorRecord:
    def __init__(self, onewire_gpio: int, sample_period_ms: int, num_samples: int):
        (ds, address) = ds18x20_init(onewire_gpio=onewire_gpio)
        self._ds = ds
        self._ds_address = address
        self._max_samples = num_samples
        self.init_display()
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_period_ms, callback=self._sensor_handler)
        self._samples_deg_c = []
        self.is_recording = True

    def init_display(self):
        st7796.Init()
        st7796.Clear(_BLACK_RGB)
        st7796.Line(_XMIN, _Y0, _XMIN+self._max_samples, _Y0, _WHITE_RGB)
        st7796.Line(_XMIN, _YMIN, _XMIN, _YMAX, _WHITE_RGB)

    def _sensor_handler(self, Timer: Timer):
        self._ds.convert_temp()
        time.sleep_ms(750)
        meas = self._ds.read_temp(self._ds_address)
        self._samples_deg_c.append(meas)

        # Stop recording if desired number of samples is reached
        if len(self._samples_deg_c) >= self._max_samples:
            self._timer.deinit()
            self.is_recording = False

        

if __name__ == "__main__":
    record = SensorRecord(onewire_gpio=_ONEWIRE_GPIO, sample_period_ms=_SAMPLE_PERIOD_MS, num_samples=_NUM_SAMPLES)

    # Record data
    while record.is_recording:
        continue
