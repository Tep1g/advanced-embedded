import time
from machine import Pin, SPI
from random import randrange

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

def combo_lock():
    """Combo lock game"""

    def p3():
        """Return a random number between 0 and 255"""
        return randrange(0, 255+1)

    def p4(bus: SPI, load: Pin):
        """
        Read the binary inputs of a 74LS165 through SPI bus

        :param SPI bus: 74LS165's SPI bus object that gets read from
        :param Pin load: Output pin tied to the 74LS165's load pin

        :return int: 74LS165's 1 byte input
        """
        # Temporarily pull load pin down
        load.value(1)
        time.sleep_us(1)
        load.value(0)
        time.sleep_us(1)
        load.value(1)

        # Return the binary inputs
        return int(bus.read(1))

    bus = SPI(1, baudrate=10_000_000, polarity=0, phase=0, bits=8, sck=10, mosi=11, miso=12)
    load = Pin(13, Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    led = Pin(16, Pin.OUT)

    try:
        while True:
            print("Game Start")
            guess_result = ""
            rand_int = p3()
            guess = -1
            led.off()
            while guess != rand_int:
                while button.value():
                    continue
                guess = p4(bus, load)
                if rand_int == guess:
                    guess_result = "correct"
                elif rand_int > guess:
                    guess_result = "too high"
                else:
                    guess_result = "too low"
                
                print("Guess {} was {}".format(guess, guess_result))

    except KeyboardInterrupt:
        pass