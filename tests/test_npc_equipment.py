import unittest

from Modules.Scenes.Assets.Characters.NPCs.npc_equipped_inventory_slots import EquippedInventorySlots
from Modules.Scenes.Assets.Items import item_system


class EquipmentSlotTests(unittest.TestCase):
    def setUp(self):
        self.slots = EquippedInventorySlots()
        self.helm = item_system.Item("Helm", "Iron Helm", "d", "i", 1)
        self.other_helm = item_system.Item("Helm", "Steel Helm", "d", "i", 1)

    def test_equip_into_empty_slot(self):
        self.assertTrue(self.slots.equip("helm", self.helm))
        self.assertIs(self.slots.helm, self.helm)

    def test_same_item_cannot_be_equipped_twice(self):
        # Reproduces the duplicate-equip bug: the same item in two slots.
        self.assertTrue(self.slots.equip("helm", self.helm))
        self.assertFalse(self.slots.equip("neck", self.helm))
        self.assertIsNone(self.slots.neck)

    def test_occupied_slot_blocks_new_item(self):
        self.assertTrue(self.slots.equip("helm", self.helm))
        self.assertFalse(self.slots.equip("helm", self.other_helm))
        self.assertIs(self.slots.helm, self.helm)

    def test_unequip_frees_slot_for_reuse(self):
        self.slots.equip("helm", self.helm)
        removed = self.slots.unequip("helm")
        self.assertIs(removed, self.helm)
        self.assertIsNone(self.slots.helm)
        self.assertTrue(self.slots.equip("helm", self.other_helm))

    def test_same_item_after_unequip_can_move_slots(self):
        self.slots.equip("helm", self.helm)
        self.slots.unequip("helm")
        self.assertTrue(self.slots.equip("neck", self.helm))
        self.assertIsNone(self.slots.helm)
        self.assertIs(self.slots.neck, self.helm)

    def test_unknown_slot_rejected(self):
        with self.assertRaises(ValueError):
            self.slots.equip("waist", self.helm)
        with self.assertRaises(ValueError):
            self.slots.unequip("waist")

    def test_raynor_default_loadout_is_intact(self):
        from Modules.Scenes.Assets.Characters.NPCs import raynor_of_londor

        equipped = raynor_of_londor.RaynorOfLondor.npcObject.playerObject.inventory
        for slot in EquippedInventorySlots.EQUIPMENT_SLOTS:
            self.assertEqual(getattr(equipped, slot), slot)


if __name__ == "__main__":
    unittest.main()
