import numpy as np
import io
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args, _ = parser.parse_known_args()
    test = args.test

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
    print(rays)
    xmin = min((rays[:, 0].min(), rays[:, 2].min()))
    xmax = max((rays[:, 0].max(), rays[:, 2].max()))
    ymin = min((rays[:, 1].min(), rays[:, 3].min()))
    ymax = max((rays[:, 1].max(), rays[:, 3].max()))
    print(xmin, xmax, ymin, ymax)

    vent_map = np.zeros((ymax + 1, xmax + 1), dtype=int)

    for ray in rays:
        x1 = ray[0]
        y1 = ray[1]
        x2 = ray[2]
        y2 = ray[3]
        # horizontal
        if x1 == x2:
            if y2 < y1:
                idx_y1 = y2
                idx_y2 = y1
            else:
                idx_y1 = y1
                idx_y2 = y2
            idx_y2 += 1
            # print("ray", ray, "is horiztonal adding 1 to", slice(idx_y1, idx_y2), slice(x1))
            vent_map[idx_y1:idx_y2, x1] += 1
        # vertical
        elif y1 == y2:
            if x2 < x1:
                idx_x1 = x2
                idx_x2 = x1
            else:
                idx_x1 = x1
                idx_x2 = x2
            idx_x2 += 1
            # print("ray", ray, "is vertical adding 1 to", slice(y1), slice(idx_x1, idx_x2))
            vent_map[y1, idx_x1:idx_x2] += 1
        # diagonal
        else:
            pass

    for row in vent_map:
        for col in row:
            if col == 0:
                print(".", end="")
            else:
                print(col, end="")
        print("\n", end="")

    # print(vent_map.astype("str"))
    print((vent_map > 1).sum())

if __name__ == "__main__":
    main()
