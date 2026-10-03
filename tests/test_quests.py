import io
import unittest
from contextlib import redirect_stdout

from Modules.Scenes.Assets.Items import item_system
from Modules.Scenes.Quests import quest_system
from Modules.Scenes.Assets.Characters.Players import player


def make_player(inventory=None):
    return player.Player("Human", "Tester", "Paladin", 0, 25, inventory or [], {})


class TestQuestPrerequisites(unittest.TestCase):
    def setUp(self):
        self.pendant = item_system.Item("Pendant", "Azure Pendant", "", "", 1)
        self.quest = quest_system.Quest(
            "Oracle's Guidance",
            required_dialogue=["met_raynor"],
            required_items=["Azure Pendant"],
        )

    def test_dialogue_alone_does_not_complete_quest(self):
        player_obj = make_player()
        self.assertFalse(self.quest.is_complete(player_obj, {"met_raynor": True}, set()))

    def test_item_alone_does_not_complete_quest(self):
        player_obj = make_player(inventory=[self.pendant])
        self.assertFalse(self.quest.is_complete(player_obj, {}, set()))

    def test_quest_completes_with_dialogue_and_items(self):
        player_obj = make_player(inventory=[self.pendant])
        self.assertTrue(
            self.quest.is_complete(player_obj, {"met_raynor": True}, set())
        )

    def test_item_consumed_on_turn_in(self):
        player_obj = make_player(inventory=[self.pendant])
        with redirect_stdout(io.StringIO()):
            self.quest.turn_in(player_obj, {"met_raynor": True}, set())
        self.assertEqual(player_obj.inventory, [])

    def test_turn_in_rejected_when_incomplete(self):
        player_obj = make_player(inventory=[self.pendant])
        # dialogue flag missing -> quest incomplete -> turn-in must not consume items
        with redirect_stdout(io.StringIO()):
            self.quest.turn_in(player_obj, {}, set())
        self.assertEqual(len(player_obj.inventory), 1)

    def test_prerequisite_quest_must_be_completed(self):
        chained = quest_system.Quest(
            "Chained Quest",
            required_dialogue=["spoke"],
            required_items=[],
            prerequisite_quests=["Oracle's Guidance"],
        )
        player_obj = make_player()
        self.assertFalse(chained.is_complete(player_obj, {"spoke": True}, set()))
        self.assertTrue(
            chained.is_complete(player_obj, {"spoke": True}, {"Oracle's Guidance"})
        )


if __name__ == "__main__":
    unittest.main()
