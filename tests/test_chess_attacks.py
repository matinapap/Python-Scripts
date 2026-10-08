import random
import unittest

from src.chess_attacks import Position, bishop_attacks, play, queen_attacks, rook_attacks


class AttackTest(unittest.TestCase):
    def test_rook(self):
        self.assertTrue(rook_attacks((1, 1), (1, 8)))
        self.assertTrue(rook_attacks((1, 1), (8, 1)))
        self.assertFalse(rook_attacks((1, 1), (2, 2)))

    def test_bishop(self):
        self.assertTrue(bishop_attacks((1, 1), (8, 8)))
        self.assertTrue(bishop_attacks((2, 7), (7, 2)))
        self.assertTrue(bishop_attacks((1, 6), (3, 8)))
        self.assertFalse(bishop_attacks((1, 1), (1, 2)))

    def test_queen_combines_rook_and_bishop(self):
        self.assertTrue(queen_attacks((4, 4), (4, 8)))
        self.assertTrue(queen_attacks((4, 4), (7, 7)))
        self.assertFalse(queen_attacks((4, 4), (5, 6)))


class PositionTest(unittest.TestCase):
    def test_random_positions_use_distinct_squares(self):
        rng = random.Random(0)
        for _ in range(500):
            p = Position.random(rng)
            self.assertEqual(len({p.rook, p.bishop, p.queen}), 3)

    def test_scores(self):
        p = Position(rook=(1, 1), bishop=(3, 3), queen=(1, 5))
        self.assertEqual(p.white_score(), 2)  # rook on row, bishop on diagonal
        self.assertEqual(p.black_score(), 2)  # queen sees both

    def test_render_marks_pieces(self):
        board = Position(rook=(1, 1), bishop=(2, 2), queen=(8, 8)).render()
        lines = board.splitlines()
        self.assertEqual(lines[1], "1 R . . . . . . .")
        self.assertEqual(lines[2], "2 . B . . . . . .")
        self.assertEqual(lines[8], "8 . . . . . . . q")


class PlayTest(unittest.TestCase):
    def test_seeded_games_are_reproducible(self):
        self.assertEqual(play(100, random.Random(42)), play(100, random.Random(42)))


if __name__ == "__main__":
    unittest.main()
