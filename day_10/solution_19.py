import numpy as np
import io
import argparse

from numpy.lib.npyio import loads

def check_syntax(line):
    open_symbols = np.array(["[", "(", "{", "<"])
    close_symbols = np.array(["]", ")", "}", ">"])
    score_lookup = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    opened = []
    for c in line:
        if c in open_symbols:
            opened.append(c)
        elif c in close_symbols:
            # Check against last open symbol
            last_opened = opened[-1]
            i = np.where(open_symbols == last_opened)[0][0]
            if c == close_symbols[i]:
                # good
                opened = opened[:-1]
            else:
                # bad
                print(f"{line} - Expected {close_symbols[i]}, but found {c} instead.")
                return score_lookup[c]
    if len(opened) > 1:
        # incomplete
        return 0
    else:
        # complete and valid
        return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    
    scores = []
    for line in lines:
        score = check_syntax(line)
        scores.append(score)
    print(scores)
    print(np.sum(scores))

if __name__ == "__main__":
    main()
