from machine import ADC, Pin
from motor import BidirectionalMotor

_MAX_U16 = const((2 ** 16) - 1)
_JS_FACTOR = (BidirectionalMotor.MAX_BI_SPEED_PCT - BidirectionalMotor.MIN_BI_SPEED_PCT) / _MAX_U16

class Joystick():
    """Joystick"""
    def __init__(self, adc_port):
        self._adc = ADC(adc_port)

    def read(self) -> int:
        value = round((self._adc.read_u16() * _JS_FACTOR) + BidirectionalMotor.MIN_BI_SPEED_PCT)
        return (max(min(value, BidirectionalMotor.MAX_BI_SPEED_PCT), BidirectionalMotor.MIN_BI_SPEED_PCT))
    
if __name__ == "__main__":
    joystick = Joystick(adc_port=1)
    while(1):
        print("Number converted from joystick: {}".format(joystick.read()))