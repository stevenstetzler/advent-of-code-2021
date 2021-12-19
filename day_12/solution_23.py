import numpy as np
import io
import argparse

def is_small_cave(cave):
    return cave.lower() == cave

def is_big_cave(cave):
    return cave.upper() == cave

def traverse(start, target, cave_paths, visited):
    # print(f"traversing from {start}")
    # copy visited and paths
    # cave_paths = dict(cave_paths)
    visited = dict(visited)

    visited[start] = True
    if start == "end":
        return [["end"]]

    paths = []
    for cave in cave_paths[start]:
        if (not visited[cave]) or (visited[cave] and is_big_cave(cave)):
            # print(f"Starting new path from {start} to {cave}")
            paths_to_end = traverse(cave, target, cave_paths, visited)
            for path in paths_to_end:
                # print(path)
                paths.append([start] + path)
        else:
        # elif visited[cave]:
            # print(f"Cave {cave} already visited, ignoring in path determination")
            continue
        # elif cave == "end":
        #     print(f"Reached end of from {start}")
        #     paths.append([start, "end"])

    # print(f"Found path to end: {paths}")
    return paths
            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--test-num", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    test_num = args.test_num
    verbose = args.verbose

    if test:
        infile = f"test_input_{test_num}"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    cave_paths = {}
    for line in lines:
        start = line.split("-")[0]
        end = line.split("-")[1]
        if cave_paths.get(start, None):
            cave_paths[start].append(end)
        else:
            cave_paths[start] = [end]

        if cave_paths.get(end, None):
            cave_paths[end].append(start)
        else:
            cave_paths[end] = [start]

    visited = {
        key : False
        for key in cave_paths.keys()
    }
    paths = traverse("start", "end", cave_paths, visited)
    if verbose:
        for path in paths:
            print(",".join(path))
    print(f"There are {len(paths)} paths through the cave")

if __name__ == "__main__":
    main()
