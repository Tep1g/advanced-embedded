import time
import random
import _thread
from machine import Pin

def leds():
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
    """
    Button Counter

    Increment a counter when an IRQ interrupt is triggered.

    :param int button_pin: Button GPIO pin
    :param int button_pull: Specify if the pin has a pull resistor attached
    :param int trigger: The IRQ event that triggers an interrupt
    :param list[int] counter_ptr: Pointer to the counter
    :param int increment: Increment size
    :param lock: lock object to prevent simulatenous access to shared resource.
    """
    def __init__(
            self, 
            button_pin: int, 
            button_pull: int, 
            trigger:int, 
            counter_ptr: list[int], 
            increment: int,
            lock
        ):

        self._button = Pin(button_pin, Pin.IN, button_pull)
        self._button.irq(trigger=trigger, handler=self._button_callback)
        self._counter_ptr = counter_ptr
        self._increment = increment
        self._lock = lock

    def _button_callback(self, pin: Pin):
        with self._lock:
            self._counter_ptr[0] += self._increment

def counter():
    """Counter program"""
    counter_ptr = [0]
    lock = _thread.allocate_lock()
    
    # Configure button counter objects to increment on falling edge
    ButtonCounter(15, Pin.PULL_UP, Pin.IRQ_FALLING, counter_ptr, 10, lock)
    ButtonCounter(14, Pin.PULL_UP, Pin.IRQ_FALLING, counter_ptr, 1, lock)

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
    def __init__(self, clk_pin: int, ld_pin: int, rx_pin: int):
        self._clock = Pin(clk_pin, Pin.OUT)
        self._load = Pin(ld_pin, Pin.OUT)
        self._rx = Pin(rx_pin, Pin.IN)

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

    #Init SN74165N, button, and led
    shiftreg = SN74165N(clk_pin=10, ld_pin=9, rx_pin=12)
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

                if guess == rand_int:
                    guess_result = "correct"
                elif guess > rand_int:
                    guess_result = "too high"
                else:
                    guess_result = "too low"
                
                print("Guess {} was {}".format(guess, guess_result))

    except KeyboardInterrupt:
        pass
    
    finally:
        return "Exited Sucessfully"