from machine import Pin

if __name__ == "__main__":
    button1 = Pin(15, Pin.IN, Pin.PULL_UP)
    button2 = Pin(14, Pin.IN, Pin.PULL_UP)
    led1 = Pin(16, Pin.OUT)
    led2 = Pin(17, Pin.OUT)

    while True:
        led1.value((1 - button1.value()) & (1 - button2.value()))
        led2.value((1 - button1.value()) ^ (1 - button2.value()))