# some NPCs can be multi-instance (like monsters), but support-character NPCs should only exist in one instance (dont want 3x Geralt of Rivias in the world at once, for example)

from . import npc_definition
from ..Players import player
from . import npc_equipped_inventory_slots


# will have all the same info (like health, etc.) as a player, with some added attribs
class RaynorOfLondor:
    npcObject:npc_definition.NPC = npc_definition.NPC(
        player.Player(
                    #loading up some default attribs - in case no object is passed in
                    "Human",
                    "Raynor of Londor",
                    "Cleric",
                    "Temp",
                    "60",
                    #will revisit this as soon as I've loaded up more items, hardcoding defaults for now
                    npc_equipped_inventory_slots.EquippedInventorySlots(
                        helm = "helm",
                        neck = "neck",
                        shoulders = "shoulders",
                        chest = "chest",
                        back = "back",
                        gauntlets = "gauntlets",
                        hands = "hands",
                        legs = "legs",
                        feet = "feet"
                    ), # todo: give this a meaningful inventory with unique items, etc.
                    "85"
                 ))


