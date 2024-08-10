from machine import Pin

BUTTON1 = Pin("GP15", Pin.IN)
BUTTON2 = Pin("GP14", Pin.IN)
LED1 = Pin("GP16", Pin.OUT)
LED2 = Pin("GP17", Pin.OUT)

def p1():
    LED1.value((1 - BUTTON1.value()) & (1 - BUTTON2.value()))
    LED2.value((1 - BUTTON1.value()) ^ (1 - BUTTON2.value()))
