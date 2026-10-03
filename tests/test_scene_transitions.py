import ast
import os
import unittest

from Modules.Scenes import scene_registry

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE_FILE = os.path.join(
    REPO_ROOT, "Modules", "Scenes", "Dungeon", "Scene_one", "dungeon_intro.py"
)


def scene_call_graph():
    """Return {scene_function_name: set(scene functions it calls)} by static analysis."""
    with open(SCENE_FILE) as handle:
        tree = ast.parse(handle.read())

    scene_names = set(scene_registry.LEGAL_TRANSITIONS)
    graph = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in scene_names:
            callees = set()
            for call in ast.walk(node):
                if (isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Name)
                        and call.func.id in scene_names):
                    callees.add(call.func.id)
            graph[node.name] = callees
    return graph


class TestSceneTransitions(unittest.TestCase):
    def test_registry_covers_every_scene_in_file(self):
        graph = scene_call_graph()
        self.assertEqual(set(graph), set(scene_registry.LEGAL_TRANSITIONS),
                         "scene registry and scene file are out of sync")

    def test_all_transitions_go_through_legal_entries(self):
        graph = scene_call_graph()
        for caller, callees in graph.items():
            legal = set(scene_registry.LEGAL_TRANSITIONS[caller])
            self.assertEqual(callees, legal,
                             f"{caller} jumps to scenes outside its legal entries: "
                             f"{callees - legal or 'missing'} / {legal - callees or ''}")

    def test_every_scene_is_reachable_from_the_entry_point(self):
        graph = scene_call_graph()
        reachable = set()
        frontier = [scene_registry.ENTRY_SCENE]
        while frontier:
            current = frontier.pop()
            if current in reachable:
                continue
            reachable.add(current)
            frontier.extend(graph.get(current, ()))
        self.assertEqual(reachable, set(scene_registry.LEGAL_TRANSITIONS),
                         "some scenes can never be entered through legal transitions")


if __name__ == "__main__":
    unittest.main()
