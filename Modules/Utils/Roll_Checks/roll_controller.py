#handles all the roll checks and provides methods for actually rolling and getting a random number between 1 and 30
import random


def roll(sides=30):
    if sides < 1:
        raise ValueError("a die must have at least 1 side")
    return random.randint(1, sides)
