# holds a list of every NPC, we use this to dynamically import the correct npcs, etc.
# remember to add your NPC here once you've created their file in the NPC folder
from . import raynor_of_londor

#just doing this to make it neater in the list
raynor = raynor_of_londor.RaynorOfLondor.npcObject

npc_list = [
    {"name":raynor.playerObject.name, "object":raynor}
]