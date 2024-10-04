from machine import PWM, Pin

class UnidirectionalMotor():
    """Unidirectional Motor"""

    MIN_SPEED_PCT = const(0)
    MAX_SPEED_PCT = const(100)
    MIN_DUT_CYCLE_PCT = const(50)
    SEC_TO_NS_FLOAT = const(1_000_000_000)
    PWM_FREQ = const(20_000)
    PWM_PERIOD_NS = SEC_TO_NS_FLOAT / PWM_FREQ
    PWM_FACTOR = float(PWM_PERIOD_NS / (MAX_SPEED_PCT - MIN_DUT_CYCLE_PCT))
    PWM_OFFSET = round((float(MIN_DUT_CYCLE_PCT / MAX_SPEED_PCT)) * PWM_PERIOD_NS)
    
    def __init__(self, pwm_gpio: int):
        self._pwm = PWM(Pin(pwm_gpio, Pin.OUT))
        self._pwm.duty_ns(0)
        self._pwm.freq(self.PWM_FREQ)

    def set_speed_pct(self, speed_pct: int):
        if not (self.MIN_SPEED_PCT <= speed_pct <= self.MAX_SPEED_PCT):
            raise ValueError("Invalid unidirectional speed percentage: {}, must be within {} and {} inclusive.".format(speed_pct, self.MIN_SPEED_PCT, self.MAX_SPEED_PCT))
        
        # DC motor doesn't spin below 50% duty cycle
        # Current work around is to scale and offset it
        self._pwm.duty_ns(round(speed_pct * self.PWM_FACTOR) + self.PWM_OFFSET)
    
    def turn_off(self):
        self._pwm.duty_ns(0)

class BidirectionalMotor():
    """Bidirectional Motor"""
    MIN_BI_SPEED_PCT = -UnidirectionalMotor.MAX_SPEED_PCT
    MAX_BI_SPEED_PCT = UnidirectionalMotor.MAX_SPEED_PCT
    
    def __init__(self, cw_gpio: int, ccw_gpio: int):
        self._cw = UnidirectionalMotor(pwm_gpio=cw_gpio)
        self._ccw = UnidirectionalMotor(pwm_gpio=ccw_gpio)

    def set_speed_pct(self, speed_pct: int):
        if not (self.MIN_BI_SPEED_PCT <= speed_pct <= self.MAX_BI_SPEED_PCT):
            raise ValueError("Invalid bidirectional speed percentage: {}, must be within {} and {} inclusive.".format(speed_pct, self.MIN_BI_SPEED_PCT, self.MAX_BI_SPEED_PCT))

        if speed_pct < 0:
            self._cw.turn_off()
            self._ccw.set_speed_pct(abs(speed_pct))
        else:
            self._ccw.turn_off()
            self._cw.set_speed_pct(speed_pct)

if __name__ == "__main__":
    """Test Script"""
    motor = BidirectionalMotor(cw_gpio=16, ccw_gpio=17)
    while (True):
        motor.set_speed_pct(int(input("Set DC servo motor speed percentage: ".format(motor.MIN_BI_SPEED_PCT, motor.MAX_BI_SPEED_PCT))))