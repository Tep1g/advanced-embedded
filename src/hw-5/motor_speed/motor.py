from machine import PWM, Pin

SEC_TO_NS_FLOAT = const(1_000_000_000.0)

MIN_SPEED_PCT = const(0)
MAX_SPEED_PCT = const(100)

class MonodirectionalMotor():
    def __init__(self, pwm_gpio: int, freq_hz: int):
        self._pwm = PWM(Pin(pwm_gpio, Pin.OUT))
        self._pwm.duty_ns(0)
        self._pwm.freq(freq_hz)
        self._duty_ns = round(SEC_TO_NS_FLOAT / freq_hz)

    def set_freq(self, freq_hz: int):
        self._duty_ns = round(SEC_TO_NS_FLOAT / freq_hz)
        self._pwm.freq(freq_hz)

    def set_speed(self, speed_pct: float):
        if not (MIN_SPEED_PCT <= speed_pct <= MAX_SPEED_PCT):
            raise ValueError("Invalid speed percentage: {}, must be within {} and {} inclusive.".format(speed_pct, MIN_SPEED_PCT, MAX_SPEED_PCT))
        
        self._pwm.duty_ns(round(self._duty_ns * speed_pct))

class BidirectionalMotor():
    def __init__(self, cw_gpio: int, ccw_gpio: int, freq_hz: int):
        self.cw_motor = MonodirectionalMotor(pwm_gpio=cw_gpio, freq_hz=freq_hz)
        self.ccw_motor = MonodirectionalMotor(pwm_gpio=ccw_gpio, freq_hz=freq_hz)