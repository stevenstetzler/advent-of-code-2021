import numpy as np
import io
import argparse

def print_energies(energies, flashed):
    for i, row in enumerate(energies):
        for j, energy in enumerate(row):
            if flashed[i, j]:
                print(f"[{energy}]", end="")
            else:
                print(f" {energy} ", end="")
        print("")
    print("")

def step(energies):
    rows, cols = energies.shape
    energies = np.copy(energies)
    flashed = np.zeros_like(energies, dtype=bool)
    
    # First, the energy level of each octopus increases by 1.
    energies += 1
    # Then, any octopus with an energy level greater than 9 flashes. 
    # This increases the energy level of all adjacent octopuses by 1, 
    # including octopuses that are diagonally adjacent. If this causes 
    # an octopus to have an energy level greater than 9, it also flashes. 
    # This process continues as long as new octopuses keep having their 
    # energy level increased beyond 9. (An octopus can only flash at most 
    # once per step.)
    while True:
        to_process = (energies > 9) & ~flashed
        if np.any(to_process):
            will_flash = np.where(to_process)
            for i, j in zip(*will_flash):
                flashed[i, j] = True
                left = (i, j - 1)
                right = (i, j + 1)
                up = (i - 1, j)
                down = (i + 1, j)
                upleft = (i - 1, j - 1)
                upright = (i - 1, j + 1)
                downleft = (i + 1, j - 1)
                downright = (i + 1, j + 1)
                add_to = [left, right, up, down, upleft, upright, downleft, downright]
                # boundary conditions
                add_to = list(
                    filter(
                        lambda p : (p[0] >= 0) and (p[0] < rows) and (p[1] >= 0) and (p[1] < cols), 
                        add_to
                    )
                )
                for p in add_to:
                    energies[p] += 1
        else:
            break 
    # Finally, any octopus that flashed during this step has its energy 
    # level set to 0, as it used all of its energy to flash.
    energies[flashed] = 0

    return energies, flashed

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
    energies = np.zeros((len(lines), len(lines[0])), dtype=int)
    rows, cols = energies.shape
    for i, line in enumerate(lines):
        for j, d in enumerate(line):
            energies[i, j] = int(d)
    
    i = 0
    while True:
        i += 1
        energies, flashed = step(energies)
        if verbose:
            print(f"After step {i}:")
            print_energies(energies, flashed)
        if np.all(flashed):
            break
    print(f"All flashed after step {i}")

if __name__ == "__main__":
    main()
