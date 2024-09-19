from machine import Pin, ADC, PWM

MAX_U16 = (2 ** 16) - 1
HALF_U16 = round(MAX_U16 / 2)

MIN_FREQ = 220
MAX_FREQ = 440

FREQ_FACTOR = (MAX_FREQ - MIN_FREQ) / MAX_U16

V_REF = 3.3

VOLT_FACTOR = V_REF / MAX_U16

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
            js_adc_val = joystick.read_u16()
            freq = round(js_adc_val * FREQ_FACTOR) + MIN_FREQ
            freq = max(min(freq, MAX_FREQ), MIN_FREQ)
            trombone.freq(freq)
            if not trombone_is_on:
                trombone.duty_u16(HALF_U16)
                trombone_is_on = True

            voltage = js_adc_val * VOLT_FACTOR
            print("Frequency: {}, Voltage: {:.2f}".format(freq, voltage))
        
        elif trombone_is_on:
            trombone.duty_u16(0)
            trombone_is_on = False