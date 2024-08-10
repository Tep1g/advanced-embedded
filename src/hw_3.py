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
        pass

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
        pass