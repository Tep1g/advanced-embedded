import matrix
import math
from machine import Timer
from sensor import Sensor

_ONEWIRE_GPIO = const(4)
_SAMPLE_PERIOD_MS = const(1000)
_T_AMB_C = const(27.0)

class SensorLeastSquares:
    def __init__(self, onewire_gpio: int, sample_period_ms: int, t_amb_c: float):
        self._sensor = Sensor(onewire_gpio=onewire_gpio)
        self._sample_period_s = sample_period_ms/1000
        self._t_amb_c = t_amb_c
        self._b_matrix =  [[0.01,0],[0,0.01]]
        self._y_matrix = [[0],[0]]
        self._x = 0
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_period_ms, callback=self._sensor_handler)
        
    def _sensor_handler(self, timer: Timer):
        temp_c = self._sensor.read_temp()

        self._x += self._sample_period_s
        y = math.log(temp_c - self._t_amb_c)

        b_matrix = matrix.add(self._b_matrix, [[self._x*self._x, self._x], [self._x, 1]])
        y_matrix = matrix.add(self._y_matrix, [[self._x*y], [y]])
        b_matrix_inverse = matrix.inv(b_matrix)
        a_matrix = matrix.mult(b_matrix_inverse, y_matrix)
        a = abs(a_matrix[0][0])
        b = math.exp(a_matrix[1][0])
        tc = 1/a
        self._b_matrix = b_matrix
        self._y_matrix = y_matrix
        print("Current Temp: {}".format(temp_c))
        print("Time: {}\na: {}\nb: {}\nTC: {}".format(self._x, a, b, tc))

if __name__ == "__main__":
    least_squares = SensorLeastSquares(onewire_gpio=_ONEWIRE_GPIO, sample_period_ms=_SAMPLE_PERIOD_MS, t_amb_c=_T_AMB_C)

    while True:
        continue