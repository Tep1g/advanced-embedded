from random import randrange

NUM_TESTS = 5

def randnum() -> int:
    """Return a random number between 0 and 255"""
    return randrange(0, 256)

if __name__ == "__main__":
    """Test Script"""
    for _ in range(0, NUM_TESTS):
        print(randnum())