import lcd
from joystick import Joystick
from motor import BidirectionalMotor

if __name__ == "__main__":
    joystick = Joystick(adc_port=1)
    motor = BidirectionalMotor(cw_gpio=16, ccw_gpio=17, freq_hz=20_000)
    lcd.init()
    while (True):
        js_value = joystick.read()
        motor.set_speed_pct(js_value)
        lcd.update_motor_speed(js_value)