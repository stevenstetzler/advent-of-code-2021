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

    timers = np.array([int(s.strip()) for s in lines[0].split(",")]).astype(int)
    if verbose:
        print(f"Initial state:", ",".join(map(str, timers)))
    
    timer_counts = {
        i : 0
        for i in range(9)
    }
    for timer in timers:
        timer_counts[timer] += 1
    
    print(timer_counts)

    for day in range(ndays):
        new_timer_counts = {i : 0 for i in range(9)}
        # 0 fish create 8 fish
        num_spawn = timer_counts[0]
        new_timer_counts[8] = num_spawn
        # 0 fish reset to 6 fish
        new_timer_counts[6] = num_spawn
        for i in range(0, 8):
            # n fish count down to n - 1
            new_timer_counts[i] += timer_counts[i + 1]
        
        timer_counts = new_timer_counts
        if verbose:
            print(f"After {day + 1} days: ", timer_counts)
            
    print(timer_counts)
    num_fish = sum(timer_counts.values())
    print(f"After {ndays} days there are {num_fish} fish")

if __name__ == "__main__":
    main()
