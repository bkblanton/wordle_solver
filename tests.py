import unittest

from wordle_solver.constants import DEFAULT_HARD_MODE, DEFAULT_MAX_GUESSES
from wordle_solver.corpus import Corpus
from wordle_solver.solver import Solver
from wordle_solver.clue import Colors, Color


class ColorTestCase(unittest.TestCase):

    def test_parse(self):
        self.parse_subtest(Colors(), '')
        self.parse_subtest(Colors((Color.GREY, Color.YELLOW, Color.GREEN)), '012')

    def parse_subtest(self, expected_colors: Colors, color_str: str):
        with self.subTest():
            self.assertEqual(expected_colors, Colors.parse(color_str))

    def test_from_words(self):
        self.from_words_subtest('', '', '')
        self.from_words_subtest('2', 'a', 'a')
        self.from_words_subtest('0', 'b', 'a')
        self.from_words_subtest('11', 'ba', 'ab')
        self.from_words_subtest('1122', 'baba', 'abba')
        self.from_words_subtest('102', 'bbb', 'aabb')

    def from_words_subtest(self, expected_color_str: str, guess: str, answer: str):
        with self.subTest():
            self.assertEqual(Colors.parse(expected_color_str), Colors.from_words(guess, answer))


class SolverTestCase(unittest.TestCase):

    def test_solver(self):
        self.solver_subtest()
        self.solver_subtest(hard_mode=True)

    def solver_subtest(self, hard_mode=DEFAULT_HARD_MODE):
        def get_path_to(word):
            corpus = Corpus(min_word_freq=10 ** -5, word_len=len(word))
            solver = Solver(corpus=corpus, min_freq_ratio=0.5, hard_mode=hard_mode)
            return list(solver.path_to(word))
        with self.subTest():
            clues = get_path_to('snake')
            self.assertLess(1, len(clues))
            self.assertEqual('snake', clues[-1].guess)
        with self.subTest():
            clues = get_path_to('abcde')
            self.assertLess(1, len(clues))
            self.assertGreater(DEFAULT_MAX_GUESSES, len(clues))


if __name__ == '__main__':
    unittest.main()
