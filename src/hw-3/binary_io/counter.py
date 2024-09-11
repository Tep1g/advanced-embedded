import _thread
from machine import Pin

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
            button_gpio: int, 
            button_pull: int, 
            trigger:int, 
            counter_ptr: list[int], 
            increment: int,
            lock
        ):

        self._button = Pin(button_gpio, Pin.IN, button_pull)
        self._button.irq(trigger=trigger, handler=self._button_callback)
        self._counter_ptr = counter_ptr
        self._increment = increment
        self._lock = lock

    def _button_callback(self, pin: Pin):
        with self._lock:
            self._counter_ptr[0] += self._increment

if __name__ == "__main__":
    """Counter Program"""
    counter_ptr = [0]
    lock = _thread.allocate_lock()
    
    # Configure button counter objects to increment when buttons are let go
    ButtonCounter(15, Pin.PULL_UP, Pin.IRQ_RISING, counter_ptr, 10, lock)
    ButtonCounter(14, Pin.PULL_UP, Pin.IRQ_RISING, counter_ptr, 1, lock)

    try:
        while True:
            print(counter_ptr[0])
    
    except KeyboardInterrupt:
        pass