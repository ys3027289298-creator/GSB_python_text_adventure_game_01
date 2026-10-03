import unittest
from unittest import mock

from Modules.Utils.Roll_Checks import roll_controller


class RollBoundaryTests(unittest.TestCase):
    def test_rolls_stay_within_bounds_d30(self):
        for _ in range(5000):
            result = roll_controller.roll()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 30)

    def test_extreme_endpoints_are_reachable(self):
        seen = {roll_controller.roll() for _ in range(5000)}
        self.assertIn(1, seen)
        self.assertIn(30, seen)

    def test_single_sided_die(self):
        self.assertEqual(roll_controller.roll(1), 1)

    def test_custom_sides_bounds(self):
        for _ in range(2000):
            result = roll_controller.roll(6)
            self.assertTrue(1 <= result <= 6)

    def test_randint_called_with_inclusive_bounds(self):
        # The out-of-bounds bug was randint(0, sides) / randrange(1, sides).
        with mock.patch.object(roll_controller.random, "randint", return_value=1) as randint:
            roll_controller.roll(30)
            randint.assert_called_once_with(1, 30)

    def test_invalid_sides_rejected(self):
        for bad in (0, -1, 1.5, "30", None):
            with self.assertRaises(ValueError):
                roll_controller.roll(bad)

    def test_check_target_bounds(self):
        with self.assertRaises(ValueError):
            roll_controller.is_successful_check(30, 31)
        with self.assertRaises(ValueError):
            roll_controller.is_successful_check(30, 0)

    def test_check_success_and_failure_endpoints(self):
        with mock.patch.object(roll_controller, "roll", return_value=1):
            result, success = roll_controller.is_successful_check(30, 1)
            self.assertEqual(result, 1)
            self.assertTrue(success)
        with mock.patch.object(roll_controller, "roll", return_value=30):
            result, success = roll_controller.is_successful_check(30, 30)
            self.assertEqual(result, 30)
            self.assertTrue(success)
        with mock.patch.object(roll_controller, "roll", return_value=1):
            _, success = roll_controller.is_successful_check(30, 2)
            self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
