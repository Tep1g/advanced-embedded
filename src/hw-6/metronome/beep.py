from machine import Pin, PWM, Timer

_DUTY_ON_NS = const(500_000_000)
_DUTY_OFF_NS = const(0)

class Beeper:
    def __init__(self, init_wait_period_ms: int, beep_width_ms: int, beep_freq: int, beep_gpio: int):
        self.wait_period_ms = init_wait_period_ms
        self._beep_width_ms = beep_width_ms
        self._beeper = PWM(dest=Pin(beep_gpio, Pin.OUT), freq=beep_freq, duty_ns=_DUTY_OFF_NS)
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=self.wait_period_ms, callback=self._start_beep_handler)

    def _start_beep_handler(self, timer: Timer):
        self._beeper.duty_ns(_DUTY_ON_NS)
        timer.init(mode=Timer.PERIODIC, period=self._beep_width_ms, callback=self._stop_beep_handler)

    def _stop_beep_handler(self, timer: Timer):
        self._beeper.duty_ns(_DUTY_OFF_NS)
        timer.init(mode=Timer.PERIODIC, period=self.wait_period_ms, callback=self._start_beep_handler)