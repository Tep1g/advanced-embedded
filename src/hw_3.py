from machine import Pin

def hw_3():

    def init():
        button1 = Pin("GP15", Pin.IN)
        button2 = Pin("GP14", Pin.IN)
        led1 = Pin("GP16", Pin.OUT)
        led2 = Pin("GP17", Pin.OUT)

        return (button1, button2, led1, led2)

    def p1():
        led1.value((1 - button1.value()) & (1 - button2.value()))
        led2.value((1 - button1.value()) ^ (1 - button2.value()))

    (button1, button2, led1, led2) = init()

    try:
        while True:
            p1()
    except KeyboardInterrupt:
        print("Exited")
