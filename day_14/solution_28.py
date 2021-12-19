import numpy as np
import io
import argparse

def insert(pairs, insertions, first_pair):
    add_pairs = {}
    remove_pairs = {}
    handle_first_pair = True
    for pair, action in insertions:
        if pair in pairs.keys():
            if pair == first_pair and handle_first_pair:
                first_pair = pair[0] + action
                handle_first_pair = False

            add_if_exists(add_pairs, pair[0] + action, pairs[pair])
            add_if_exists(add_pairs, action + pair[1], pairs[pair])
            add_if_exists(remove_pairs, pair, pairs[pair])
    
    for pair, num in add_pairs.items():
        add_if_exists(pairs, pair, num)
    for pair, num in remove_pairs.items():
        add_if_exists(pairs, pair, -1 * num)
    
    return first_pair

def add_if_exists(d, k, v):
    if d.get(k, None):
        d[k] += v
    else:
        d[k] = v

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("nsteps", type=int)

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose
    nsteps = args.nsteps

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    template, insertions = "\n".join(lines).split("\n\n")
    insertions = insertions.split("\n")
    insertions = [tuple([c.strip() for c in i.split(" -> ")]) for i in insertions]
    template = template.strip()
    first_pair = template[0:2]
    pairs = {}
    for i in range(len(template) - 1):
        pair = template[i:i+2] 
        add_if_exists(pairs, pair, 1)

    if verbose:
        print("Template:    ", template)

    for i in range(nsteps):
        first_pair = insert(pairs, insertions, first_pair)
        if verbose:
            print(f"After step {i+1}:", pairs)

    letters = np.unique(sum([list(p) for p in pairs.keys()], []))
    num_letters = {l : 0 for l in letters}
    for letter in letters:
        for pair in pairs.keys():
            if letter == pair[1]:
                num_letters[letter] += pairs[pair]

        if letter == first_pair[0]:
            num_letters[letter] += 1

    counts = np.array([num_letters[letter] for letter in letters])
    print("polymer length:", sum(num_letters.values()))
    print("least common:", letters[np.argmin(counts)], np.min(counts))
    print("most common:", letters[np.argmax(counts)], np.max(counts))
    print(f"{np.max(counts)} - {np.min(counts)} = {np.max(counts) - np.min(counts)}")

if __name__ == "__main__":
    main()
