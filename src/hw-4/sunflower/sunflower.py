import time
from machine import Pin, ADC, PWM
from servo import update_servo_angle
from sense import read_voltage

if __name__ == "__main__":
    light = ADC(2)
    servo = PWM(Pin(28, Pin.OUT))
    servo.freq(50)
    angle = 135
    last_voltage = read_voltage(light)
    increase_angle = True
    while True:
        if increase_angle:
            angle += 3
        else:
            angle -= 3
        angle = max(min(angle, 270), 0)
        update_servo_angle(servo, angle)
        time.sleep_ms(1)
        new_voltage = read_voltage(light)
        if new_voltage < last_voltage:
            increase_angle = not increase_angle
        last_voltage = new_voltage
        print("Current voltage: {:.2f}, Current angle {}".format(new_voltage, angle))