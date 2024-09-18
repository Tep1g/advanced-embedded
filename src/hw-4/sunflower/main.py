import time
from servo import ServoMotor
from sensor import LightSensor

if __name__ == "__main__":
    light_sensor = LightSensor(adc_port=2)
    servo = ServoMotor(pwm_gpio=28)
    servo.set_speed(50)
    angle = 135
    last_voltage = light_sensor.read_voltage()
    increase_angle = True
    while True:
        if increase_angle:
            angle += 3
        else:
            angle -= 3
        angle = max(min(angle, 270), 0)
        servo.set_angle(angle)
        time.sleep_ms(1)
        new_voltage = light_sensor.read_voltage()
        if new_voltage < last_voltage:
            increase_angle = not increase_angle
        last_voltage = new_voltage
        print("Current voltage: {:.2f}, Current angle {}".format(new_voltage, angle))