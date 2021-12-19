import numpy as np

def main():
    data = np.loadtxt("input", dtype=str)
    directions = data[:, 0]
    movement = data[:, 1].astype(int)
    horizontal_position = 0
    depth = 0
    aim = 0
    for direction, movement in zip(directions, movement):
        if direction == "up":
            aim -= movement
        elif direction == "down":
            aim += movement
        elif direction == "forward":
            horizontal_position += movement
            depth += aim * movement
    print(depth, horizontal_position, depth * horizontal_position)

if __name__ == "__main__":
    main()
