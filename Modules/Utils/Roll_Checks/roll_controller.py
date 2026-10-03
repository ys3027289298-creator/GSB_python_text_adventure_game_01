# handles all roll checks and provides methods for actually rolling
# and getting a random number between 1 and 30 (inclusive, on both ends)

import random

DEFAULT_SIDES = 30


def roll(sides=DEFAULT_SIDES):
    # The result MUST stay within [1, sides] - a d-sides die never shows
    # 0 or sides + 1 (those were the out-of-bounds results).
    if not isinstance(sides, int) or sides < 1:
        raise ValueError("A die must have at least 1 side")
    return random.randint(1, sides)


def is_successful_check(sides=DEFAULT_SIDES, target=1):
    # A successful check means the roll met or beat the target.
    if not isinstance(target, int) or target < 1 or target > sides:
        raise ValueError("Roll target must be between 1 and the number of sides")
    result = roll(sides)
    return result, result >= target
