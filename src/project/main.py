from lcd import LCD
from neopixel import NeoPixel
from machine import Pin
from rgb import RGBController

if __name__ == "__main__":
    neopixel = NeoPixel(Pin(11), 8, bpp=3, timing=1)
    rgb_switch = Pin(15, Pin.IN, Pin.PULL_UP)
    select_button = Pin(14, Pin.IN, Pin.PULL_UP)
    lcd = LCD(stick_x_gpio=26, stick_y_gpio=27)
    strip = RGBController(rgb_switch, select_button, neopixel, lcd)
    lcd.init()
    while True:
        try:
            lcd.tick()
        except KeyboardInterrupt:
            break  