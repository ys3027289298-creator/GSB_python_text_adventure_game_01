# just a definition for the inventory structure
# each NPC must have armour, etc. so I created this to have a centralized structure to hold all that info
# Note: This is ONLY for NPCs right now, this is to assign items to them at spawn

class EquippedInventorySlots:
    def __init__(self, helm, neck, shoulders, chest, back, gauntlets, hands, legs, feet):
        self.helm = helm
        self.neck = neck
        self.shoulders = shoulders
        self.chest = chest
        self.back = back
        self.gauntlets = gauntlets
        self.hands = hands
        self.legs = legs
        self.feet = feet