import numpy as np
import io
import argparse

def check_syntax(line, verbose=False):
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
                if verbose:
                    print(f"{line} - Expected {close_symbols[i]}, but found {c} instead.")
                return score_lookup[c], "corrupted"
    if len(opened) > 1:
        # incomplete
        return 0, "incomplete"
    else:
        # complete and valid
        return 0, "valid"

def complete_syntax(line, verbose=False):
    # assumes an incomplete string
    open_symbols = np.array(["[", "(", "{", "<"])
    close_symbols = np.array(["]", ")", "}", ">"])
    score_lookup = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    opened = []
    for c in line:
        if c in open_symbols:
            opened.append(c)
        elif c in close_symbols:
            # remove from opened
            opened = opened[:-1]
    
    if len(opened) == 0:
        # complete
        return 0, []
    else:
        # go in reverse order
        opened = opened[::-1]
        # need to complete
        completion = []
        score = 0
        for c in opened:
            i = np.where(open_symbols == c)[0][0]
            completion.append(close_symbols[i])
            score *= 5
            score += score_lookup[close_symbols[i]]
        if verbose:
            print("Complete by adding", "".join(completion), f"- {score} points")
        return score, completion

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
        _, state = check_syntax(line, verbose=False)
        if state == "incomplete":
            score, completion = complete_syntax(line, verbose=verbose)
            scores.append(score)
        else:
            continue
    scores = sorted(scores)
    print(scores)
    middle_score = scores[int(len(scores) / 2)]
    print(middle_score)

if __name__ == "__main__":
    main()
