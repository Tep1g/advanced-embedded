from machine import ADC, Pin

MAX_U16 = const((2 ** 16) - 1)

MIN_JS_VALUE = const(-100)
MAX_JS_VALUE = const(100)

JS_FACTOR = const(round((MAX_JS_VALUE - MIN_JS_VALUE) / MAX_U16))

class Joystick():
    """Joystick"""
    def __init__(self, adc_port):
        self._adc = ADC(adc_port)

    def read(self) -> int:
        value = (self._adc.read_u16() * JS_FACTOR) + MIN_JS_VALUE
        return (max(min(value, MAX_JS_VALUE), MIN_JS_VALUE))
    
if __name__ == "__main__":
    joystick = Joystick(adc_port=1)
    while(1):
        print("Number converted from joystick: {}".format(joystick.read()))