import matrix
import math
import time
from machine import Timer
from sensor import Sensor

_ONEWIRE_GPIO = const(4)
_SAMPLE_PERIOD_MS = const(1000)
_T_AMB_C = 25

class SensorLeastSquares:
    def __init__(self, onewire_gpio: int, sample_period_ms: int, t_amb_c: float):
        self._sensor = Sensor(onewire_gpio=onewire_gpio)
        self._sample_period_s = sample_period_ms/1000
        self._t_amb_c = t_amb_c
        self._B =  [[0.01,0],[0,0.01]]
        self._Y = [[0],[0]]
        self._x = 0
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_period_ms, callback=self._sensor_handler)
        
    def _sensor_handler(self, timer: Timer):
        self._sensor._ds18b20.convert_temp()
        time.sleep_ms(750)
        temp_c = self._sensor._ds18b20.read_temp()

        self._x += self._sample_period_s
        y = math.log(temp_c - self._t_amb_c)

        matrix.add(self._B, [[self._x*self._x, self._x], [self._x, 1]])
        matrix.add(self._Y, [[self._x*y], [y]])
        Bi = matrix.inv(self._B)
        A = matrix.mult(Bi,y)
        a = A[0][0]
        b = A[1][0]
        print(self._x, a, b)

if __name__ == "__main__":
    least_squares = SensorLeastSquares(onewire_gpio=_ONEWIRE_GPIO, sample_period_ms=_SAMPLE_PERIOD_MS, t_amb_c=_T_AMB_C)

    while True:
        continue