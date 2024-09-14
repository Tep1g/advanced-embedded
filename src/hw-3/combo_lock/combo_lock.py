from machine import Pin
from sn74165n import SN74165N
from rand import randnum

if __name__ == "__main__":
    """Combo Lock Program"""

    #Init SN74165N, button, and led
    shiftreg = SN74165N(clk_gpio=10, ld_gpio=9, rx_gpio=12)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    led = Pin(16, Pin.OUT)

    print("Combo Lock Start\n")
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
            led.on()
        elif guess > rand_int:
            guess_result = "too high"
        else:
            guess_result = "too low"
        
        if guess != rand_int:
            print("Code: {}".format(rand_int))

        print("Guess {} was {}\n".format(guess, guess_result))