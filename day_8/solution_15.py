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
    
    signals = []
    outputs = []
    len_to_digit = {
        2: 1,
        3: 7,
        4: 4,
        7: 8,
    }
    num_unique = 0
    for line in lines:
        signal = [s.strip() for s in line.split("|")[0].split(" ") if s != ""]
        output = [s.strip() for s in line.split("|")[1].split(" ") if s != ""]
        signals.append(signal)
        outputs.append(output)

        # for s in signal:
        #     if len(s) in len_to_digit.keys():
        #         num_unique += 1
        #         print(s, end=" ")
        for o in output:
            if len(o) in len_to_digit.keys():
                num_unique += 1
                if verbose:
                    print(o, end=" ")
        if verbose:
            print("")
    
    print(num_unique)

if __name__ == "__main__":
    main()
