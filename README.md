# Red Scare

Solutions to the five Red Scare problems (`doc/red-scare.pdf`):
`alternate.py`, `few.py`, `many.py`, `none.py`, `some.py`.
See `SOLUTIONS.md` for the algorithms and why they are correct.

## Requirements

Python 3 with `networkx` (and `pandas` for the test runner):

```sh
pip install networkx pandas
```

## Recreating results.txt

From the repository root:

```sh
python run_all.py
```

This runs every solution on every graph in `data/` (about 2 minutes) and writes:

- `results.txt`: tab-separated table with columns
  `Instance name, n, A, F, M, N, S` (Alternate, Few, Many, None, Some).
  `?!` means the problem is NP-hard and the instance is outside the graph
  class our algorithm solves.
- `timings.txt`: the same table with the running time of each program in seconds.

## Running a single instance

Each program reads one instance on standard input and prints the answer:

```sh
python few.py < data/G-ex.txt
```

Run the programs from the repository root, because they import `utils/graph.py`.

## Tests

```sh
python utils/test.py            # check all solutions against utils/test.csv
python utils/make_expected.py   # regenerate expected answers (brute force)
```
