from machine import Timer
from sensor import ds18x20_init

SENSOR_RX_GPIO = const(4)

class SensorRecord:
    def __init__(self, sample_period_ms: int, samples: int):
        (ds, address) = ds18x20_init()
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
    sensor = SensorRecord(1000, 120)
    while sensor.is_recording:
        continue