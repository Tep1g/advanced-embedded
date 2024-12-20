from lcd import LCD
from machine import Pin
from neopixel import NeoPixel

RGB_STRING = "RGB"

class RGBController:
    def __init__(self, button_rgb: Pin, button_clear: Pin, neopixel: NeoPixel, lcd: LCD):
        self._neopixel = neopixel
        self._lcd = lcd
        self._rgb_pointer = 0
        self._np_selected = False
        self._current_rgb = [0, 0, 0]
        self._button_rgb = button_rgb
        self._button_clear = button_clear
        self._button_rgb.irq(handler=self._rgb_handler, trigger=Pin.IRQ_FALLING)
        self._button_clear.irq(handler=self._clear_handler, trigger=Pin.IRQ_FALLING)

    def _rgb_handler(self, pin: Pin):
        if not self._np_selected:
            self._lcd.switch_box_rgb(self._rgb_pointer)
            self._np_selected = True
            self._lcd.vertically_constrained = True
            print("Selected NeoPixel {}".format(self._lcd.box_pos[1]))
        else:
            self._current_rgb[self._rgb_pointer] = 23 * self._lcd.box_pos[0]
            self._neopixel[self._lcd.box_pos[1]] = tuple(self._current_rgb) #type: ignore
            self._neopixel.write()
            print("Set {} value to {}".format(RGB_STRING[self._rgb_pointer], self._current_rgb[self._rgb_pointer]))
            self._rgb_pointer = (self._rgb_pointer + 1) % 3

            if self._rgb_pointer == 0:
                self._np_selected = False
                self._lcd.vertically_constrained = False
                print("Set NeoPixel {} to RGB value {}".format(self._lcd.box_pos[1], self._current_rgb))
                self._lcd.clear_box_rgb()
                self._current_rgb = [0, 0, 0]
            else:
                self._lcd.switch_box_rgb(self._rgb_pointer)

    def _clear_handler(self, pin: Pin):
        self._np_selected = False
        self._lcd.vertically_constrained = False
        self._lcd.clear_box_rgb()
        self._rgb_pointer = 0
        self._current_rgb = [0, 0, 0]
        self._neopixel.fill((0,0,0))
        self._neopixel.write()
        print("All NeoPixels Cleared")