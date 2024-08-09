from random import randrange

CODE_LENGTH = 4
MAX_DIGIT_VALUE = 6

def p1():
    rand_num = ""
    for _ in range(0, CODE_LENGTH):
        rand_num += str(randrange(MAX_DIGIT_VALUE))

    # python removes leading zeroes from int, return as string
    return rand_num

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

def p3():
    score = 0
    code = p1()
    while score < 40:
        try:
            guess = input("Enter a four digit guess: ")
            score = p2(guess, code)
            print("Your guess score: {}".format(score))
        except ValueError as error:
            print(error)
