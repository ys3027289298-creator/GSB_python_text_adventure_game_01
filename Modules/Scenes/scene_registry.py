# Central registry of every scene entry point and every legal transition
# between scenes. A scene is only reachable through its registered entry
# function, and a transition is only legal if it is listed below.

ENTRY_POINTS = {
    # function name in dungeon_intro.py : fully qualified function path
    "dungeon_intro_scene": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.dungeon_intro_scene",
    "deeper_into_tunnel": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.deeper_into_tunnel",
    "exit_tunnel": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.exit_tunnel",
    "hide_in_shadows": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.hide_in_shadows",
    "continue_hiding": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.continue_hiding",
    "confront_figure": "Modules.Scenes.Dungeon.Scene_one.dungeon_intro.confront_figure",
}

START_ENTRY_POINT = "dungeon_intro_scene"

# caller -> scenes it is allowed to jump to
LEGAL_TRANSITIONS = {
    "dungeon_intro_scene": {"deeper_into_tunnel", "exit_tunnel"},
    "deeper_into_tunnel": {"hide_in_shadows", "confront_figure"},
    "exit_tunnel": set(),
    "hide_in_shadows": {"continue_hiding"},
    "continue_hiding": set(),
    "confront_figure": set(),
}


def is_legal_transition(from_scene, to_scene):
    # Re-printing the same scene on invalid input is a legal self-loop.
    if from_scene == to_scene:
        return to_scene in ENTRY_POINTS
    return to_scene in LEGAL_TRANSITIONS.get(from_scene, set())
