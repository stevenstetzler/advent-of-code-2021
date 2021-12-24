import numpy as np
import io
import argparse
from solution_33 import get_succesful_trajectories

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

    xrange, yrange = lines[0].split(" ")[2:]
    xrange = list(map(int, xrange.split(",")[0].split("=")[1].split("..")))
    yrange = list(map(int, yrange.split("=")[1].split("..")))

    trajectories = get_succesful_trajectories(xrange, yrange)
    print("there are", len(trajectories), "trajectories")


if __name__ == "__main__":
    main()
