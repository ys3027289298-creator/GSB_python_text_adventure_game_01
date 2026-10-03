import ast
import contextlib
import io
import importlib
import os
import unittest
from unittest import mock

from Modules.Scenes import scene_registry

SCENE_FILE = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "Modules",
    "Scenes",
    "Dungeon",
    "Scene_one",
    "dungeon_intro.py",
)


def parse_scene_calls():
    """Return {scene_function: {called_scene_functions}} by walking the AST."""
    with open(SCENE_FILE) as handle:
        tree = ast.parse(handle.read())
    scene_functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }
    edges = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        targets = set()
        for call in ast.walk(node):
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
                if call.func.id in scene_functions:
                    targets.add(call.func.id)
        edges[node.name] = targets
    return scene_functions, edges


class SceneTransitionTests(unittest.TestCase):
    def test_every_scene_function_is_a_registered_entry_point(self):
        scene_functions, _ = parse_scene_calls()
        self.assertEqual(scene_functions, set(scene_registry.ENTRY_POINTS.keys()))
        for name, path in scene_registry.ENTRY_POINTS.items():
            module_path, _, func_name = path.rpartition(".")
            module = importlib.import_module(module_path)
            self.assertTrue(callable(getattr(module, func_name)), name)

    def test_every_transition_is_legal(self):
        scene_functions, edges = parse_scene_calls()
        for caller, targets in edges.items():
            for callee in targets:
                self.assertIn(caller, scene_registry.ENTRY_POINTS)
                self.assertIn(callee, scene_registry.ENTRY_POINTS)
                self.assertTrue(
                    scene_registry.is_legal_transition(caller, callee),
                    f"illegal scene jump: {caller} -> {callee}",
                )

    def test_every_scene_is_reachable_from_the_start_entry_point(self):
        _, edges = parse_scene_calls()
        seen = set()
        stack = [scene_registry.START_ENTRY_POINT]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(edges.get(current, set()) - seen)
        self.assertEqual(seen, set(scene_registry.ENTRY_POINTS.keys()))

    def test_registered_transitions_match_actual_calls(self):
        # No phantom transitions in the registry that the scene never performs.
        _, edges = parse_scene_calls()
        for caller, targets in scene_registry.LEGAL_TRANSITIONS.items():
            # ignore retry self-loops which the scene performs on invalid input
            self.assertTrue(edges.get(caller, set()).issubset(targets | {caller}))

    def test_dungeon_intro_plays_through_every_branch_via_legal_entries(self):
        from Modules.Scenes.Dungeon.Scene_one import dungeon_intro
        from Modules.Scenes.Assets.Characters.Players.player import Player

        inputs_to_play_every_branch = [
            ["1", "1", "1"],   # deeper -> hide -> pick up pendant
            ["1", "1", "2"],   # deeper -> hide -> continue hiding
            ["1", "2"],        # deeper -> confront
            ["2"],             # exit
            ["3", "2"],        # invalid choice, retry, exit
        ]
        for answers in inputs_to_play_every_branch:
            player_object = Player("Human", "Tester", "Paladin", "00", "40", [], "")
            with contextlib.redirect_stdout(io.StringIO()):
                with mock.patch("builtins.input", side_effect=answers):
                    dungeon_intro.dungeon_intro_scene(player_object)

    def test_start_entry_point_resolves_to_intro(self):
        module_path, _, func_name = scene_registry.ENTRY_POINTS[
            scene_registry.START_ENTRY_POINT
        ].rpartition(".")
        module = importlib.import_module(module_path)
        from Modules.Scenes.Dungeon.Scene_one import dungeon_intro

        self.assertIs(getattr(module, func_name), dungeon_intro.dungeon_intro_scene)


if __name__ == "__main__":
    unittest.main()
