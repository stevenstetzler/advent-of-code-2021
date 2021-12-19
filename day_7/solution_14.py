import numpy as np
import io
import argparse

def cache(f):
    _cache = {}

    def _f(*args):
        if args in _cache:
            return _cache[args]
        else:
            value = f(*args)
            _cache[args] = value
            return value
    
    return _f

@cache
def sum_from_0_to_n(n):
    return sum([i for i in range(0, n + 1)])

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

    fuel_costs = []
    fuel_totals = []
    for x in range(min_position, max_position + 1):
        steps = np.abs(positions - x)
        fuel_cost_per_position = list(map(sum_from_0_to_n, steps))
        fuel_total = sum(fuel_cost_per_position)
        fuel_costs.append(fuel_cost_per_position)
        fuel_totals.append(fuel_total)

    fuel_costs = np.array(fuel_costs)
    fuel_totals = np.array(fuel_totals)

    min_fuel = fuel_totals.min()
    best_fuel_index = fuel_totals.argmin()
    best_position = best_fuel_index + min_position
    if verbose:
        for i, position in enumerate(positions):
            print(f"Move from {position} to {best_position}: {fuel_costs[best_fuel_index][i]} fuel")
    
    print("minimimum fuel of", min_fuel, "at", best_position)

if __name__ == "__main__":
    main()
