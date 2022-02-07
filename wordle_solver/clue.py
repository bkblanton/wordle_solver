from collections import Counter
from enum import Enum
from functools import cache
from typing import Iterable, Iterator, NamedTuple, AbstractSet


class Color(Enum):
    GREEN = 2  # right letter, right position
    YELLOW = 1  # right letter, wrong position
    GREY = 0  # wrong letter, wrong position


class Colors(tuple[Color]):

    @classmethod
    def parse(cls, string: str) -> 'Colors':
        return cls((Color(int(c)) for c in string))

    @classmethod
    def from_words(cls, guess: str, answer: str) -> 'Colors':
        word_letter_counts = _get_letter_counts(guess)
        truth_letter_counts = _get_letter_counts(answer)
        colors = [Color.GREY] * len(guess)
        # Try placing a tile for each letter from the true word.
        for true_letter, truth_letter_count in truth_letter_counts.items():
            word_truth_letter_count = word_letter_counts[true_letter]
            if not word_truth_letter_count:
                continue
            remaining = min(truth_letter_count, word_truth_letter_count)
            # Place green tiles before yellow tiles.
            for guess_index, guess_letter in enumerate(guess):
                if (guess_letter == true_letter and colors[guess_index] == Color.GREY
                        and guess_letter == answer[guess_index]):
                    colors[guess_index] = Color.GREEN
                    remaining -= 1
                    if remaining <= 0:
                        break
            else:
                for guess_index, guess_letter in enumerate(guess):
                    if guess_letter == true_letter and colors[guess_index] == Color.GREY:
                        colors[guess_index] = Color.YELLOW
                        remaining -= 1
                        if remaining <= 0:
                            break
        return cls(colors)


class Clue(NamedTuple):
    guess: str
    colors: Colors

    @classmethod
    def from_guess(cls, guess_word: str, true_word: str) -> 'Clue':
        return cls(guess_word, Colors.from_words(guess_word, true_word))

    @cache
    def matches(self, word) -> bool:
        return Colors.from_words(self.guess, word) == self.colors


class ClueSet(frozenset[Clue]):

    def __or__(self, other: AbstractSet[Clue]) -> 'ClueSet':
        return ClueSet(super().__or__(other))

    @cache
    def all_match(self, word: str) -> bool:
        return all(clue.matches(word) for clue in self)

    @cache
    def any_match(self, word: str) -> bool:
        return any(clue.matches(word) for clue in self)

    def iter_matches(self, words: Iterable[str]) -> Iterator[str]:
        return (word for word in words if self.all_match(word))

    def iter_fuzzy_matches(self, words: Iterable[str]) -> Iterator[str]:
        return (word for word in words if self.any_match(word))


@cache
def _get_letter_counts(word: str) -> Counter:
    return Counter(word)
