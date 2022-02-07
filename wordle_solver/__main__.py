from argparse import ArgumentParser, Namespace
from itertools import islice
from sys import stderr
from typing import Iterable

from wordle_solver.clue import ClueSet, Colors, Clue
from wordle_solver.corpus import Corpus
from wordle_solver.solver import Solver
from wordle_solver.constants import DEFAULT_MAX_GUESSES, DEFAULT_WORD_LEN, DEFAULT_MIN_FREQ, DEFAULT_MIN_FREQ_RATIO, DEFAULT_LANGUAGE

_PROMPT = '> '


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-c', '--clues', nargs='*', help='sequence of guess and clue pairs')
    parser.add_argument('-i', '--interactive', default=True, type=bool, help='interactive mode')
    parser.add_argument('-m', '--hard_mode', action='store_true', help='hard mode')
    parser.add_argument('-t', '--test', nargs='*', help='sequence of answers to test')
    parser.add_argument('-n', '--top_n', default=10, type=int, help='sequence of answers to test')
    parser.add_argument('--language', default=DEFAULT_LANGUAGE, help='language identifier')
    parser.add_argument('--max_guesses', default=DEFAULT_MAX_GUESSES, type=int, help='maximum number of guesses')
    parser.add_argument('--word_len', default=DEFAULT_WORD_LEN, type=int, help='word length')
    parser.add_argument('--min_freq', default=DEFAULT_MIN_FREQ, type=float, help='corpus minimum word frequency')
    parser.add_argument('--min_freq_ratio', default=DEFAULT_MIN_FREQ_RATIO, type=float,
                        help='internal solver parameter which affects speed vs precision')
    return parser.parse_args()


def main(args: Namespace):
    clues = parse_clues(args.clues) if args.clues else ClueSet()
    corpus = Corpus(word_len=args.word_len, min_word_freq=args.min_freq)
    solver = Solver(clues, corpus, hard_mode=args.hard_mode, min_freq_ratio=args.min_freq_ratio)
    if args.test is not None:
        test_mode_main(solver, args)
    else:
        clue_mode_main(args, solver)


def parse_clues(tokens: Iterable[str]) -> ClueSet:
    pairs = zip(islice(tokens, None, None, 2), islice(tokens, 1, None, 2))
    return ClueSet((Clue(guess, Colors.parse(color_str)) for guess, color_str in pairs))


def clue_mode_main(args: Namespace, solver: Solver):
    print_top_n(solver, args)
    if not args.interactive:
        return
    while len(solver.clues) < args.max_guesses:
        if len(solver.matches) <= 1:
            return
        try:
            guess, color_str = input(_PROMPT).split(maxsplit=1)
            solver = solver.with_clue(Clue(guess, Colors.parse(color_str)))
        except ValueError as e:
            print(f'Invalid input. Example: {_PROMPT}snake 01210\nError: {e}', file=stderr)
            continue
        print_top_n(solver, args)


def print_top_n(solver: Solver, args: Namespace):
    for _, word in zip(range(args.top_n), solver.best_guesses):
        print(word, solver.get_score(word), sep='\t')


def test_mode_main(solver: Solver, args: Namespace):
    for answer in args.test:
        print_path(answer, args, solver)
    if args.interactive:
        while True:
            answer = input('> ')
            if not answer:
                break
            print_path(answer, args, solver)


def print_path(answer: str, args: Namespace, solver: Solver):
    print(solver.path_to(answer, max_guesses=args.max_guesses))


if __name__ == '__main__':
    main(parse_args())
