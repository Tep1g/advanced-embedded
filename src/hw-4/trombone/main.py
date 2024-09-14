from machine import Pin, ADC, PWM

if __name__ == "__main__":
    play_btn = Pin(14, Pin.IN, Pin.PULL_UP)
    joystick = ADC(0)
    trombone = PWM(Pin(28, Pin.OUT))
    trombone.duty_u16(32768)
    
    while True:
        if play_btn.value() == 0:
            freq = int(((joystick.read_u16() / 65535) * 220) + 220)
            trombone.freq(freq)
        else:
            trombone.duty_u16(0)