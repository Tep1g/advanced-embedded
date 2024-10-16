from machine import Timer
from sensor import ds18x20_init

_ONEWIRE_GPIO = const(4)
_SAMPLE_PERIOD_MS = const(1000)
_SAMPLES = const(120)

class SensorRecord:
    def __init__(self, onewire_gpio: int, sample_period_ms: int, samples: int):
        (ds, address) = ds18x20_init(onewire_gpio=onewire_gpio)
        self._ds = ds
        self._ds_address = address
        self._samples = samples
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_period_ms, callback=self._sensor_handler)
        self._samples_deg_c = []
        self.is_recording = True

    def _sensor_handler(self, Timer: Timer):
        meas = self._ds.read_temp(self._ds_address)
        self._samples_deg_c.append(meas)

        # Stop recording if desired number of samples is reached
        if len(self._samples_deg_c) >= self._samples:
            self._timer.deinit()
            self.is_recording = False

if __name__ == "__main__":
    sensor = SensorRecord(onewire_gpio=_ONEWIRE_GPIO, sample_period_ms=_SAMPLE_PERIOD_MS, samples=_SAMPLES)

    # Record data
    while sensor.is_recording:
        continue
