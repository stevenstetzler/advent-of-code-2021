import numpy as np
import io
import argparse
from solution_31 import unpackage, hex_to_binary

actions = {
    0: sum,
    1: np.product,
    2: min,
    3: max,
    5: lambda x : int(x[0] > x[1]),
    6: lambda x : int(x[0] < x[1]),
    7: lambda x : int(x[0] == x[1]),
}

def generate_value(packet):
    if type(packet['value']) is list:
        action = actions[packet['type_id']]
        return action([generate_value(sub_packet) for sub_packet in packet['value']])
    else:
        return packet['value']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--test-num", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    test_num = args.test_num
    verbose = args.verbose

    if test:
        infile = f"test_input_{test_num}"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    hex = lines[0]
    packet = hex_to_binary(hex)
    packets = unpackage(packet, verbose=verbose)
    if verbose:
        print("packets:", packets)

    print(generate_value(packets[0]))
    
if __name__ == "__main__":
    main()
