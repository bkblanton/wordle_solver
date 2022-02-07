from functools import cache
from typing import Iterable, Iterator

from wordfreq import word_frequency, iter_wordlist

from wordle_solver.constants import DEFAULT_WORD_LEN, DEFAULT_MIN_FREQ, DEFAULT_LANGUAGE


class Corpus(Iterable[str]):

    def __init__(self,
                 language: str = DEFAULT_LANGUAGE,
                 word_len: int = DEFAULT_WORD_LEN,
                 min_word_freq: float = DEFAULT_MIN_FREQ):
        self._language = language
        self._word_len = word_len
        self._min_word_freq = min_word_freq

    def __iter__(self) -> Iterator[str]:
        return iter(self._wordlist)

    def __contains__(self, word: str) -> bool:
        return len(word) == self._word_len and word.isalpha() and self.get_freq(word) > self._min_word_freq

    def get_freq(self, word: str) -> float:
        return word_frequency(word, self._language)

    def iter_weighted_head(self, min_freq_ratio: float, words: Iterable[str]) -> Iterator[str]:
        mean_freq = 1.0
        for i, word in enumerate(words, 1):
            mean_freq = mean_freq * ((i - 1)/i) + self.get_freq(word) * (1/i)
            if self.get_freq(word) / mean_freq <= min_freq_ratio:
                break
            yield word

    @property
    @cache
    def _wordlist(self):
        return tuple((word for word in iter_wordlist(self._language) if word in self))
