from random import randrange

def p1():
    rand_int = ""
    for _ in range(0,4):
        rand_int += str(randrange(6))

    # python removes leading zeroes from int, return as string
    return rand_int