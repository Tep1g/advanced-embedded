from machine import ADC, Pin
from motor import BidirectionalMotor

MAX_U16 = const((2 ** 16) - 1)

MIN_JS_VALUE = const(-100)
MAX_JS_VALUE = const(100)

JS_FACTOR = const(round((BidirectionalMotor.MAX_SPEED_PCT - BidirectionalMotor.MIN_SPEED_PCT) / MAX_U16))

class Joystick():
    """Joystick"""
    def __init__(self, adc_port):
        self._adc = ADC(adc_port)

    def read(self) -> int:
        value = (self._adc.read_u16() * JS_FACTOR) + BidirectionalMotor.MIN_SPEED_PCT
        return (max(min(value, BidirectionalMotor.MAX_SPEED_PCT), BidirectionalMotor.MIN_SPEED_PCT))
    
if __name__ == "__main__":
    joystick = Joystick(adc_port=1)
    while(1):
        print("Number converted from joystick: {}".format(joystick.read()))