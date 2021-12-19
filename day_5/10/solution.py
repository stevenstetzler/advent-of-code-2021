import numpy as np
import io
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--no-diagonals", action="store_true")
    parser.add_argument("--diagram", action="store_true")
    args, _ = parser.parse_known_args()
    test = args.test
    no_diagonals = args.no_diagonals
    diagram = args.diagram

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    
    rays = []
    for line in lines:
        points = line.split("->")
        points = [point.strip() for point in points]
        ray_start = points[0].split(",")
        ray_start = [int(coord.strip()) for coord in ray_start]
        ray_end = points[1].split(",")
        ray_end = [int(coord.strip()) for coord in ray_end]
        rays.append(ray_start + ray_end)
    
    rays = np.array(rays)
    xmin = min((rays[:, 0].min(), rays[:, 2].min()))
    xmax = max((rays[:, 0].max(), rays[:, 2].max()))
    ymin = min((rays[:, 1].min(), rays[:, 3].min()))
    ymax = max((rays[:, 1].max(), rays[:, 3].max()))

    vent_map = np.zeros((ymax + 1, xmax + 1), dtype=int)

    for ray in rays:
        x1 = ray[0]
        y1 = ray[1]
        x2 = ray[2]
        y2 = ray[3]

        if y2 > y1:
            yrange = range(y1, y2 + 1, 1)
        elif y2 < y1:
            yrange = range(y1, y2 - 1, -1)
        else:
            yrange = None
        
        if x2 > x1:
            xrange = range(x1, x2 + 1, 1)
        elif x2 < x1:
            xrange = range(x1, x2 - 1, -1)
        else:
            xrange = None

        # vertical
        if x1 == x2:
            for y in yrange:
                vent_map[y, x1] += 1
        # horizontal
        elif y1 == y2:
            for x in xrange:
                vent_map[y1, x] += 1
        # diagonal
        else:
            if no_diagonals:
                continue
            for x, y in zip(xrange, yrange):
                vent_map[y, x] += 1

    if diagram:
        for row in vent_map:
            for col in row:
                if col == 0:
                    print(".", end="")
                else:
                    print(col, end="")
            print("\n", end="")

    print((vent_map > 1).sum())

if __name__ == "__main__":
    main()
