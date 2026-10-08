"""Monte Carlo chess game: white rook and bishop against a black queen.

Each round places a white rook, a white bishop and a black queen on random,
distinct squares of an 8x8 board. Rounds alternate between the two players:

* White's turn: white scores a point for each of its pieces (rook, bishop)
  that attacks the queen.
* Black's turn: black scores a point for each white piece the queen attacks.

As in the original exercise, pieces do not block each other's line of attack.

Usage:
    python -m src.chess_attacks --rounds 100 --seed 42 --show-boards
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

BOARD_SIZE = 8

Square = Tuple[int, int]  # (row, column), both 1-based


def rook_attacks(rook: Square, target: Square) -> bool:
    return rook[0] == target[0] or rook[1] == target[1]


def bishop_attacks(bishop: Square, target: Square) -> bool:
    return abs(bishop[0] - target[0]) == abs(bishop[1] - target[1])


def queen_attacks(queen: Square, target: Square) -> bool:
    return rook_attacks(queen, target) or bishop_attacks(queen, target)


@dataclass(frozen=True)
class Position:
    rook: Square
    bishop: Square
    queen: Square

    @classmethod
    def random(cls, rng: random.Random) -> "Position":
        squares = [(r, c) for r in range(1, BOARD_SIZE + 1) for c in range(1, BOARD_SIZE + 1)]
        rook, bishop, queen = rng.sample(squares, 3)
        return cls(rook, bishop, queen)

    def white_score(self) -> int:
        return int(rook_attacks(self.rook, self.queen)) + int(bishop_attacks(self.bishop, self.queen))

    def black_score(self) -> int:
        return int(queen_attacks(self.queen, self.rook)) + int(queen_attacks(self.queen, self.bishop))

    def render(self) -> str:
        """Return the board as text: R = white rook, B = white bishop, q = black queen."""
        pieces = {self.rook: "R", self.bishop: "B", self.queen: "q"}
        header = "  " + " ".join(str(c) for c in range(1, BOARD_SIZE + 1))
        rows = [header]
        for r in range(1, BOARD_SIZE + 1):
            cells = (pieces.get((r, c), ".") for c in range(1, BOARD_SIZE + 1))
            rows.append(f"{r} " + " ".join(cells))
        return "\n".join(rows)


def play(rounds: int, rng: random.Random, show_boards: bool = False) -> Tuple[int, int]:
    """Play ``rounds`` rounds, white moving first, and return (white, black) scores."""
    white = black = 0
    for i in range(rounds):
        position = Position.random(rng)
        if show_boards:
            print(position.render(), end="\n\n")
        if i % 2 == 0:
            white += position.white_score()
        else:
            black += position.black_score()
    return white, black


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rounds", type=int, default=100, help="number of rounds (default: 100)")
    parser.add_argument("--seed", type=int, help="random seed for reproducible games")
    parser.add_argument("--show-boards", action="store_true", help="print the board of every round")
    args = parser.parse_args(argv)

    white, black = play(args.rounds, random.Random(args.seed), args.show_boards)
    print(f"White score: {white}")
    print(f"Black score: {black}")


if __name__ == "__main__":
    main()
