import unittest

from Modules.Scenes.Quests.quest_system import Quest
from Modules.Scenes.Assets.Items import item_system


def buggy_dialogue_only_completion(quest, dialogue_flags):
    # The old behaviour: completing the dialogue finished the quest even
    # though the required items were never handed over.
    return all(flag in dialogue_flags for flag in quest.required_dialogue)


class QuestPrerequisiteTests(unittest.TestCase):
    def setUp(self):
        self.quest = Quest(
            quest_id="oracle_pendant",
            description="Bring the Azure Pendant to the Oracle.",
            required_dialogue=["met_oracle"],
            required_items=["Azure Pendant"],
        )
        self.pendant = item_system.Item(
            type="Pendant",
            name="Azure Pendant",
            description="d",
            interaction_description="i",
            weight=1,
        )

    def test_reproduce_dialogue_only_bug(self):
        # Documents the bug: dialogue alone used to complete the quest.
        self.assertTrue(buggy_dialogue_only_completion(self.quest, {"met_oracle"}))

    def test_dialogue_without_item_does_not_complete(self):
        self.assertFalse(self.quest.is_complete({"met_oracle"}, []))

    def test_item_without_dialogue_does_not_complete(self):
        self.assertFalse(self.quest.is_complete(set(), [self.pendant]))

    def test_dialogue_and_item_completes(self):
        self.assertTrue(self.quest.is_complete({"met_oracle"}, [self.pendant]))

    def test_wrong_item_does_not_complete(self):
        other = item_system.Item("Pendant", "Angel's Tear", "d", "i", 1)
        self.assertFalse(self.quest.is_complete({"met_oracle"}, [other]))

    def test_item_name_matching_is_case_insensitive(self):
        lower = item_system.Item("Pendant", "azure pendant", "d", "i", 1)
        self.assertTrue(self.quest.is_complete({"met_oracle"}, [lower]))

    def test_quest_without_prerequisites_completes_immediately(self):
        trivial = Quest("trivial", "no requirements")
        self.assertTrue(trivial.is_complete(set(), []))


if __name__ == "__main__":
    unittest.main()
