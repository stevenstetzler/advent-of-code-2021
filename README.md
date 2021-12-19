# advent-of-code-2021
Advent of Code 2021 solutions

Solutions written in Python. Requires Python 3 and the `numpy` package.

Run a particular solution with:
```
$ ./execute.py <day> --problem <problem>
```
and verify against the shared test input with
```
$ ./execute.py <day> --problem <problem> --test
```
Some solutions require input (e.g. number of iterations) which can be passed with
```
$ ./execute.py <day> --problem <problem> --test --extra [extra]
```
For example, getting the solution for problem 2 of day 14 with the test input and 10 steps:
```
$ ./execute.py 14 --problem 2 --test --extra 10
# executing 'python3 solution_28.py --test 10' in /Users/steven/Projects/advent-of-code-2021/day_14
polymer length: 3073
least common: H 161
most common: B 1749
1749 - 161 = 1588
```