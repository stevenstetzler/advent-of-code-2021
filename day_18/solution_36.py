import numpy as np
import io
import argparse
from solution_35 import parse_number, reduce, add, magnitude

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

    numbers = []
    for line in lines:
        numbers.append(parse_number(eval(line)))

    largest_mag = -np.inf
    largest_pair = None
    for i, n in enumerate(numbers):
        for j, m in enumerate(numbers):
            if i == j:
                continue
            number = reduce(add(n.copy(), m.copy()))
            if magnitude(number) > largest_mag:
                largest_mag = magnitude(number)
                largest_pair = (n.copy(), m.copy())

    print("Largest magnitude is", largest_mag, "from", largest_pair[0], "+", largest_pair[1])
            

if __name__ == "__main__":
    main()
