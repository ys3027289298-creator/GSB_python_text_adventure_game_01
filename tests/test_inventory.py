import io
import unittest
import unittest.mock
from contextlib import redirect_stdout

from Modules.Scenes.Assets.Items import item_system
from Modules.Scenes.Assets.Items.Magic.Wearables.Small import magic_pendants
from Modules.Scenes.Dungeon.Scene_one.Loot_controller import controller
from Modules.Utils.Player_Inventory import inventory_system


def quiet(func, *args):
    with redirect_stdout(io.StringIO()):
        return func(*args)


class TestInventoryStacking(unittest.TestCase):
    def make_potion(self):
        return item_system.StackableItem(
            "Potion", "Healing Potion", "Heals you", "", 1, max_stack_size=5
        )

    def test_stack_increments_until_max(self):
        potion = self.make_potion()
        for expected in range(2, 6):
            self.assertTrue(quiet(inventory_system.add_to_stack, potion))
            self.assertEqual(potion.stack_count, expected)
        self.assertFalse(quiet(inventory_system.add_to_stack, potion))
        self.assertEqual(potion.stack_count, 5)

    def test_remove_from_stack(self):
        potion = self.make_potion()
        quiet(inventory_system.add_to_stack, potion)
        quiet(inventory_system.add_to_stack, potion)
        self.assertTrue(quiet(inventory_system.remove_from_stack, potion))
        self.assertEqual(potion.stack_count, 2)

    def test_remove_from_empty_stack(self):
        potion = self.make_potion()
        self.assertTrue(quiet(inventory_system.remove_from_stack, potion))
        self.assertEqual(potion.stack_count, 0)
        self.assertFalse(quiet(inventory_system.remove_from_stack, potion))
        self.assertEqual(potion.stack_count, 0)


class TestDropDeduplication(unittest.TestCase):
    def test_same_pendant_dropped_twice_stacks_into_one_entry(self):
        with unittest.mock.patch("random.choice", return_value=magic_pendants.azure_pendant.name):
            first_drop = controller.get_random_item_pendant(controller.loot_table_pendants)
            second_drop = controller.get_random_item_pendant(controller.loot_table_pendants)

        self.assertEqual(first_drop.name, second_drop.name)
        self.assertIsNot(first_drop, second_drop)

        inventory = []
        quiet(inventory_system.add_to_inventory, first_drop, inventory)
        quiet(inventory_system.add_to_inventory, second_drop, inventory)
        self.assertEqual(len(inventory), 1, "identical drops were added as duplicate entries")

    def test_different_items_coexist(self):
        inventory = []
        quiet(inventory_system.add_to_inventory,
              item_system.Item("Axe", "Axe", "", "", 3), inventory)
        quiet(inventory_system.add_to_inventory,
              item_system.Item("Sword", "Sword", "", "", 2), inventory)
        self.assertEqual(len(inventory), 2)

    def test_remove_unknown_item(self):
        self.assertFalse(
            quiet(inventory_system.remove_from_inventory, "Sword", [])
        )


class TestWeightLimit(unittest.TestCase):
    def test_not_overweight_accounts_for_stacks(self):
        potion = item_system.StackableItem("Potion", "Healing Potion", "", "", 2,
                                           max_stack_size=20)
        quiet(inventory_system.add_to_stack, potion)
        quiet(inventory_system.add_to_stack, potion)
        self.assertTrue(inventory_system.not_overweight([potion]))

        heavy = [item_system.Item("Axe", "Heavy", "", "", inventory_system.max_weight)]
        self.assertFalse(inventory_system.not_overweight(heavy))

    def test_add_rejected_at_weight_limit(self):
        inventory = [
            item_system.Item("Axe", "Heavy", "", "", inventory_system.max_weight - 1)
        ]
        pendant = item_system.Item("Pendant", "Azure Pendant", "", "", 10)
        quiet(inventory_system.add_to_inventory, pendant, inventory)
        self.assertEqual(len(inventory), 1, "overweight add was accepted")


if __name__ == "__main__":
    unittest.main()
