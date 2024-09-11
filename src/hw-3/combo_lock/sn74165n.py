import time
from machine import Pin

class SN74165N():
    """
    SN74165N Shift Register
    
    :param Pin clock: Serial clock
    :param Pin load: Loads and shifts the shift register's parallel inputs
    :param Pin rx: Serial receive
    """
    def __init__(self, clk_gpio: int, ld_gpio: int, rx_gpio: int):
        self._clock = Pin(clk_gpio, Pin.OUT)
        self._load = Pin(ld_gpio, Pin.OUT)
        self._rx = Pin(rx_gpio, Pin.IN)

    def read(self) -> int:
        """Read the 8-bit input of a 74LS165 shift register using bit banging"""
        # Temporarily pull load pin down
        self._load.value(1)
        self._clock.value(0)
        time.sleep_ms(100)
        self._load.value(0)
        time.sleep_ms(100)
        self._load.value(1)
        # data is latched - now shift it in
        X = 0
        for i in range(0,8):
            self._clock.value(0)
            time.sleep_ms(100)
            X = (X << 1) + self._rx.value()
            self._clock.value(1)
            time.sleep_ms(100)
        
        return(X)
    
if __name__ == "__main__":
    """Test Script"""
    shiftreg = SN74165N(clk_gpio=10, ld_gpio=9, rx_gpio=12)
    
    try:
        print(shiftreg.read())
    
    except KeyboardInterrupt:
        pass