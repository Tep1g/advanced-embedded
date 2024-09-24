from machine import Pin, PWM

class ServoMotor():
    """Servo Motor"""

    MIN_FREQ_HZ = 50
    MAX_FREQ_HZ = 330

    MIN_ANGLE = 0
    MAX_ANGLE = 270
    _MIN_PW_NS = 500_000
    _MAX_PW_NS = 2_500_000

    _PW_FACTOR = (_MAX_PW_NS - _MIN_PW_NS) / MAX_ANGLE

    def __init__(self, pwm_gpio: int):
        """
        Initialize the ServoMotor object
        
        :param int pwm_gpio: PWM GPIO pin
        """
        self._pwm = PWM(Pin(pwm_gpio, Pin.OUT))

    def set_speed(self, freq_hz: int):
        """
        Set the servo speed by passing a PWM frequency
        
        :param int freq_hz: Between 50Hz (slowest) and 330Hz (fastest)
        """
        if not (self.MIN_FREQ_HZ <= freq_hz <= self.MAX_FREQ_HZ):
            raise ValueError("Invalid frequency for servo speed control: {}, must be between {} and {} inclusive".format(freq_hz, self.MIN_FREQ_HZ, self.MAX_FREQ_HZ))

        self._pwm.freq(freq_hz)

    def set_angle(self, angle_deg: int):
        """
        Set the servo angle
         
        :param int angle_deg: Must be between 0 and 270 degrees
        """
        if not (self.MIN_ANGLE <= angle_deg <= self.MAX_ANGLE):
            raise ValueError("Invalid servo angle: {}, must be between {} and {} inclusive".format(angle_deg, self.MIN_ANGLE, self.MAX_ANGLE))

        duty_cycle_ns = int((angle_deg) * self._PW_FACTOR) + self._MIN_PW_NS
        duty_cycle_ns = max(min(duty_cycle_ns, self._MAX_PW_NS), self._MIN_PW_NS)
        self._pwm.duty_ns(duty_cycle_ns)

if __name__ == "__main__":
    """Test Script"""
    servo = ServoMotor(pwm_gpio=22)
    servo.set_speed(freq_hz=50)
    while True:
        angle = int(input("Enter new servo angle: "))
        servo.set_angle(angle)