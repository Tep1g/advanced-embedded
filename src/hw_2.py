from random import randrange

CODE_LENGTH = 4
MAX_DIGIT_VALUE = 6

def p1():
    rand_int = ""
    for _ in range(0, CODE_LENGTH):
        rand_int += str(randrange(MAX_DIGIT_VALUE))

    # python removes leading zeroes from int, return as string
    return rand_int

def p2(guess: str, code: str):
    if ((len(guess) != CODE_LENGTH) or (len(code) != CODE_LENGTH)):
        raise ValueError("Incorrect code length")
    
    score = 0
    for pos in range(0, CODE_LENGTH):
        if guess[pos] == code[pos]:
            score += 10
        else:
            score += 1
        
    return score