#!/usr/bin/env python3

import numpy as np
import io
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)

    args, _ = parser.parse_known_args()
    day = args.day

    project_dir = "/Users/steven/Projects/advent-of-code-2021"
    python_template = os.path.join(project_dir, "template.py")

    if not os.path.exists(python_template):
        raise os.error(f"Python template {python_template} does not exist!")
    with open(python_template, "r") as f:
        template = f.read()

    dir = os.path.join(project_dir, f"day_{day}")

    if not os.path.exists(dir):
        print(f"creating directory {dir}")
        os.makedirs(dir)
    else:
        print(f"directory exists {dir}")
        
    input_files = ["input", "test_input"]    
    for fname in input_files:
        path = os.path.join(dir, fname)
        if not os.path.exists(path):
            print(f"creating file {path}")
            Path(path).touch()
        else:
            print(f"file exists {path}")

    python_files = [f"solution_{day * 2 - 1}.py", f"solution_{day * 2}.py"]
    for fname in python_files:
        path = os.path.join(dir, fname)
        if not os.path.exists(path):
            print(f"creating file {path} and populating with template")
            Path(path).touch()
            with open(path, "w") as f:
                f.write(template)
        else:
            print(f"file exists {path}")

if __name__ == "__main__":
    main()
