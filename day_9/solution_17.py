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

    lines = [l.strip() for l in lines]

    heightmap = np.zeros((len(lines), len(lines[0])), dtype=int)
    rows, cols = heightmap.shape
    for i, line in enumerate(lines):
        for j, d in enumerate(line):
            heightmap[i, j] = int(d)

    risk = 0
    for i, row in enumerate(heightmap):
        for j, height in enumerate(row):
            if (i == 0) and (j == 0):
                is_min = (
                    (height < heightmap[i + 1, j]) and 
                    (height < heightmap[i, j + 1]) 
                )
            elif (i == rows - 1) and (j == 0):
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j + 1]) 
                )
            elif (i == 0) and (j == cols - 1):
                is_min = (
                    (height < heightmap[i + 1, j]) and 
                    (height < heightmap[i, j - 1]) 
                )
            elif (i == rows - 1) and (j == cols - 1):
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j - 1]) 
                )
            elif (i == 0):
                is_min = (
                    (height < heightmap[i + 1, j]) and 
                    (height < heightmap[i, j - 1]) and
                    (height < heightmap[i, j + 1])
                )
            elif (i == rows - 1):
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j - 1]) and
                    (height < heightmap[i, j + 1])
                )
            elif (j == 0):
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j + 1]) and
                    (height < heightmap[i + 1, j])
                )
            elif (j == cols - 1):
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j - 1]) and
                    (height < heightmap[i + 1, j])
                )
            else:
                is_min = (
                    (height < heightmap[i - 1, j]) and 
                    (height < heightmap[i, j - 1]) and
                    (height < heightmap[i, j + 1]) and
                    (height < heightmap[i + 1, j])
                )
            if is_min:
                print(f"[{height}]", end="")
                risk += 1 + height
            else:
                print(" " + str(height), end=" ")
        print("")
    
    print(risk)






if __name__ == "__main__":
    main()
