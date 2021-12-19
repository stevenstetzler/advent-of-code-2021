import numpy as np
import io
import argparse

def insert(template, insertions):
    template = list(template)
    new = list(template)
    modifications = []
    for pair, insertion in insertions:
        for i, c in enumerate(template):
            if i == len(template) - 1:
                break
            if template[i] == pair[0] and template[i + 1] == pair[1]:
                modifications.append((i + 1, insertion))
    
    new = list(template)
    modifications = sorted(modifications, key=lambda x : x[0])
    while len(modifications) > 0:
        index, insertion = modifications[0]
        new.insert(index, insertion)
        modifications = [(i + 1, _) for i, _ in modifications[1:]]
    return new

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
    template = template.strip()
    insertions = insertions.split("\n")
    insertions = [tuple([c.strip() for c in i.split(" -> ")]) for i in insertions]

    if verbose:
        print("Template:    ", template)

    polymer = template
    for i in range(nsteps):
        polymer = insert(polymer, insertions)
        if verbose:
            print(f"After step {i+1}:", "".join(polymer))

    elements = np.unique(polymer)
    num_elements = []
    for e in elements:
        num_elements.append((np.array(polymer) == e).sum())
    print("polymer length:", len(polymer))
    print("least common:", elements[np.argmin(num_elements)], np.min(num_elements))
    print("most common:", elements[np.argmax(num_elements)], np.max(num_elements))
    print(f"{np.max(num_elements)} - {np.min(num_elements)} = {np.max(num_elements) - np.min(num_elements)}")

if __name__ == "__main__":
    main()
