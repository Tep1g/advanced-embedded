from machine import Pin, ADC, PWM
from math import ceil

MAX_U16 = (2 ** 16) - 1
HALF_U16 = ceil(MAX_U16 / 2)

MIN_FREQ = 220
MAX_FREQ = 440

FREQ_FACTOR = ((MAX_FREQ - MIN_FREQ) / MAX_U16)

BUTTON_GPIO = 14
ADC_PORT = 0
SPEAKER_GPIO = 28

if __name__ == "__main__":
    play_btn = Pin(BUTTON_GPIO, Pin.IN, Pin.PULL_UP)
    joystick = ADC(ADC_PORT)
    trombone = PWM(Pin(SPEAKER_GPIO, Pin.OUT))
    trombone.duty_u16(0)
    trombone_is_on = False
    
    while True:
        if play_btn.value() == 0:
            freq = int(joystick.read_u16() * FREQ_FACTOR) + MIN_FREQ
            trombone.freq(freq)
            if not trombone_is_on:
                trombone.duty_u16(HALF_U16)
                trombone_is_on = True
        
        elif trombone_is_on:
            trombone.duty_u16(0)
            trombone_is_on = False