import numpy as np
import io
import argparse

def determine_basin(start, heightmap, maxheight=9):
    rows, cols = heightmap.shape
    basin = [start]
    consider = [start]
    considered = []
    while True:
        point = consider[0]
        considered.append(point)
        i, j = point
        # consider points around this one
        left = (i - 1, j)
        right = (i + 1, j)
        up = (i, j - 1)
        down = (i, j + 1)
        # apply boundary conditions
        for pt in [left, right, up, down]:
            if (pt[0] > -1) and (pt[0] < rows) and (pt[1] > -1) and (pt[1] < cols):
                consider.append(pt)
        consider = [pt for pt in consider if pt not in considered]
        # reject points that hit the max
        consider = [pt for pt in consider if heightmap[pt] != maxheight]
        if len(consider) == 0:
            break
        else:
            basin += [point]
    return basin

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

    basin_sizes = []
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
                basin = determine_basin((i, j), heightmap)
                if verbose:
                    for _i in range(rows):
                        for _j in range(cols):
                            if (_i, _j) in basin:
                                print(f"[{heightmap[_i, _j]}]", end="")
                            else:
                                print(f" {heightmap[_i, _j]} ", end="")
                        print("")
                    print("")
                basin_sizes.append(len(basin))
    
    print("basin sizes:", basin_sizes)
    largest_three_basins = sorted(basin_sizes)[-3:]
    print("largest three basins:", largest_three_basins)
    print(np.multiply.reduce(largest_three_basins))

if __name__ == "__main__":
    main()
