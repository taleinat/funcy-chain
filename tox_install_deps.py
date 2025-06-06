#!/usr/bin/env python
import subprocess
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--no-deps" in args:
        subprocess.run(["flit", "install", "--deps", "none"], check=True)
    else:
        subprocess.run(
            ["pip", "install", "--disable-pip-version-check", "--no-python-version-warning"] + args,
            check=True,
        )
        subprocess.run(["flit", "install", "--extras", "test"], check=True)
