"""Longest runs of 0s and 1s in public randomness from the drand beacon.

Fetches the latest drand round plus the rounds before it, converts each
round's 256-bit randomness to binary, joins all of it into one bit string
and reports the longest run of consecutive 0s and of consecutive 1s.

Usage:
    python -m src.drand_runs --rounds 100
"""

from __future__ import annotations

import argparse
import json
from itertools import groupby
from typing import Dict, List, Optional
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = "https://drand.cloudflare.com/public"


def fetch_round(endpoint: str, round_id: str = "latest", timeout: float = 10.0) -> Dict:
    """Return the JSON for one drand round (``round_id`` may be ``"latest"``)."""
    request = Request(f"{endpoint}/{round_id}", headers={"User-Agent": "ergasies/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def hex_to_bits(hex_string: str) -> str:
    """Convert a hex string to a binary string, keeping leading zeros."""
    return "".join(format(byte, "08b") for byte in bytes.fromhex(hex_string))


def longest_runs(bits: str) -> Dict[str, int]:
    """Return the longest run of consecutive ``"0"`` and ``"1"`` characters."""
    runs = {"0": 0, "1": 0}
    for bit, group in groupby(bits):
        runs[bit] = max(runs[bit], sum(1 for _ in group))
    return runs


def collect_bits(endpoint: str, rounds: int) -> str:
    """Fetch the latest ``rounds`` rounds and return their randomness as bits."""
    latest = fetch_round(endpoint)
    bits = [hex_to_bits(latest["randomness"])]
    for round_id in range(latest["round"] - 1, latest["round"] - rounds, -1):
        bits.append(hex_to_bits(fetch_round(endpoint, str(round_id))["randomness"]))
    return "".join(bits)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rounds", type=int, default=100, help="number of rounds to fetch (default: 100)")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help=f"drand HTTP API (default: {DEFAULT_ENDPOINT})")
    args = parser.parse_args(argv)

    bits = collect_bits(args.endpoint, args.rounds)
    runs = longest_runs(bits)
    print(f"Analysed {len(bits)} bits from {args.rounds} rounds")
    print(f"Longest run of 0s: {runs['0']}")
    print(f"Longest run of 1s: {runs['1']}")


if __name__ == "__main__":
    main()
