#we'll eventually just import every NPC file in the directory through a single import, but that'll require modifying the __init__.py
from . import raynor_of_londor
from . import npc_definition
import random
from . import npc_list

# Holds all special NPCs and characters
unique_npc_loot_table = [ # not to be used in "get random npc" methods
    {"name": raynor_of_londor.RaynorOfLondor.npcObject.playerObject.name, "weight": 1}
    ]
monster_npc_loot_table = [] #todo
unique_monster_npc_loot_table = [] #todo
generic_npc_loot_table = [] #todo | for generic guardsmen, townfolk, etc.


def get_random_npc(object_name): #this method of dynamically getting the "loot table to search through"'s name, allows us to reuse this code, without having lots of copies of it for each item type (like pendants, swords, etc.)
    # Create a list of items based on their weights
    choices = []
    for entry in object_name:
        item, weight = entry["item"], entry["weight"]
        choices.extend([item] * weight) # expands the choices list by adding multiple copies of the same item according to its specified weight. Items with higher weights have a proportionally greater chance of being selected

    # Select a random item from that expanded list
    selected_item = random.choice(choices)
    return selected_item #cast_object_as_npc(get_object_for_cast(selected_item, object_name))

def get_npc_object(list, object_name):
    for item in list:
        if object_name in item["name"]:
            for npc_item in npc_list.npc_list:
                if object_name in npc_item["name"]:
                    return npc_item["object"]
    else:
        return None

def cast_object_as_npc(itemObject):
    return npc_definition.NPC(
        itemObject.race,
        itemObject.name,
        itemObject.playerclass,
        itemObject.playerStats,
        itemObject.weight,
        itemObject.maxweight,
        itemObject.inventory
        )
