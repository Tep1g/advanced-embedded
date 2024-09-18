from machine import Pin, PWM

_MIN_FREQ_HZ = 50
_MAX_FREQ_HZ = 330

_MIN_PW_NS = 500_000
_MAX_PW_NS = 2_500_000
_MIN_ANGLE = 0
_MAX_ANGLE = 270

_PW_FACTOR = (_MAX_PW_NS - _MIN_PW_NS) / _MAX_ANGLE

class ServoMotor():
    """Servo Motor"""
    def __init__(self, pwm_gpio: int):
        self._pwm = PWM(Pin(pwm_gpio, Pin.OUT))

    def set_speed(self, freq_hz: int):
        """
        Set the servo speed by passing a frequency
        
        :param int freq_hz: Between 50Hz (slowest) and 330Hz (fastest)"""
        if not (_MIN_FREQ_HZ <= freq_hz <= _MAX_FREQ_HZ):
            raise ValueError("Invalid frequency for servo speed control: {}, must be between {} and {} inclusive".format(freq_hz, _MIN_FREQ_HZ, _MAX_FREQ_HZ))

        self._pwm.freq(freq_hz)

    def set_angle(self, angle_deg: int):
        """
        Set the servo angle
         
        :param int angle_deg: Must be between 0 and 270 degrees
        """
        if not (_MIN_ANGLE <= angle_deg <= _MAX_ANGLE):
            raise ValueError("Invalid servo angle: {}, must be between {} and {} inclusive".format(angle_deg, _MIN_ANGLE, _MAX_ANGLE))

        duty_cycle_ns = int((angle_deg) * _PW_FACTOR) + _MIN_PW_NS
        duty_cycle_ns = max(min(duty_cycle_ns, _MAX_PW_NS), _MIN_PW_NS)
        self._pwm.duty_ns(duty_cycle_ns)

if __name__ == "__main__":
    """Test Script"""
    servo = ServoMotor(pwm_gpio=28)
    servo.set_speed(freq_hz=50)
    while True:
        angle = int(input("Enter new servo angle: "))
        servo.set_angle(angle)