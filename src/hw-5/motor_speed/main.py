import lcd
from joystick import Joystick
from motor import BidirectionalMotor

ADC_PORT = const(1)

PWM_CW_GPIO = const(16)
PWM_CCW_GPIO = const(17)

if __name__ == "__main__":
    joystick = Joystick(adc_port=ADC_PORT)
    motor = BidirectionalMotor(cw_gpio=PWM_CW_GPIO, ccw_gpio=PWM_CCW_GPIO)
    display = lcd.LCD()
    display.init()
    while (True):
        js_value = joystick.read()
        motor.set_speed_pct(js_value)
        display.update_motor_speed(js_value)