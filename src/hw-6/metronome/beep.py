from machine import Pin, PWM, Timer

_DUTY_ON_U16 = round(((2 ** 16) - 1) / 2)
_DUTY_OFF_U16 = const(0)

class Beeper:
    def __init__(self, between_beeps_ms: int, beep_length_ms: int, beep_freq: int, beep_gpio: int):
        self.between_beeps_ms = between_beeps_ms
        self._beep_length_ms = beep_length_ms
        self._beeper = PWM(Pin(beep_gpio, Pin.OUT), freq=beep_freq, duty_u16=_DUTY_OFF_U16)
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.ONE_SHOT, period=self.between_beeps_ms, callback=self._start_beep_handler)

    def _start_beep_handler(self, timer: Timer):
        self._beeper.duty_u16(_DUTY_ON_U16)
        timer.init(mode=Timer.ONE_SHOT, period=self._beep_length_ms, callback=self._stop_beep_handler)

    def _stop_beep_handler(self, timer: Timer):
        self._beeper.duty_u16(_DUTY_OFF_U16)
        timer.init(mode=Timer.ONE_SHOT, period=self.between_beeps_ms, callback=self._start_beep_handler)

if __name__ == "__main__":
    """Test Script"""
    beeper = Beeper(between_beeps_ms=1000, beep_length_ms=10, beep_freq=500, beep_gpio=28)
    while (True):
        continue
