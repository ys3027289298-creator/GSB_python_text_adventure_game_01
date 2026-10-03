import unittest

from Modules.Utils.Roll_Checks import roll_controller


class TestRollChecks(unittest.TestCase):
    ROLLS = 20000

    def test_roll_stays_within_bounds(self):
        for _ in range(self.ROLLS):
            result = roll_controller.roll()
            self.assertGreaterEqual(result, 1, "roll produced a value below 1")
            self.assertLessEqual(result, 30, "roll produced a value above 30")

    def test_roll_bounds_are_reachable(self):
        results = {roll_controller.roll() for _ in range(self.ROLLS)}
        self.assertIn(1, results, "lower bound 1 was never rolled")
        self.assertIn(30, results, "upper bound 30 was never rolled")

    def test_roll_custom_die(self):
        for _ in range(5000):
            result = roll_controller.roll(6)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

    def test_roll_rejects_invalid_die(self):
        with self.assertRaises(ValueError):
            roll_controller.roll(0)
        with self.assertRaises(ValueError):
            roll_controller.roll(-5)


if __name__ == "__main__":
    unittest.main()
