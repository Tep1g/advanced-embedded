from machine import UART

_KNOTS_TO_M_PER_S = 0.514444

class GPS6M:
    def __init__(self, uart: UART):
        self._uart = uart

    def read_speed_m_per_s(self):
        msg = self._uart.readline()
        if msg != None:
            speed_knots_str = msg[46:51]
            return float(speed_knots_str) * _KNOTS_TO_M_PER_S
        else:
            raise TimeoutError("No gps msg received")
