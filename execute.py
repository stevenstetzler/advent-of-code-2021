#!/usr/bin/env python3

import numpy as np
import io
import argparse
import os
import sys
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("--problem", type=int, default="-1")
    parser.add_argument("--extra", nargs="+")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    day = args.day
    test = args.test
    verbose = args.verbose
    extra = args.extra
    problem = args.problem

    project_dir = "/Users/steven/Projects/advent-of-code-2021"

    dir = os.path.join(project_dir, f"day_{day}")
    to_execute = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "__pycache__" in root:
                continue
            if ".py" in file:
                to_execute.append(os.path.join(root, file))
    
    to_execute = sorted(to_execute, key=lambda x : os.path.dirname(x))
    to_execute = sorted(to_execute, key=lambda x : os.path.basename(x))
    if problem == 1:
        to_execute = to_execute[0:1]
    elif problem == 2:
        to_execute = to_execute[1:2]

    for file in to_execute:
        cmd = ["python3", os.path.basename(file)]
        if test:
            cmd += ["--test"]
        if verbose:
            cmd += ["--verbose"]
        if extra:
            for arg in extra:
                if "=" in arg:
                    cmd += [f"--{arg}"]
                else:
                    cmd += [arg]
        cwd = os.path.dirname(file)
        print(f"# executing '{' '.join(cmd)}' in {cwd}", file=sys.stderr)
        subprocess.call(cmd, cwd=cwd)
        print("", file=sys.stderr)

if __name__ == "__main__":
    main()
