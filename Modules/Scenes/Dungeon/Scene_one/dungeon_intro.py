# Imports
from .Loot_controller import controller
from ...Assets.Items.Magic.Wearables.Small import magic_pendants
from ....Utils.Player_Inventory import inventory_system
from ....Utils.Text_Formatting import text_handler
from ...Assets.Characters.Players import player
from ...Assets.Characters.NPCs import npc_controller

# The opening/entry scene 
def dungeon_intro_scene(player_object: player.Player):
    text_handler.printNarrationText(["\nYou find yourself standing at the entrance of a narrow, damp tunnel.", "The flickering torches on the walls cast eerie shadows around you.", "Your heart races as you step forward, uncertain of what lies ahead."])
    text_handler.printChoiceText(["Choose your next move:", "1. Proceed deeper into the tunnel.", "2. Turn back and exit the tunnel."])
    choice = text_handler.getInput("Enter 1 or 2: ")

    if choice == "1":
        deeper_into_tunnel(player_object)
    elif choice == "2":
        exit_tunnel(player_object)
    else:
        text_handler.printWarningText(["Invalid choice. Try again."])
        # repeat our intro scene if their choice was invalid
        dungeon_intro_scene(player_object)

def exit_tunnel(player_object: player.Player):
    text_handler.printNarrationText(["Common sense prevails! You turn and run as fast as you can.", "After what feels like an eon, you find yourself standing in a forest clearing."])
    # todo: beef this one up and pass control to the forest scene

# The player ventures deeper into the tunnel.
def deeper_into_tunnel(player_object: player.Player):
    text_handler.printNarrationText(["\nYou continue cautiously, the darkness enveloping you.", "Suddenly, you hear footsteps echoing from behind."])
    text_handler.printChoiceText(["Do you:", "1. Hide in the shadows.", "2. Confront the approaching figure."])

    choice = text_handler.getInput("Enter 1 or 2: ")

    if choice == "1":
        hide_in_shadows(player_object)
    elif choice == "2":
        confront_figure(player_object)
    else:
        text_handler.printWarningText(["Invalid choice. Try again."])
        deeper_into_tunnel(player_object)

# The player hides in the shadows.
def hide_in_shadows(player_object: player.Player):
    text_handler.printNarrationText(["\nYou press yourself against the cold stone wall, heart pounding.", "The figure passes by, cloaked in darkness.", "As they disappear, you notice a glimmering pendant on the ground."])
    text_handler.printChoiceText(["Do you pick it up?", "1. Yes", "2. No"])

    choice = text_handler.getInput("Enter 1 or 2: ")

    if choice == "1":
        # in this sub-scene, we specifically want only a pendant (this programming-approach, on the next line, gives us more control over the types of items the player will get/encounter at this point)
        item = controller.get_random_item_pendant(controller.loot_table_pendants) 
        # this next line makes the game more modular by dynamically/procedurally getting items and their "interaction descriptions", instead of having it all hardcoded all over the place!
        text_handler.printItemText([f"{magic_pendants.get_interaction_description(item.name)}"])
        text_handler.resetColorToWhite()

        inventory_system.add_to_inventory(item, player_object.inventory)
        inventory_system.list_inventory_items(player_object.inventory)
        text_handler.resetColorToWhite()
    elif choice == "2":
        continue_hiding(player_object)
    else:
        text_handler.printWarningText(["Invalid choice. Try again."])
        #repeat the sub-scene
        hide_in_shadows(player_object)

# The player remains hidden.
def continue_hiding(player_object: player.Player):
    text_handler.printNarrationText(["\nYou stay hidden, heart still racing.", "The footsteps fade away, and you decide to keep moving."])
    # todo: add more

# The player confronts the approaching figure.
def confront_figure(player_object: player.Player):
    #this is incorrect -> need to rethink how we do this, since passing in the loot table, etc. is wrong
    npc_object = npc_controller.get_npc_object(npc_controller.unique_npc_loot_table, "Raynor of Londor")
    #todo extract into Raynor scene
    #text_handler.printNarrationText(["\nYou step forward, ready to face the unknown figure.", "The figure turns and your eyes fall on a hooded woman with piercing blue eyes.", f"She introduces herself as Raynor of Londor, a lost cleric of the House of Londor."])
    #might want to use the random method instead? that way every interaction is random and chance-based?
    # i actually don't want to do this, I DO want to make it configurable, but only so that we can have difficulty levels
    #I'm actually thinking of turning this into a custom visual novel at the end, with a nice GUI and scene building support
    #but it's going to be a while until we get there and I want to build the engine first
    print(npc_object)
    print(npc_object.playerObject.playerclass)
    #need to now convert that npc_object into a usable NPC object to access data
    # todo: Call the next scene here
    #todo: can abstract NPC info into a file for different NPCs in future, like we did for the pendants
