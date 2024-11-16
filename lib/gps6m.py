from machine import UART

_KNOTS_TO_M_PER_S = 0.514444

class GPS6M:
    def __init__(self, uart: UART):
        self._uart = uart

    def read_speed_m_per_s(self):
        msg = self._read_line()
        speed_knots_str = msg[46:51]

        # simpler error handling in case of invalid cast
        try:
            speed_knots = float(speed_knots_str)
        except:
            return 0.0
        
        return speed_knots * _KNOTS_TO_M_PER_S

    def _read_line(self):
        flag = 0
        msg = ''
        while(flag == 0):
            x = self._uart.read(1)
            if(x != None):
                x = ord(x)
            else:
                raise TimeoutError("No gps msg received")

            if(chr(x) == '$'):
                msg = ''
            if(x == 13):
                flag = 1
            else:
                msg = msg + chr(x)
        return(msg)