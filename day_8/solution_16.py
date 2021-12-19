import argparse

def determine_mapping_from_signals(signals):
    #   0:      1:      2:      3:      4:
    #  aaaa    ....    aaaa    aaaa    ....
    # b    c  .    c  .    c  .    c  b    c
    # b    c  .    c  .    c  .    c  b    c
    #  ....    ....    dddd    dddd    dddd
    # e    f  .    f  e    .  .    f  .    f
    # e    f  .    f  e    .  .    f  .    f
    #  gggg    ....    gggg    gggg    ....

    #   5:      6:      7:      8:      9:
    #  aaaa    aaaa    aaaa    aaaa    aaaa
    # b    .  b    .  .    c  b    c  b    c
    # b    .  b    .  .    c  b    c  b    c
    #  dddd    dddd    ....    dddd    dddd
    # .    f  e    f  .    f  e    f  .    f
    # .    f  e    f  .    f  e    f  .    f
    #  gggg    gggg    ....    gggg    gggg

    one = [s for s in signals if len(s) == 2][0]
    seven = [s for s in signals if len(s) == 3][0]
    four = [s for s in signals if len(s) == 4][0]
    eight = [s for s in signals if len(s) == 7][0]

    len_five = [s for s in signals if len(s) == 5]
    len_six = [s for s in signals if len(s) == 6]

    two, three, five = None, None, None
    for digit in len_five:
        if len(set(digit).difference(set(one))) == 3:
            three = digit
        else:
            if len(set(digit).difference(set(four))) == 3:
                two = digit
            elif len(set(digit).difference(set(four))) == 2:
                five = digit
            else:
                print("len five digit that doesn't fit")
    
    zero, six, nine = None, None, None
    for digit in len_six:
        if len(set(digit).difference(set(one))) == 5:
            six = digit
        else:
            if len(set(digit).difference(set(four))) == 3:
                zero = digit
            elif len(set(digit).difference(set(four))) == 2:
                nine = digit
            else:
                print("len six digit not determined")
    
    digits = [zero, one, two, three, four, five, six, seven, eight, nine]
    assert(all([d is not None for d in digits]))
    return digits

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

    sum_outputs = 0
    for line in lines:
        signals = line.split("|")[0].strip().split(" ")
        output = line.split("|")[1].strip().split(" ")
        digits = determine_mapping_from_signals(signals)
        print(" ".join(output), end=": ")
        output_value_string = ""
        for o in output:
            for i, d in enumerate(digits):
                if len(o) == len(d):
                    if len(set(o).difference(set(d))) == 0:
                        print(i, end="")
                        output_value_string += str(i)
                        break
        output_value = int(output_value_string)
        sum_outputs += output_value
        print("")
    print(sum_outputs)

if __name__ == "__main__":
    main()
