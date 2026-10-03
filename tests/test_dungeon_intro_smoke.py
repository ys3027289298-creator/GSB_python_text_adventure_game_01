import builtins
import io
import unittest
from contextlib import redirect_stdout

from Modules.Scenes.Assets.Characters.Players import player
from Modules.Scenes.Dungeon.Scene_one import dungeon_intro


def make_player():
    return player.Player("Human", "Tester", "Paladin", 0, 25, [], {})


def run_scene(inputs):
    responses = iter(inputs)
    output = io.StringIO()
    with redirect_stdout(output):
        original_input = builtins.input
        builtins.input = lambda prompt="": next(responses)
        try:
            dungeon_intro.dungeon_intro_scene(make_player())
        finally:
            builtins.input = original_input
    return output.getvalue()


class TestDungeonIntroScene(unittest.TestCase):
    def test_exit_tunnel_path(self):
        self.assertIn("forest clearing", run_scene(["2"]))

    def test_hide_and_pick_up_pendant(self):
        self.assertIn("tuck the pendant", run_scene(["1", "1", "1"]))

    def test_hide_and_keep_hiding(self):
        self.assertIn("keep moving", run_scene(["1", "1", "2"]))

    def test_confront_figure_path(self):
        self.assertIn("Cleric", run_scene(["1", "2"]))

    def test_invalid_choice_repeats_scene(self):
        output = run_scene(["x", "2"])
        self.assertIn("Invalid choice", output)
        self.assertIn("forest clearing", output)


if __name__ == "__main__":
    unittest.main()
