from machine import Pin, ADC, PWM
from math import ceil

MAX_U16 = (2 ** 16) - 1

MIN_FREQ = 220
MAX_FREQ = 440

FREQ_RANGE = MAX_FREQ - MIN_FREQ

BUTTON_GPIO = 14
ADC_PORT = 0
BUZZER_GPIO = 28

if __name__ == "__main__":
    play_btn = Pin(BUTTON_GPIO, Pin.IN, Pin.PULL_UP)
    joystick = ADC(ADC_PORT)
    trombone = PWM(Pin(BUZZER_GPIO, Pin.OUT))
    trombone.duty_u16(ceil(MAX_U16 / 2))
    
    while True:
        if play_btn.value() == 0:
            freq = int(((joystick.read_u16() / MAX_U16) * FREQ_RANGE) + MIN_FREQ)
            trombone.freq(freq)
            currently_playing = True
        elif currently_playing:
            trombone.duty_u16(0)
            currently_playing = False