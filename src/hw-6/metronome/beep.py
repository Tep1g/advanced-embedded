from machine import Pin, PWM, Timer
from time import ticks_us

_DUTY_ON_U16 = round(((2 ** 16) - 1) / 2)
_DUTY_OFF_U16 = const(0)

class Beeper:
    def __init__(self, quiet_period_ms: int, beep_length_ms: int, beep_freq: int, beep_gpio: int):
        self.quiet_period_ms = quiet_period_ms
        self._beep_length_ms = beep_length_ms
        self._pwm = PWM(Pin(beep_gpio, Pin.OUT), freq=beep_freq, duty_u16=_DUTY_OFF_U16)
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.ONE_SHOT, period=self.quiet_period_ms, callback=self._start_beep_handler)

    def _start_beep_handler(self, timer: Timer):
        self._pwm.duty_u16(_DUTY_ON_U16)
        timer.init(mode=Timer.ONE_SHOT, period=self._beep_length_ms, callback=self._stop_beep_handler)

    def _stop_beep_handler(self, timer: Timer):
        self._pwm.duty_u16(_DUTY_OFF_U16)
        timer.init(mode=Timer.ONE_SHOT, period=self.quiet_period_ms, callback=self._start_beep_handler)

if __name__ == "__main__":
    """Rough test script for measuring quiet period between beeps"""
    beeper = Beeper(quiet_period_ms=1000, beep_length_ms=10, beep_freq=500, beep_gpio=28)
    got_start_ticks = False
    got_stop_ticks = False
    while (True):
        if ((beeper._pwm.duty_u16() == 0) and (not got_start_ticks)):
            start_ticks_us = ticks_us()
            got_start_ticks = True
            got_stop_ticks = False

        elif ((beeper._pwm.duty_u16() != 0) and (not got_stop_ticks)):
            print(ticks_us()-start_ticks_us)
            got_stop_ticks = True
            got_start_ticks = False