from random import randrange

CODE_LENGTH = 4
MAX_DIGIT_VALUE = 5
MIN_DIGIT_VALUE = 0
MAX_SCORE = 40

def get_code() -> list:
    rand_digits = []
    for _ in range(0, CODE_LENGTH):
        rand_digits.append(randrange(MIN_DIGIT_VALUE, MAX_DIGIT_VALUE + 1))

    return rand_digits

def get_score(guess: list, code: list) -> int:
    score = 0
    non_matching_digits = []

    for index in range(0, CODE_LENGTH):

        guess_digit = guess[index]
        code_digit = code[index]

        # Add 10 points for every matching digit
        if guess_digit == code_digit:
            score += 10

        # Save the code's non matching digits
        else:
            non_matching_digits.append(code_digit)

    # Add a point for every non-matching code digit that exists within the guess
    for digit in non_matching_digits:
        if digit in guess:
            score += 1
        
    return score

def main():
    score = 0
    guess_num = 1
    code = get_code()
    while score < MAX_SCORE:
        try:
            user_input = input("\nGuess number: {}\nEnter a four digit guess: ".format(guess_num))

            # Check the input
            invalid_input = False
            if (len(user_input) != CODE_LENGTH) or (not user_input.isdigit()):
                invalid_input |= True
            else:
                for digit in user_input:
                    invalid_input |= not (MIN_DIGIT_VALUE < int(digit) < MAX_DIGIT_VALUE)

            if invalid_input:
                raise ValueError("Invalid input: {}, must be a {} digit code".format(user_input, CODE_LENGTH))
            
            guess = [int(digit) for digit in user_input]
            score = get_score(guess, code)
            guess_num += 1
            print("Your score: {}".format(score))
        except ValueError as error:
            print(error)
