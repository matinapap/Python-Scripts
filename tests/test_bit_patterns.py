import unittest

from src.bit_patterns import char_nibble, divisibility_percentages, to_16bit_numbers


class BitPatternsTest(unittest.TestCase):
    def test_char_nibble_keeps_outer_bits(self):
        self.assertEqual(char_nibble("a"), "1101")  # 'a' = 1100001

    def test_four_characters_make_one_number(self):
        # a=1101, b=1110, c=1111, d=1100
        self.assertEqual(to_16bit_numbers("abcd"), [0b1101111011111100])

    def test_spaces_are_ignored_and_short_group_is_left_padded(self):
        self.assertEqual(to_16bit_numbers("ab cd a"), [0b1101111011111100, 0b1101])

    def test_percentages(self):
        result = divisibility_percentages([2, 3, 5, 7, 210])
        self.assertEqual(result, {2: 40.0, 3: 40.0, 5: 40.0, 7: 40.0})

    def test_empty_input(self):
        self.assertEqual(divisibility_percentages([]), {2: 0.0, 3: 0.0, 5: 0.0, 7: 0.0})


if __name__ == "__main__":
    unittest.main()
