import json

from ...Scenes.Assets.Characters.NPCs import npc_list
from ...Scenes.Assets.Characters.NPCs.npc_equipped_inventory_slots import EquippedInventorySlots

DEFAULT_SAVE_FILE = "save_game.json"

# Example game state vars -> will be changing how we get this in here, but leaving as is for now: todo: revisit
player_stats = {"health": 100, "mana": 50}
inventory = ["Sword", "Healing Potion"]
current_scene = "Forest"
quest_progress = {"main_quest": 2, "side_quest": 1}
character_info = {"race": "Human", "looks": "Tall", "stats": {"strength": 8, "agility": 6}}


def _item_name(item):
    return getattr(item, "name", item)


def serialize_npc_state():
    # Previously the save file had no NPC section at all, so every NPC's
    # inventory/equipment/state was lost on reload. Persist it explicitly.
    serialized = []
    for entry in npc_list.npc_list:
        npc_object = entry["object"]
        character = npc_object.playerObject
        state = {"name": character.name}
        if isinstance(character.inventory, EquippedInventorySlots):
            state["equipped"] = {
                slot: getattr(character.inventory, slot)
                for slot in EquippedInventorySlots.EQUIPMENT_SLOTS
            }
        else:
            state["inventory"] = [_item_name(item) for item in (character.inventory or [])]
        serialized.append(state)
    return serialized


def apply_npc_state(saved_npcs):
    for saved in saved_npcs or []:
        for entry in npc_list.npc_list:
            npc_object = entry["object"]
            if npc_object.playerObject.name != saved["name"]:
                continue
            character = npc_object.playerObject
            if "equipped" in saved and isinstance(character.inventory, EquippedInventorySlots):
                for slot in EquippedInventorySlots.EQUIPMENT_SLOTS:
                    setattr(character.inventory, slot, saved["equipped"].get(slot))
            elif "inventory" in saved:
                character.inventory = list(saved["inventory"])
            break


def build_game_state():
    return {
        "player_stats": player_stats,
        "inventory": inventory,
        "current_scene": current_scene,
        "quest_progress": quest_progress,
        "character_info": character_info,
        "npcs": serialize_npc_state(),
    }


# Save game state to a JSON file
def save_game_state(state=None, save_file=DEFAULT_SAVE_FILE):
    game_state = state if state is not None else build_game_state()
    with open(save_file, "w") as file_handle:  # same as with C/C++ FILE -> "w" is to write, "r" is to read
        json.dump(game_state, file_handle, indent=4)


# Load game state from the JSON file and restore NPC state
def load_game_state(save_file=DEFAULT_SAVE_FILE, restore_npcs=True):
    try:
        with open(save_file, "r") as file_handle:
            loaded_data = json.load(file_handle)
    except FileNotFoundError:
        print("No saved game found.")
        return None
    if restore_npcs and "npcs" in loaded_data:
        apply_npc_state(loaded_data["npcs"])
    return loaded_data


if __name__ == "__main__":
    # Example usage
    save_game_state()
    loaded_data = load_game_state()
    if loaded_data:
        print("Loaded game state:", loaded_data)
