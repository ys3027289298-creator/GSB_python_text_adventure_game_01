import unittest

from Modules.Scenes.Assets.Characters.NPCs import npc_equipped_inventory_slots
from Modules.Scenes.Assets.Items import item_system


def make_slots():
    return npc_equipped_inventory_slots.EquippedInventorySlots(
        helm=None, neck=None, shoulders=None, chest=None, back=None,
        gauntlets=None, hands=None, legs=None, feet=None,
    )


class TestNpcEquipSlots(unittest.TestCase):
    def setUp(self):
        self.slots = make_slots()
        self.helm = item_system.Item("Helm", "Iron Helm", "A sturdy helm", "", 2)
        self.other_helm = item_system.Item("Helm", "Steel Helm", "A shinier helm", "", 3)

    def test_equip_into_empty_slot(self):
        self.assertTrue(self.slots.equip("helm", self.helm))
        self.assertIs(self.slots.helm, self.helm)

    def test_equip_occupied_slot_is_rejected(self):
        self.slots.equip("helm", self.helm)
        self.assertFalse(self.slots.equip("helm", self.other_helm))
        self.assertIs(self.slots.helm, self.helm, "occupied slot was overwritten")

    def test_same_item_cannot_be_equipped_twice(self):
        self.slots.equip("helm", self.helm)
        self.assertFalse(self.slots.equip("gauntlets", self.helm),
                         "the same item instance was equipped into two slots")
        self.assertIsNone(self.slots.gauntlets)

    def test_equip_unknown_slot_is_rejected(self):
        self.assertFalse(self.slots.equip("ring", self.helm))

    def test_unequip_frees_the_slot(self):
        self.slots.equip("helm", self.helm)
        self.assertIs(self.slots.unequip("helm"), self.helm)
        self.assertIsNone(self.slots.helm)
        self.assertTrue(self.slots.equip("helm", self.other_helm))


if __name__ == "__main__":
    unittest.main()
