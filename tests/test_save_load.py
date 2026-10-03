import json
import os
import tempfile
import unittest

from Modules.Utils.Save_Game import save_game
from Modules.Scenes.Assets.Characters.NPCs import npc_list


def raynor():
    return npc_list.npc_list[0]["object"]


class SaveLoadTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.save_path = os.path.join(self.tmpdir.name, "save_game.json")
        self.original = {
            slot: getattr(raynor().playerObject.inventory, slot)
            for slot in save_game.EquippedInventorySlots.EQUIPMENT_SLOTS
        }

    def tearDown(self):
        for slot, value in self.original.items():
            setattr(raynor().playerObject.inventory, slot, value)
        self.tmpdir.cleanup()

    def test_save_file_contains_npc_state(self):
        save_game.save_game_state(save_file=self.save_path)
        with open(self.save_path) as handle:
            data = json.load(handle)
        self.assertIn("npcs", data)
        names = [npc["name"] for npc in data["npcs"]]
        self.assertIn("Raynor of Londor", names)

    def test_npc_state_survives_save_and_load(self):
        # Mutate the NPC's equipped gear, save, wipe the state, then reload.
        raynor().playerObject.inventory.chest = "Shadowmail Vestments"
        raynor().playerObject.inventory.helm = None
        save_game.save_game_state(save_file=self.save_path)

        raynor().playerObject.inventory.chest = "chest"
        raynor().playerObject.inventory.helm = "helm"

        loaded = save_game.load_game_state(save_file=self.save_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(raynor().playerObject.inventory.chest, "Shadowmail Vestments")
        self.assertIsNone(raynor().playerObject.inventory.helm)

    def test_load_missing_file_returns_none(self):
        missing = os.path.join(self.tmpdir.name, "nope.json")
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(save_game.load_game_state(save_file=missing))

    def test_old_fields_still_saved(self):
        save_game.save_game_state(save_file=self.save_path)
        with open(self.save_path) as handle:
            data = json.load(handle)
        for key in ("player_stats", "inventory", "current_scene", "quest_progress", "character_info"):
            self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
