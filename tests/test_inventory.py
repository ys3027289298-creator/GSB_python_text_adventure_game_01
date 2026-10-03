import contextlib
import io
import unittest

from Modules.Scenes.Assets.Items import item_system
from Modules.Utils.Player_Inventory import inventory_system


@contextlib.contextmanager
def silence_game_text():
    new_out = io.StringIO()
    with contextlib.redirect_stdout(new_out):
        yield


def make_potion():
    return item_system.StackableItem(
        type="Potion",
        name="Healing Potion",
        description="Restores health.",
        interaction_description="You drink it.",
        weight=1,
        max_stack_size=5,
    )


class StackingTests(unittest.TestCase):
    def test_stack_grows_up_to_max_only(self):
        potion = make_potion()
        for _ in range(4):
            with silence_game_text():
                self.assertTrue(inventory_system.add_to_stack(potion))
        self.assertEqual(potion.stack_count, 5)
        with silence_game_text():
            self.assertFalse(inventory_system.add_to_stack(potion))
        self.assertEqual(potion.stack_count, 5)

    def test_stack_shrinks_down_to_zero_only(self):
        potion = make_potion()
        with silence_game_text():
            inventory_system.add_to_stack(potion)
            inventory_system.add_to_stack(potion)
            inventory_system.remove_from_stack(potion)
        self.assertEqual(potion.stack_count, 2)
        with silence_game_text():
            inventory_system.remove_from_stack(potion)
            inventory_system.remove_from_stack(potion)
        self.assertEqual(potion.stack_count, 0)
        with silence_game_text():
            self.assertFalse(inventory_system.remove_from_stack(potion))
        self.assertEqual(potion.stack_count, 0)

    def test_new_stack_starts_at_one(self):
        potion = make_potion()
        self.assertEqual(potion.stack_count, 1)


class DuplicateDropTests(unittest.TestCase):
    def test_same_item_dropped_twice_is_not_duplicated(self):
        # The loot controller builds a fresh Item instance on every drop.
        def drop():
            return item_system.Item(
                type="Pendant",
                name="Azure Pendant",
                description="d",
                interaction_description="i",
                weight=1,
            )

        inventory = []
        with silence_game_text():
            inventory_system.add_to_inventory(drop(), inventory)
            inventory_system.add_to_inventory(drop(), inventory)
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].name, "Azure Pendant")

    def test_different_items_both_kept(self):
        inventory = []
        with silence_game_text():
            inventory_system.add_to_inventory(item_system.Item("Pendant", "Azure Pendant", "d", "i", 1), inventory)
            inventory_system.add_to_inventory(item_system.Item("Pendant", "Angel's Tear", "d", "i", 1), inventory)
        self.assertEqual(len(inventory), 2)


class WeightTests(unittest.TestCase):
    def test_not_overweight_counts_stack_weights(self):
        potion = make_potion()
        self.assertTrue(inventory_system.not_overweight([potion]))
        with silence_game_text():
            for _ in range(4):
                inventory_system.add_to_stack(potion)
        self.assertTrue(inventory_system.not_overweight([potion]))

    def test_overweight_blocks_add(self):
        heavy = item_system.Item("Weapon", "Boulder", "d", "i", inventory_system.max_weight)
        inventory = [heavy]
        with silence_game_text():
            added = inventory_system.add_to_inventory(
                item_system.Item("Weapon", "Second Boulder", "d", "i", 1), inventory
            )
        self.assertIsNone(added)
        self.assertEqual(len(inventory), 1)


if __name__ == "__main__":
    unittest.main()
