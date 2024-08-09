from random import randrange

CODE_LENGTH = 4
MAX_DIGIT_VALUE = 6

def p1():
    rand_int = ""
    for _ in range(0, CODE_LENGTH):
        rand_int += str(randrange(MAX_DIGIT_VALUE))

    # python removes leading zeroes from int, return as string
    return rand_int