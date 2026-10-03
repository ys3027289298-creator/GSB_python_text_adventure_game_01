# Quest definitions and completion checks.
# A quest may require that certain dialogue flags have been triggered AND
# that the player actually holds the required items. Checking dialogue alone
# let quests complete while the required items were never obtained.


def _inventory_has_item(inventory, item_name):
    wanted = item_name.lower()
    for entry in inventory:
        name = getattr(entry, "name", entry)
        if str(name).lower() == wanted:
            return True
    return False


class Quest:
    def __init__(self, quest_id, description, required_dialogue=None, required_items=None):
        self.quest_id = quest_id
        self.description = description
        self.required_dialogue = list(required_dialogue or [])
        self.required_items = list(required_items or [])

    def dialogue_prerequisites_met(self, dialogue_flags):
        dialogue_flags = dialogue_flags or set()
        return all(flag in dialogue_flags for flag in self.required_dialogue)

    def item_prerequisites_met(self, inventory):
        return all(_inventory_has_item(inventory, item_name) for item_name in self.required_items)

    def is_complete(self, dialogue_flags, inventory):
        # Both conditions must hold - talking is not enough if the items
        # required to finish the quest are missing.
        return (
            self.dialogue_prerequisites_met(dialogue_flags)
            and self.item_prerequisites_met(inventory)
        )
