from machine import PWM, Pin, Timer

_DUTY_ON_U16 = const(32768)

class Beeper:
    def __init__(self, beeper_gpio: int, beep_period_ms: int, led_gpio: int):
        self._beep_period_ms = beep_period_ms
        self._pwm = PWM(Pin(beeper_gpio, Pin.OUT))
        self._led = Pin(led_gpio, Pin.OUT)
        self._timer = Timer(-1)

    def start_beep(self):
        self._pwm.duty_u16(_DUTY_ON_U16)
        self._led.value(1)
        self._timer.init(mode=Timer.ONE_SHOT, period=self._beep_period_ms, callback=self._stop_beep_handler)

    def _stop_beep_handler(self, timer: Timer):
        self._pwm.duty_u16(0)
        self._led.value(0)