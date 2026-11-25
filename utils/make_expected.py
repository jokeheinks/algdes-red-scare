"""Regenerate utils/test.csv with expected answers from the brute-force solver.

Includes every handmade test case plus the instances in data/ with at most
MAX_N vertices (larger ones are too slow to brute-force).

Usage (from the repo root): python utils/make_expected.py
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from brute_force import parse, solve  # noqa: E402

MAX_N = 50

files = sorted(glob.glob("test-cases/*/*.txt"))
files += sorted(glob.glob("alternate - test cases /*.txt"))
small_data = []
for f in glob.glob("data/*.txt"):
    with open(f) as fh:
        n = int(fh.readline().split()[0])
    if n <= MAX_N:
        small_data.append((n, f))
files += [f for _, f in sorted(small_data)]

with open("utils/test.csv", "w", newline="") as out:
    w = csv.writer(out)
    w.writerow(["data", "none", "some", "few", "many", "alternate"])
    for f in files:
        with open(f) as fh:
            none, some, many, few, alt = solve(*parse(fh))
        w.writerow([f, none, some, few, many, alt])
        print(f, none, some, few, many, alt)
