from machine import Pin
from beep import Beeper

class BetweenBeepsIncrementer:
    def __init__(self, beeper: Beeper, incr_pct: int, incr_gpio: int, decr_gpio: int, pull_config: int):
        self._beeper = beeper
        self._incr_step = round(beeper.init_between_beeps_ms * incr_pct / 100.0)
        self._increment = Pin(incr_gpio, Pin.IN, pull_config)
        self._decrement = Pin(decr_gpio, Pin.IN, pull_config)
        
        if pull_config == Pin.PULL_UP:
            edge_config = Pin.IRQ_FALLING
        elif pull_config == Pin.PULL_DOWN:
            edge_config = Pin.IRQ_RISING
        else:
            raise ValueError("Invalid pull configuration, must be {} or {}".format(Pin.IRQ_RISING, Pin.IRQ_FALLING))

        self._increment.irq(handler=self._increment_handler, trigger=edge_config)
        self._decrement.irq(handler=self._decrement_handler, trigger=edge_config)

    def _increment_handler(self, pin):
        self._beeper.between_beeps_ms += self._incr_step

    def _decrement_handler(self, pin):
        self._beeper.between_beeps_ms -= self._incr_step