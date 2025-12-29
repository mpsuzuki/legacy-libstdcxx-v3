#!/usr/bin/env python3
import sys
import subprocess

def load_reachable_from_file(path):
    reachable = set()
    with open(path, "r") as f:
        for line in f:
            h = line.strip()
            if h:
                reachable.add(h)
    return reachable

def load_reachable_from_git():
    reachable = set()
    result = subprocess.run(
        ["git", "rev-list", "--all"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    for line in result.stdout.splitlines():
        h = line.strip()
        if h:
            reachable.add(h)
    return reachable

def main():
    if len(sys.argv) == 2:
        reachable = load_reachable_from_file(sys.argv[1])
    elif len(sys.argv) == 1:
        reachable = load_reachable_from_git()
    else:
        print(f"Usage: {sys.argv[0]} [reachable.txt]", file=sys.stderr)
        sys.exit(1)

    for line in sys.stdin:
        line = line.rstrip("\n")

        if not line:
            continue

        parts = line.strip().split()

        if parts == ["old", "new"]:
            print(line)
            continue

        if len(parts) != 2:
            print(line)
            continue

        old, new = parts

        if new == "0000000000000000000000000000000000000000":
            continue

        if new not in reachable:
            continue

        print(line)

if __name__ == "__main__":
    main()
