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

def p2():

    class p2_stuff():
        def __init__(self):

            self.button1 = Pin(15, Pin.IN, Pin.PULL_UP)
            self.button1.irq(trigger=Pin.IRQ_RISING, handler=self._p2_callback1)
            self.button2 = Pin(14, Pin.IN, Pin.PULL_UP)
            self.button2.irq(trigger=Pin.IRQ_RISING, handler=self._p2_callback2)
            self.led1 = Pin(16, Pin.OUT)
            self.led2 = Pin(17, Pin.OUT)
            self.counter = 0
    
        def _p2_callback1(self, pin):
            self.counter += 10

        def _p2_callback2(self, pin):
            self.counter += 1

    stuff = p2_stuff()

    try:
        while True:
            print(stuff.counter)
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