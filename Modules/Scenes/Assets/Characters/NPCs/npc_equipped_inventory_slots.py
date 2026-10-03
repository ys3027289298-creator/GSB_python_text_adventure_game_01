# just a definition for the inventory structure
# each NPC must have armour, etc. so I created this to have a centralized structure to hold all that info
# Note: This is ONLY for NPCs right now, this is to assign items to them at spawn

class EquippedInventorySlots:
    EQUIPMENT_SLOTS = (
        "helm", "neck", "shoulders", "chest", "back",
        "gauntlets", "hands", "legs", "feet",
    )

    def __init__(self, helm=None, neck=None, shoulders=None, chest=None, back=None, gauntlets=None, hands=None, legs=None, feet=None):
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
        return [getattr(self, slot) for slot in self.EQUIPMENT_SLOTS if getattr(self, slot) is not None]

    def is_equipped(self, item):
        return any(equipped == item for equipped in self.equipped_items())

    def equip(self, slot, item):
        # Guards against the duplicate-equip bug:
        #   1. an item already sitting in another slot cannot be equipped again
        #   2. an occupied slot must be unequipped before something else goes in
        if slot not in self.EQUIPMENT_SLOTS:
            raise ValueError(f"Unknown equipment slot: {slot}")
        if item is None:
            raise ValueError("Cannot equip nothing")
        if self.is_equipped(item):
            return False
        if getattr(self, slot) is not None:
            return False
        setattr(self, slot, item)
        return True

    def unequip(self, slot):
        if slot not in self.EQUIPMENT_SLOTS:
            raise ValueError(f"Unknown equipment slot: {slot}")
        item = getattr(self, slot)
        setattr(self, slot, None)
        return item
