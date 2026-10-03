from ..Players import player
# Define what an NPC is
class NPC:
    def __init__(self, playerObject: player.Player): # will have all the same info (like health, etc.) as a player, with some added attribs
        self.playerObject = playerObject
        # just a general note: every NPC must have their own inventory
        #   we initialize this inventory in their actual character file (See Raynor of Londor file)
        #todo for later: add other attribs -> not going to do this now