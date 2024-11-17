from machine import UART

_KNOTS_TO_M_PER_S = 0.514444

class GPS6M:
    def __init__(self, uart: UART):
        self._uart = uart

    def read_speed_m_per_s(self):
        # simpler error handling in case of invalid cast
        try:
            msg = self._read_line()
            msg_values = msg.split(',')
            if msg_values[0] == "$GPRMC":
                return (float(msg_values[7]) * _KNOTS_TO_M_PER_S)
            else:
                raise Exception

        except:
            return 0.0

    def _read_line(self):
        flag = 0
        msg = ''
        while(flag == 0):
            x = self._uart.read(1)
            if(x != None):
                x = ord(x)
            else:
                raise Exception("No gps msg received")

            if(chr(x) == '$'):
                msg = ''
            if(x == 13):
                flag = 1
            else:
                msg = msg + chr(x)
        return(msg)