import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

from Modules.Scenes.Assets.Characters.NPCs import npc_list
from Modules.Scenes.Assets.Characters.NPCs import npc_equipped_inventory_slots
from Modules.Scenes.Assets.Items import item_system
from Modules.Utils.Save_Game import save_game


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.save_path = os.path.join(self.tmpdir.name, "save_game.json")
        self.raynor = npc_list.npc_list[0]["object"]

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_import_has_no_side_effects(self):
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, PYTHONPATH=repo_root)
            subprocess.run(
                [sys.executable, "-c", "import Modules.Utils.Save_Game.save_game"],
                cwd=tmp, env=env, check=True,
            )
            self.assertEqual(os.listdir(tmp), [],
                             "importing save_game created files as a side effect")

    def test_player_state_roundtrip(self):
        state = {
            "player_stats": {"health": 42},
            "inventory": ["Sword"],
            "current_scene": "Dungeon",
            "quest_progress": {"main_quest": 1},
            "character_info": {"race": "Elf"},
        }
        save_game.save_game_state(state, self.save_path)
        loaded = save_game.load_game_state(self.save_path)
        for key, value in state.items():
            self.assertEqual(loaded[key], value)

    def test_npc_state_survives_save_and_load(self):
        slots = npc_equipped_inventory_slots.EquippedInventorySlots(
            helm=None, neck=None, shoulders=None, chest=None, back=None,
            gauntlets=None, hands=None, legs=None, feet=None,
        )
        pendant = item_system.Item("Pendant", "Azure Pendant", "", "", 1)
        self.raynor.playerObject.inventory = slots
        self.assertTrue(slots.equip("helm", pendant))
        self.raynor.playerObject.playerStats = {"health": 7}

        save_game.save_game_state({}, self.save_path)

        # mutate the live NPC after saving (simulates continued play / restart)
        slots.unequip("helm")
        self.raynor.playerObject.playerStats = {"health": 999}

        loaded = save_game.load_game_state(self.save_path)
        self.assertIn("npc_state", loaded, "save file does not contain NPC state")
        save_game.restore_game_state(loaded)

        self.assertIsNotNone(slots.helm, "NPC equipped item was lost after load")
        self.assertEqual(slots.helm.name, "Azure Pendant",
                         "NPC equipment was lost after load")
        self.assertEqual(self.raynor.playerObject.playerStats["health"], 7,
                         "NPC stats were lost after load")

    def test_load_missing_file_returns_none(self):
        with redirect_stdout(io.StringIO()):
            result = save_game.load_game_state(
                os.path.join(self.tmpdir.name, "nope.json"))
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
