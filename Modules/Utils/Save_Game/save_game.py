import json

from ...Scenes.Assets.Characters.NPCs import npc_list
from ...Scenes.Assets.Characters.NPCs import npc_equipped_inventory_slots
from ...Scenes.Assets.Items import item_system

# Example game state vars -> will be changing how we get this in here, but leaving as is for now: todo: revisit
player_stats = {"health": 100, "mana": 50}
inventory = ["Sword", "Healing Potion"]
current_scene = "Forest"
quest_progress = {"main_quest": 2, "side_quest": 1}
character_info = {"race": "Human", "looks": "Tall", "stats": {"strength": 8, "agility": 6}}


def encode_item(item):
    if item is None:
        return None
    return getattr(item, "name", item)


def decode_item(encoded):
    return item_system.Item("Restored", encoded, "", "", 0) if isinstance(encoded, str) else encoded


# Serialize every NPC's live state (stats, inventory contents and equipped slots)
def serialize_npcs():
    npc_state = {}
    for entry in npc_list.npc_list:
        player_object = entry["object"].playerObject
        state = {"playerStats": player_object.playerStats}

        if isinstance(player_object.inventory, npc_equipped_inventory_slots.EquippedInventorySlots):
            slots = player_object.inventory
            state["equipped"] = {
                slot: encode_item(getattr(slots, slot)) for slot in slots.SLOTS
            }
            state["inventory"] = []
        else:
            state["equipped"] = {}
            state["inventory"] = [encode_item(item) for item in player_object.inventory]

        npc_state[player_object.name] = state
    return npc_state


# Restore NPC state back onto the live NPC objects
def restore_npcs(npc_state):
    for entry in npc_list.npc_list:
        player_object = entry["object"].playerObject
        saved = npc_state.get(player_object.name)
        if saved is None:
            continue

        player_object.playerStats = saved.get("playerStats", player_object.playerStats)

        if isinstance(player_object.inventory, npc_equipped_inventory_slots.EquippedInventorySlots):
            slots = player_object.inventory
            for slot in slots.SLOTS:
                setattr(slots, slot, decode_item(saved.get("equipped", {}).get(slot)))
        else:
            player_object.inventory = [decode_item(encoded) for encoded in saved.get("inventory", [])]


# Save game state to a JSON file
def save_game_state(game_state=None, path="save_game.json"):
    if game_state is None:
        game_state = {
            "player_stats": player_stats,
            "inventory": inventory,
            "current_scene": current_scene,
            "quest_progress": quest_progress,
            "character_info": character_info,
        }
    game_state["npc_state"] = serialize_npcs()
    with open(path, "w") as save_file: #same as with C/C++ FILE -> "w" is to write, "r" is to read
        json.dump(game_state, save_file, indent=4)

# Load game state from the JSON file
def load_game_state(path="save_game.json"):
    try:
        with open(path, "r") as save_file:
            loaded_data = json.load(save_file)
            return loaded_data
    except FileNotFoundError:
        print("No saved game found.")
        return None

# Apply a loaded state back onto the live game objects
def restore_game_state(loaded_data):
    if loaded_data and "npc_state" in loaded_data:
        restore_npcs(loaded_data["npc_state"])
    return loaded_data

# Example usage
if __name__ == "__main__":
    save_game_state()
    loaded_data = load_game_state()
    if loaded_data:
        print("Loaded game state:", loaded_data)
