from machine import Pin

def hw_3():

    class hw_stuff():
        def __init__(self):
        
            self.button1 = Pin("GP15", Pin.IN)
            self.button1.irq(trigger=Pin.IRQ_RISING, handler=self._p2_callback1)
            self.button2 = Pin("GP14", Pin.IN)
            self.button2.irq(trigger=Pin.IRQ_RISING, handler=self._p2_callback2)
            self.led1 = Pin("GP16", Pin.OUT)
            self.led2 = Pin("GP17", Pin.OUT)
            self.counter = 0
    
        def _p2_callback1(self, pin):
            self.counter += 10

        def _p2_callback2(self, pin):
            self.counter += 1

    def p1(stuff: hw_stuff):
        stuff.led1.value((1 - stuff.button1.value()) & (1 - stuff.button2.value()))
        stuff.led2.value((1 - stuff.button1.value()) ^ (1 - stuff.button2.value()))

    stuff = hw_stuff()

    try:
        while True:
            print(stuff.counter)
    except KeyboardInterrupt:
        pass