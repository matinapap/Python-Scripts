import unittest

from ergasies.word_lengths import format_histogram, length_histogram, remove_pairs, tokenize


class TokenizeTest(unittest.TestCase):
    def test_strips_digits_and_punctuation(self):
        self.assertEqual(tokenize("Hello, world! 123 e-mail"), ["Hello", "world", "email"])

    def test_newlines_separate_words(self):
        self.assertEqual(tokenize("one\ntwo"), ["one", "two"])


class RemovePairsTest(unittest.TestCase):
    def test_removes_first_matching_partner(self):
        words = ["a" * 10, "b" * 3, "c" * 10, "d" * 10]
        self.assertEqual(remove_pairs(words), ["b" * 3, "d" * 10])

    def test_keeps_words_without_partner(self):
        self.assertEqual(remove_pairs(["abc", "de"]), ["abc", "de"])

    def test_does_not_mutate_input(self):
        words = ["a" * 15, "b" * 5]
        remove_pairs(words)
        self.assertEqual(len(words), 2)


class HistogramTest(unittest.TestCase):
    def test_counts_by_length(self):
        self.assertEqual(length_histogram(["a", "bb", "cc", "dddd"]), [1, 2, 0, 1])

    def test_empty(self):
        self.assertEqual(length_histogram([]), [])

    def test_format_uses_singular_for_one_letter(self):
        self.assertEqual(
            format_histogram([1, 2]),
            "Words with  1 letter: 1\nWords with  2 letters: 2",
        )


if __name__ == "__main__":
    unittest.main()
