from machine import Pin, PWM

def update_servo_angle(servo: PWM, angle: int):
    duty_cycle_ns = int(((angle/135) * 1_000_000) + 500_000)
    servo.duty_ns(duty_cycle_ns)

if __name__ == "__main__":
    """Test Script"""
    servo = PWM(Pin(28, Pin.OUT))
    while True:
        angle = int(input("Enter new servo angle: "))
        update_servo_angle(servo, angle)