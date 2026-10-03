# Central registry of every scene and the scenes it is allowed to hand control to.
# Scene functions may only transfer control to entries listed here (or repeat
# themselves for invalid input). tests/test_scene_transitions.py proves that
# every jump in the scene files goes through one of these legal entry points.

ENTRY_SCENE = "dungeon_intro_scene"

LEGAL_TRANSITIONS = {
    "dungeon_intro_scene": ["deeper_into_tunnel", "exit_tunnel", "dungeon_intro_scene"],
    "deeper_into_tunnel": ["hide_in_shadows", "confront_figure", "deeper_into_tunnel"],
    "hide_in_shadows": ["continue_hiding", "hide_in_shadows"],
    "exit_tunnel": [],
    "continue_hiding": [],
    "confront_figure": [],
}
