# Ergasies

[![tests](https://github.com/matinapap/Ergasies/actions/workflows/tests.yml/badge.svg)](https://github.com/matinapap/Ergasies/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

Four Python programs from my university coursework (*ergasies* is Greek for
"assignments"). Each one is a small command-line tool covering text
processing, Monte Carlo simulation, bit manipulation, or randomness analysis
using a live public API.

The project uses only the Python standard library and has unit tests that run
on GitHub Actions.

| Module | What it does | Concepts |
| --- | --- | --- |
| [`word_lengths`](ergasies/word_lengths.py) | Cleans a text file, removes pairs of words whose lengths sum to 20, and prints a histogram of the remaining word lengths | Text cleaning, `str.translate`, greedy pairing |
| [`chess_attacks`](ergasies/chess_attacks.py) | Simulates rounds of a white rook and bishop against a black queen on random squares and scores each side's attacks | Monte Carlo simulation, dataclasses, seeded RNG |
| [`bit_patterns`](ergasies/bit_patterns.py) | Encodes text as 7-bit codes, packs them into 16-bit numbers, and reports what share is even or divisible by 3, 5 and 7 | Binary encoding, bit slicing, padding |
| [`drand_runs`](ergasies/drand_runs.py) | Downloads 100 rounds of public randomness from the [drand](https://drand.love) beacon and finds the longest runs of 0s and 1s | HTTP and JSON, hex-to-binary, `itertools.groupby` |

## Getting started

```bash
git clone https://github.com/matinapap/Ergasies.git
cd Ergasies
python -m pip install -e ".[dev]"   # optional: installs the CLI commands and pytest
```

You don't need to install anything to run the modules. `python -m ergasies.<module>`
works straight from the repository with Python 3.9 or newer.

## Usage

### Word-length histogram

```console
$ python -m ergasies.word_lengths examples/sample.txt
Words with  1 letter: 2
Words with  2 letters: 8
Words with  3 letters: 7
...
Words with 11 letters: 2
```

### Chess attack simulation

```console
$ python -m ergasies.chess_attacks --rounds 100 --seed 42
White score: 15
Black score: 31
```

Add `--show-boards` to print every board (`R` = white rook, `B` = white bishop,
`q` = black queen):

```text
  1 2 3 4 5 6 7 8
1 . . . . . . . .
2 B . . . . . . .
3 . R . . . . . .
4 . . . . . . . .
5 q . . . . . . .
...
```

Rounds alternate between the players. On white's turn, white scores a point for
each of its pieces that attacks the queen. On black's turn, black scores a point
for each white piece the queen attacks. Pieces don't block each other, as the
original assignment specified.

### 16-bit pattern analysis

```console
$ python -m ergasies.bit_patterns examples/sample.txt
16-bit numbers: 98
even              39.80%
divisible by 3    37.76%
divisible by 5    24.49%
divisible by 7    11.22%
```

### Runs in drand public randomness

```console
$ python -m ergasies.drand_runs --rounds 100
Analysed 25600 bits from 100 rounds
Longest run of 0s: 19
Longest run of 1s: 15
```

Each run fetches live data, so your numbers will differ. Use `--endpoint` to
point at another drand HTTP relay.

## Running the tests

```bash
python -m pytest            # or, without installing anything:
python -m unittest discover -s tests -t .
```

## Project structure

```text
ergasies/
├── word_lengths.py     # text cleaning + word-length histogram
├── chess_attacks.py    # rook/bishop vs queen Monte Carlo game
├── bit_patterns.py     # 7-bit → 16-bit packing and divisibility stats
└── drand_runs.py       # longest bit runs in drand beacon output
tests/                  # unittest test suite (also runs under pytest)
examples/sample.txt     # sample input for the text-based tools
```

## License

[GPL-3.0](LICENSE)
