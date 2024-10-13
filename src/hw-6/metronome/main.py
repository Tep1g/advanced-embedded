from beep import Beeper
from beep_incrementer import BeepIncrementer
from lcd import LCD
from machine import Pin

if __name__ == "__main__":
    beeper = Beeper(
        quiet_period_ms=1000, 
        beep_length_ms=10, 
        beep_freq=500, 
        beep_gpio=28
    )

    incrementer = BeepIncrementer(
        beeper=beeper, 
        incr_pct=1, 
        incr_gpio=15, 
        decr_gpio=14, 
        pull_config=Pin.PULL_UP
    )

    lcd = LCD(beeper=beeper)

    while (True):
        lcd.update_display()