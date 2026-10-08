import unittest
from unittest.mock import patch

from src import drand_runs
from src.drand_runs import collect_bits, hex_to_bits, longest_runs


class DrandRunsTest(unittest.TestCase):
    def test_hex_to_bits_keeps_leading_zeros(self):
        self.assertEqual(hex_to_bits("0f"), "00001111")

    def test_longest_runs(self):
        self.assertEqual(longest_runs("0011100010"), {"0": 3, "1": 3})
        self.assertEqual(longest_runs("1111"), {"0": 0, "1": 4})
        self.assertEqual(longest_runs(""), {"0": 0, "1": 0})

    def test_collect_bits_walks_back_from_latest_round(self):
        rounds = {"latest": {"round": 10, "randomness": "ff"}, "9": {"round": 9, "randomness": "00"}}
        with patch.object(drand_runs, "fetch_round", side_effect=lambda _, r="latest": rounds[r]) as fetch:
            self.assertEqual(collect_bits("https://example.test", 2), "1111111100000000")
        self.assertEqual(fetch.call_count, 2)


if __name__ == "__main__":
    unittest.main()
