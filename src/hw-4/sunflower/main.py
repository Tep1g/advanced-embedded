import time
from servo import ServoMotor
from sensor import LightSensor

LDR_ADC_PORT = 2
PWM_GPIO = 28
SERVO_SPEED_HZ = 50

if __name__ == "__main__":
    light_sensor = LightSensor(adc_port=LDR_ADC_PORT)
    servo_motor = ServoMotor(pwm_gpio=PWM_GPIO)
    servo_motor.set_speed(SERVO_SPEED_HZ)
    angle = 135
    last_voltage = light_sensor.read_voltage()
    increase_angle = True
    while True:
        if increase_angle:
            angle += 3
        else:
            angle -= 3
        angle = max(min(angle, ServoMotor.MAX_ANGLE), ServoMotor.MAX_ANGLE)
        servo_motor.set_angle(angle)
        time.sleep_ms(1)
        new_voltage = light_sensor.read_voltage()
        if new_voltage < last_voltage:
            increase_angle = not increase_angle
        last_voltage = new_voltage
        print("Current voltage: {:.2f}, Current angle {}".format(new_voltage, angle))