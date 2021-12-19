import numpy as np
import io
import argparse

def print_paper(paper):
    for i, row in enumerate(paper):
        for j, data in enumerate(row):
            if data > 0:
                print(f"#", end="")
            else:
                print(f".", end="")
        print("")
    print("")

def num_visible(paper):
    return (paper > 0).sum()

def fold(paper, index, along):
    rows, cols = paper.shape
    if along == "y":        
        # 15 rows
        # fold at 0: 14 left
        # fold at 1: 13 left
        # fold at 6: 8 left
        # fold at 7: 7 left
        # fold at 8: 8 left
        half_way = int(rows/2)
        folded_rows = half_way + np.abs(index - half_way)
        folded_cols = cols
    elif along == "x":
        half_way = int(cols/2)
        folded_rows = rows
        folded_cols = half_way + np.abs(index - half_way)
    else:
        raise Exception("along must be 'x' or 'y'")
    
    folded_paper = np.zeros((folded_rows, folded_cols))
    for i, row in enumerate(paper):
        for j, data in enumerate(row):
            if along == "y" and i == index:
                continue
            elif along == "x" and j == index:
                continue
            if along == "y":
                folded_i = i if (i < index) else folded_rows - (i - index)
                folded_j = j
            elif along == "x":
                folded_i = i
                folded_j = j if (j < index) else folded_cols - (j - index)
            folded_paper[folded_i, folded_j] += paper[i, j]
    
    return folded_paper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nfolds", type=int)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose
    nfolds = args.nfolds

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    dots, instructions = "\n".join(lines).split("\n\n")
    dots = dots.split("\n")
    dots = [list(map(int, d.split(","))) for d in dots]
    dots = np.array(dots)
    instructions = instructions.split("\n")
    instructions = [tuple(i.split("fold along ")[1].split("=")) for i in instructions]
    instructions = [(i[0], int(i[1])) for i in instructions]

    paper = np.zeros((np.max(dots[:, 1]) + 1, np.max(dots[:, 0]) + 1))

    rows, cols = paper.shape
    for x, y in dots:
        paper[y, x] = 1
    
    if verbose:
        print("starting paper")
        print_paper(paper)

    for i, (along, index) in enumerate(instructions):
        if i >= nfolds and nfolds != -1:
            break
        paper = fold(paper, index, along)
        if verbose:
            print(f"fold along {along}={index}")
            print_paper(paper)

    print("There are", num_visible(paper), "dots visible")

if __name__ == "__main__":
    main()
