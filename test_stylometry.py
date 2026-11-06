"""Checks for length-controlled vocabulary and repeated-phrase scoring."""

import unittest

import stylometry


class StyleFeatureTests(unittest.TestCase):
    def test_sliding_windows_match_reference(self):
        text = "one two three one two four five one"
        tokens = stylometry.words(text)
        expected = sum(len(set(tokens[i:i + 4])) / 4
                       for i in range(len(tokens) - 3)) / (len(tokens) - 3)
        self.assertAlmostEqual(stylometry.windowed_type_token_ratio(text, 4), expected)

    def test_fixed_windows_reduce_whole_text_length_effect(self):
        block = " ".join(f"word{i}" for i in range(50))
        longer = " ".join([block] * 4)
        self.assertEqual(stylometry.windowed_type_token_ratio(block), 1.0)
        self.assertEqual(stylometry.windowed_type_token_ratio(longer), 1.0)
        self.assertLess(stylometry.type_token_ratio(longer), 1.0)

    def test_short_text_uses_available_words(self):
        text = "one two one"
        self.assertEqual(stylometry.windowed_type_token_ratio(text), 2 / 3)
        with self.assertRaises(ValueError):
            stylometry.windowed_type_token_ratio(text, 0)

    def test_phrase_duplicates_have_known_fraction(self):
        self.assertEqual(stylometry.repeated_phrase_ratio("one two three. one two three."), 0.5)
        self.assertEqual(stylometry.repeated_phrase_ratio("one two three. four five six."), 0.0)

    def test_phrases_do_not_cross_sentence_boundaries(self):
        self.assertEqual(stylometry.repeated_phrase_ratio("one two. three four. one two. three four."), 0.0)

    def test_repetition_cannot_be_hidden_by_unique_padding(self):
        text = " ".join(["one two three four five."] * 12)
        score = stylometry.style_signal(text)
        self.assertGreaterEqual(score + 0.00005, stylometry.repeated_phrase_ratio(text))

    def test_empty_unsupported_and_varied_inputs_are_bounded(self):
        for text in ("", "!!!", "مرحبا بالعالم", "one", "one two three.",
                     "one two three. " * 100):
            score = stylometry.style_signal(text)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
        self.assertEqual(stylometry.style_signal("!!!"), 0.5)


if __name__ == "__main__":
    unittest.main()
