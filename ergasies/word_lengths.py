"""Word-length histogram after removing pairs of words whose lengths sum to 20.

Steps:
1. Read a text file and strip punctuation and digits.
2. Split the text into words.
3. Repeatedly remove pairs of words whose combined length is exactly 20.
4. Print how many of the remaining words have 1, 2, 3, ... letters.

Usage:
    python -m ergasies.word_lengths examples/sample.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

PAIR_LENGTH = 20

# Characters that are dropped entirely (so "e-mail" becomes "email").
_DROPPED = '.,#0123456789*-;:="[]'
# Characters that act as word separators.
_SEPARATORS = "+!()_'@?\n\t"

_CLEAN_TABLE = str.maketrans(_SEPARATORS, " " * len(_SEPARATORS), _DROPPED)


def tokenize(text: str) -> List[str]:
    """Strip punctuation and digits from ``text`` and return its words."""
    return text.translate(_CLEAN_TABLE).split()


def remove_pairs(words: List[str], target: int = PAIR_LENGTH) -> List[str]:
    """Remove pairs of words whose lengths add up to ``target``.

    For each word, the first later word that completes the pair is removed
    together with it. Words that have no partner are kept.
    """
    remaining = list(words)
    i = 0
    while i < len(remaining) - 1:
        partner = next(
            (j for j in range(i + 1, len(remaining))
             if len(remaining[i]) + len(remaining[j]) == target),
            None,
        )
        if partner is None:
            i += 1
        else:
            del remaining[partner]
            del remaining[i]
    return remaining


def length_histogram(words: List[str]) -> List[int]:
    """Return counts where index ``n`` holds the number of words of length ``n + 1``."""
    if not words:
        return []
    counts = [0] * max(len(word) for word in words)
    for word in words:
        counts[len(word) - 1] += 1
    return counts


def format_histogram(counts: List[int]) -> str:
    lines = []
    for length, count in enumerate(counts, start=1):
        unit = "letter" if length == 1 else "letters"
        lines.append(f"Words with {length:>2} {unit}: {count}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path, help="text file to analyse")
    args = parser.parse_args(argv)

    words = remove_pairs(tokenize(args.file.read_text(encoding="utf-8")))
    print(format_histogram(length_histogram(words)) or "No words left.")


if __name__ == "__main__":
    main()
