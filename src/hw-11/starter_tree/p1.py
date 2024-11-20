from machine import Pin, Timer
from neopixel import NeoPixel

class StarterTree:
    def __init__(self, start_button: Pin, clear_button: Pin, np_pin: Pin, num_neopixels: int=8, bpp: int=3, timing: int=1):
        self._np = NeoPixel(np_pin, num_neopixels, bpp=3, timing=1)
        self._current_np = 0
        self._num_neopixels = num_neopixels
        self._timer = Timer()
        self._start_button = start_button
        self._start_button.irq(handler=self._start_handler, trigger=Pin.IRQ_FALLING) #type: ignore
        self._clear_button = clear_button
        self._clear_button.irq(handler=self._clear_handler, trigger=Pin.IRQ_FALLING) #type: ignore

    def _start_handler(self, pin: Pin):
        self._timer.init(mode=Timer.PERIODIC, period=1000, callback=self._tree_handler)

    def _clear_handler(self, pin: Pin):
        self._np.fill((0,0,0))
        self._np.write()

    def _tree_handler(self, timer: Timer):
        self._np[self._current_np] = (255, 0, 0) #type: ignore
        self._np.write()
        self._current_np = (self._current_np + 1) % self._num_neopixels
        if self._current_np == 0:
            self._timer.deinit()

if __name__ == "__main__":
    start_button = Pin(15, Pin.IN, Pin.PULL_UP)
    clear_button = Pin(14, Pin.IN, Pin.PULL_UP)
    tree = StarterTree(start_button=start_button, clear_button=clear_button, np_pin=Pin(11))

    while True:
        continue