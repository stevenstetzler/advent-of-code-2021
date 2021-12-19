import numpy as np
import io
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ndays", type=int)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    ndays = args.ndays
    test = args.test
    verbose = args.verbose

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()

    timers = [int(s.strip()) for s in lines[0].split(",")]
    if verbose:
        print(f"Initial state:", ",".join(map(str, timers)))
    for day in range(ndays):
        updated_timers = [t for  t in timers]
        for i, timer in enumerate(timers):
            if timer == 0:
                updated_timers[i] = 6
                updated_timers.append(8)
            else:
                updated_timers[i] -= 1
        timers = updated_timers
        if verbose:
            print(f"After {day + 1} days:", ",".join(map(str, timers)))
    
    print(f"After {ndays} days there are {len(timers)} fish")

if __name__ == "__main__":
    main()
