# Wordle Solver

A Wordle solving CLI that uses entropy to solve Wordle puzzles.

## Quickstart
```sh
git clone https://github.com/bkblanton/wordle_solver.git && cd wordle_solver
python3 -m pip install -r requirements.txt
python3 -m wordle_solver --help
python3 -m wordle_solver -c snake 01210
```
## Clue colors
- 0 = gray
- 1 = yellow
- 2 = green

## Usage
```
usage: __main__.py [-h] [-c [CLUES ...]] [-i INTERACTIVE] [-m] [-t [TEST ...]] [-n TOP_N] [--language LANGUAGE] [--max_guesses MAX_GUESSES] [--word_len WORD_LEN]
                   [--min_freq MIN_FREQ] [--min_freq_ratio MIN_FREQ_RATIO]

options:
  -h, --help            show this help message and exit
  -c [CLUES ...], --clues [CLUES ...]
                        sequence of guess and clue pairs
  -i INTERACTIVE, --interactive INTERACTIVE
                        interactive mode
  -m, --hard_mode       hard mode
  -t [TEST ...], --test [TEST ...]
                        sequence of answers to test
  -n TOP_N, --top_n TOP_N
                        sequence of answers to test
  --language LANGUAGE   language identifier
  --max_guesses MAX_GUESSES
                        maximum number of guesses
  --word_len WORD_LEN   word length
  --min_freq MIN_FREQ   corpus minimum word frequency
  --min_freq_ratio MIN_FREQ_RATIO
                        internal solver parameter which affects speed vs precision
```
