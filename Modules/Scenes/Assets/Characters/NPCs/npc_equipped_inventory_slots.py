# just a definition for the inventory structure
# each NPC must have armour, etc. so I created this to have a centralized structure to hold all that info
# Note: This is ONLY for NPCs right now, this is to assign items to them at spawn

class EquippedInventorySlots:
    SLOTS = ("helm", "neck", "shoulders", "chest", "back",
             "gauntlets", "hands", "legs", "feet")

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

    def equipped_items(self):
        return [getattr(self, slot) for slot in self.SLOTS
                if getattr(self, slot) is not None]

    def equip(self, slot, item):
        if slot not in self.SLOTS:
            return False
        if getattr(self, slot) is not None:
            return False # slot is occupied, unequip first
        if item in self.equipped_items():
            return False # the same item instance cannot be equipped twice
        setattr(self, slot, item)
        return True

    def unequip(self, slot):
        if slot not in self.SLOTS:
            return None
        item = getattr(self, slot)
        setattr(self, slot, None)
        return item
