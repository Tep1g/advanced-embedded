import time
import random
from machine import Pin

def p1():
    button1 = Pin(15, Pin.IN, Pin.PULL_UP)
    button2 = Pin(14, Pin.IN, Pin.PULL_UP)
    led1 = Pin(16, Pin.OUT)
    led2 = Pin(17, Pin.OUT)

    try:
        while True:
            led1.value((1 - button1.value()) & (1 - button2.value()))
            led2.value((1 - button1.value()) ^ (1 - button2.value()))
    except KeyboardInterrupt:
        return "Exited Sucessfully"


class ButtonCounter():
    def __init__(self, button_pin: int, button_mode: int, counter_ptr: list[int], increment: int):
        self._button = Pin(button_pin, Pin.IN, button_mode)
        self._button.irq(trigger=Pin.IRQ_FALLING, handler=self._button_callback)
        self._counter_ptr = counter_ptr
        self._increment = increment

    def _button_callback(self, pin: Pin):
        self._counter_ptr[0] += self._increment

def counter():
    """Counter program"""
    counter_ptr = [0]
    
    ButtonCounter(15, Pin.PULL_UP, counter_ptr, 10)
    ButtonCounter(14, Pin.PULL_UP, counter_ptr, 1)

    try:
        while True:
            print(counter_ptr[0])
    except KeyboardInterrupt:
        return "Exited Sucessfully"


class SN74165N():
    """
    SN74165N Shift Register
    
    :param Pin clock: Serial clock
    :param Pin load: Loads and shifts the shift register's parallel inputs
    :param Pin rx: Serial receive
    """
    def __init__(self, clock: Pin, load: Pin, rx: Pin):
        self._clock = clock
        self._load = load
        self._rx = rx

    def read(self) -> int:
        """Read the 8-bit input of a 74LS165 shift register using bit banging"""
        # Temporarily pull load pin down
        self._load.value(1)
        self._clock.value(0)
        time.sleep_ms(100)
        self._load.value(0)
        time.sleep_ms(100)
        self._load.value(1)
        # data is latched - now shift it in
        X = 0
        for i in range(0,8):
            self._clock.value(1)
            time.sleep_ms(100)
            X = (X << 1) + self._rx.value()
            self._clock.value(0)
            time.sleep_ms(100)
            print(i, X)
        return(X)

def randnum() -> int:
    """Return a random number between 0 and 255"""
    return random.randrange(0, 256)

def combo_lock():
    """Combo lock game"""

    clock = Pin(10, Pin.OUT)
    load = Pin(9, Pin.OUT)
    rx = Pin(12, Pin.IN, Pin.PULL_UP)
    shiftreg = SN74165N(clock, load, rx)

    button = Pin(15, Pin.IN, Pin.PULL_UP)
    led = Pin(16, Pin.OUT)

    try:
        while True:
            print("Game Start")
            guess_result = ""
            rand_int = randnum()
            guess = -1
            led.off()
            while guess != rand_int:
                while button.value():
                    continue
                guess = shiftreg.read()
                if rand_int == guess:
                    guess_result = "correct"
                elif rand_int > guess:
                    guess_result = "too high"
                else:
                    guess_result = "too low"
                
                print("Guess {} was {}".format(guess, guess_result))

    except KeyboardInterrupt:
        pass
    
    finally:
        return "Exited Sucessfully"