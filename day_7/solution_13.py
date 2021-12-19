import numpy as np
import io
import argparse

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

    positions = np.array([int(s.strip()) for s in lines[0].split(",")]).astype(int)
    max_position = positions.max()
    min_position = positions.min()

    fuels = []
    for x in range(min_position, max_position + 1):
        fuel = np.abs(positions - x).sum()
        fuels.append(fuel)
    
    fuels = np.array(fuels)
    print("minimimum fuel of", fuels.min(), "at", fuels.argmin() + min_position)


if __name__ == "__main__":
    main()
