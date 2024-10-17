import matrix
import math
import time
from machine import Timer
from sensor import Sensor

class SensorLeastSquares:
    def __init__(self, onewire_gpio: int, sample_period_ms: int, num_samples: int, Tamb_c: float):
        self._sensor = Sensor(onewire_gpio=onewire_gpio)
        self._sample_period_s = sample_period_ms/1000
        self._Tamb_c = Tamb_c
        self._B =  [[0.01,0],[0,0.01]]
        self._Y = [[0],[0]]
        self._x = 0
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_period_ms, callback=self._sensor_handler)
        self._samples_deg_c = []
        self._sample_index = 0
        
    def _sensor_handler(self, timer: Timer):
        self._sensor._ds18b20.convert_temp()
        time.sleep_ms(750)
        temp_c = self._sensor._ds18b20.read_temp()

        self._x += self._sample_period_s
        y = math.log(temp_c - self._Tamb_c)

        matrix.add(self._B, [[self._x*self._x, self._x], [self._x, 1]])
        matrix.add(self._Y, [[self._x*y], [y]])
        Bi = matrix.inv(self._B)
        A = matrix.mult(Bi,y)
        a = A[0][0]
        b = A[1][0]
        print(self._x, a, b)