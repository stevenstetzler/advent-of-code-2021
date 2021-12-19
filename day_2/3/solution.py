import numpy as np

def main():
    data = np.loadtxt("input", dtype=str)
    directions = data[:, 0]
    movement = data[:, 1].astype(int)
    depth = movement[directions == "down"].sum() - movement[directions == "up"].sum()
    horizontal_position = movement[directions == "forward"].sum()
    print(depth, horizontal_position, depth * horizontal_position)

if __name__ == "__main__":
    main()
