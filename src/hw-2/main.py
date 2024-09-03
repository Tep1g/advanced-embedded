from random import randrange

CODE_LENGTH = 4
MAX_DIGIT_VALUE = 5
MIN_DIGIT_VALUE = 0
MAX_SCORE = 40

def p1() -> list:
    rand_digits = []
    for _ in range(0, CODE_LENGTH):
        rand_digits.append(randrange(MIN_DIGIT_VALUE, MAX_DIGIT_VALUE + 1))

    return rand_digits

def p2(guess: list, code: list) -> int:
    if ((len(guess) != CODE_LENGTH) or (len(code) != CODE_LENGTH)):
        raise ValueError("Incorrect code length")
    
    score = 0
    for pos in range(0, CODE_LENGTH):
        remaining_digits = code[:pos] + code[pos+1:]
        print(remaining_digits)
        if guess[pos] == code[pos]:
            score += 10
        for digit in remaining_digits:
            if guess[pos] == digit:
                score += 1
        
    return score

def p3():
    score = 0
    guess_num = 1
    code = p1()
    while score < MAX_SCORE:
        try:
            user_input = input("\nGuess number: {}\nEnter a four digit guess: ".format(guess_num))
            guess = [int(digit) for digit in user_input]
            score = p2(guess, code)
            guess_num += 1
            print("Your score: {}".format(score))
        except ValueError as error:
            print(error)
