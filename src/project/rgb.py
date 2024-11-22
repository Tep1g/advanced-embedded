from lcd import LCD
from machine import Pin
from neopixel import NeoPixel

class RGBController:
    def __init__(self, rgb_switch: Pin, select_button: Pin, neopixel: NeoPixel, lcd: LCD):
        self._neopixel = neopixel
        self._lcd = lcd
        self._rgb_pointer = 0
        self._np_selected = False
        self._current_rgb = [0, 0, 0]
        self._rgb_switch = rgb_switch
        self._select_button = select_button
        self._rgb_switch.irq(handler=self._rgb_switch_handler, trigger=Pin.IRQ_FALLING)
        self._select_button.irq(handler=self._select_handler, trigger=Pin.IRQ_FALLING)

    def _rgb_switch_handler(self, pin: Pin):
        if self._np_selected:
            self._current_rgb[self._rgb_pointer] = 31 * self._lcd.box_pos[0]
            self._neopixel[self._lcd.box_pos[1]] = tuple(self._current_rgb) #type: ignore
            self._neopixel.write()
            self._rgb_pointer = (self._rgb_pointer + 1) % 3

            if self._rgb_pointer == 0:
                self._np_selected = False
                self._lcd.vertically_constrained = False
                self._lcd.clear_box_rgb()
                self._current_rgb = [0, 0, 0]
            else:
                self._lcd.switch_box_rgb(self._rgb_pointer)

    def _select_handler(self, pin: Pin):
        if not self._np_selected:
            self._lcd.switch_box_rgb(self._rgb_pointer)
            self._np_selected = True
            self._lcd.vertically_constrained = True
            print("Selected NeoPixel {}".format(self._lcd.box_pos[1]))