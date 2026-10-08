"""Build 16-bit numbers from the characters of a text file and analyse them.

Steps:
1. Read a text file and drop the spaces.
2. Encode every character as a 7-bit binary code.
3. Keep only the first two and last two bits of each code (4 bits per character).
4. Join every four characters into one 16-bit number. If the last group is
   short, it is left-padded with zeros.
5. Report the percentage of numbers that are even and that are divisible
   by 3, 5 and 7.

Usage:
    python -m ergasies.bit_patterns examples/sample.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional

DIVISORS = (2, 3, 5, 7)


def char_nibble(char: str) -> str:
    """Return the first two and last two bits of the 7-bit code of ``char``."""
    code = format(ord(char), "07b")
    return code[:2] + code[-2:]


def to_16bit_numbers(text: str) -> List[int]:
    """Convert ``text`` (spaces removed) into a list of 16-bit numbers."""
    nibbles = [char_nibble(c) for c in text if c != " "]
    numbers = []
    for start in range(0, len(nibbles), 4):
        bits = "".join(nibbles[start:start + 4]).rjust(16, "0")
        numbers.append(int(bits, 2))
    return numbers


def divisibility_percentages(numbers: List[int]) -> Dict[int, float]:
    """Return, for each divisor, the percentage of ``numbers`` divisible by it."""
    if not numbers:
        return {d: 0.0 for d in DIVISORS}
    return {d: 100 * sum(n % d == 0 for n in numbers) / len(numbers) for d in DIVISORS}


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path, help="text file to analyse")
    args = parser.parse_args(argv)

    numbers = to_16bit_numbers(args.file.read_text(encoding="utf-8"))
    print(f"16-bit numbers: {len(numbers)}")
    for divisor, percent in divisibility_percentages(numbers).items():
        label = "even" if divisor == 2 else f"divisible by {divisor}"
        print(f"{label:<16} {percent:6.2f}%")


if __name__ == "__main__":
    main()
