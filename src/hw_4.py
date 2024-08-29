from machine import Pin, ADC, PWM
import time

def trombone():

    play_btn = Pin(14, Pin.IN, Pin.PULL_UP)
    joystick = ADC(0)
    trombone = PWM(Pin(28, Pin.OUT))
    trombone.duty_u16(32768)
    try:
        while True:
            if play_btn.value() == 0:
                freq = int(((joystick.read_u16() / 65535) * 220) + 220)
                trombone.freq(freq)
            else:
                trombone.duty_u16(0)
    except:
        return "Exited Successfully"
    
def sunflower():

    def read_voltage(adc: ADC):
        return (adc.read_u16() * 3.3 / 65535)
    
    def update_servo_angle(servo: PWM, angle: int):
        duty_cycle_ns = int(((angle/135) * 1_000_000) + 500_000)
        servo.duty_ns(duty_cycle_ns)

    light = ADC(2)
    servo = PWM(Pin(28, Pin.OUT))
    servo.freq(50)
    angle = 135
    last_voltage = read_voltage(light)
    increase_angle = True
    try:
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

    except:
        return "Exited Successfully"
    