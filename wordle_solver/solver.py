from collections import Counter, OrderedDict
from functools import cache
from itertools import chain
from math import log2
from typing import Iterable, Iterator, Sequence, NamedTuple

from wordle_solver.clue import Clue, ClueSet, Colors
from wordle_solver.constants import DEFAULT_MIN_FREQ_RATIO, DEFAULT_MAX_GUESSES
from wordle_solver.corpus import Corpus


class Solver(NamedTuple):
    clues: ClueSet = ClueSet()
    corpus: Corpus = Corpus()
    hard_mode: bool = False
    min_freq_ratio: float = DEFAULT_MIN_FREQ_RATIO

    @property
    @cache
    def best_guesses(self) -> Sequence[str]:
        scores = {word: self.get_score(word) for word in self.choices}
        choices = (word for word, score in scores.items() if score > 0)
        return tuple(sorted(choices, key=scores.get, reverse=True))

    @property
    @cache
    def choices(self) -> Iterable[str]:
        choices = self.matches
        if not self.hard_mode and len(self.clues) > 1:
            extra_choices = self.iter_fuzzy_matches()
            choices = OrderedDict.fromkeys(chain(choices, extra_choices)).keys()
        return choices

    @property
    @cache
    def matches(self) -> Sequence[str]:
        return tuple(self.iter_weighted_head(self.clues.iter_matches(self.corpus)))

    @cache
    def with_clue(self, clue: Clue) -> 'Solver':
        return Solver(self.clues | {clue}, self.corpus, self.hard_mode, self.min_freq_ratio)

    def path_to(self, true_word: str, max_guesses=DEFAULT_MAX_GUESSES) -> Iterable[Clue]:
        solver = self
        for i in range(max_guesses):
            if not solver.matches:
                break
            guess = solver.best_guesses[0]
            clue = Clue.from_guess(guess, true_word)
            yield clue
            if guess == true_word:
                break
            solver = solver.with_clue(clue)

    @cache
    def get_score(self, guess: str) -> float:
        if not self.matches:
            return 0
        true_guess_weight = 0
        false_guess_weight = 0
        clue_freq = Counter()
        for word in self.matches:
            freq = self.corpus.get_freq(word)
            if word == guess:
                true_guess_weight += freq
            else:
                false_guess_weight += freq
                clue_freq[Colors.from_words(guess, word)] += freq
        proportions = (weight / false_guess_weight for weight in clue_freq.values())
        entropy = sum(-p * log2(p) for p in proportions)
        total_weight = true_guess_weight + false_guess_weight
        entropy_proportion = false_guess_weight / total_weight
        return 1 - entropy_proportion * 2 ** -entropy

    def iter_fuzzy_matches(self) -> Iterator[str]:
        return self.iter_weighted_head(self.clues.iter_fuzzy_matches(self.corpus))

    def iter_weighted_head(self, words: Iterable[str]) -> Iterator[str]:
        return self.corpus.iter_weighted_head(self.min_freq_ratio, words)
