# Quest definitions and completion checks.
from ...Utils.Text_Formatting import text_handler


class Quest:
    def __init__(self, name, required_dialogue=None, required_items=None,
                 prerequisite_quests=None):
        self.name = name
        self.required_dialogue = list(required_dialogue or [])
        self.required_items = list(required_items or [])
        self.prerequisite_quests = list(prerequisite_quests or [])

    def is_complete(self, player_object, dialogue_flags, completed_quests):
        if not all(quest in completed_quests for quest in self.prerequisite_quests):
            return False
        if not all(dialogue_flags.get(flag, False) for flag in self.required_dialogue):
            return False
        inventory_names = [getattr(item, "name", item) for item in player_object.inventory]
        return all(required in inventory_names for required in self.required_items)

    def turn_in(self, player_object, dialogue_flags, completed_quests):
        if not self.is_complete(player_object, dialogue_flags, completed_quests):
            text_handler.printGameEventText([f"[Game: Quest '{self.name}' is not complete yet]"])
            return False
        for required in self.required_items:
            for item in list(player_object.inventory):
                if getattr(item, "name", item) == required:
                    player_object.inventory.remove(item)
                    break
        text_handler.printGameEventText([f"[Game: Quest '{self.name}' turned in]"])
        return True
