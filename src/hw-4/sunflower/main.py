import time
from servo import ServoMotor
from sensor import LightSensor

LDR_ADC_GPIO = 28
SERVO_PWM_GPIO = 22
SERVO_SPEED_HZ = 50
ANGLE_RES = 15

if __name__ == "__main__":
    light_sensor = LightSensor(adc_pin=LDR_ADC_GPIO)
    servo_motor = ServoMotor(pwm_gpio=SERVO_PWM_GPIO)
    servo_motor.set_speed(SERVO_SPEED_HZ)
    angle = ServoMotor.MIN_ANGLE
    lowest_voltage = 100

    while angle <= ServoMotor.MAX_ANGLE:
        servo_motor.set_angle(angle)
        time.sleep_ms(500)
        voltage = light_sensor.read_voltage()
        print("Angle: {} deg, Voltage: {:.2f}V".format(angle, voltage))

        # Pull-down LDR
        if voltage < lowest_voltage:
            lowest_voltage = voltage
            best_angle = angle
        angle += ANGLE_RES
    
    servo_motor.set_angle(best_angle)
    print("Most optimal angle: {}".format(best_angle))