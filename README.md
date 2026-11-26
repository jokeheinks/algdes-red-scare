# Red Scare

Solutions to the five Red Scare problems (`doc/red-scare.pdf`):
`alternate.py`, `few.py`, `many.py`, `none.py`, `some.py`.
The report (algorithms, correctness arguments and results) is in
`doc/report.pdf`.

| Problem | Method | Running time | Solved on |
|---|---|---|---|
| None | BFS that never expands red vertices other than `s` | `O(n + m)` | all graphs |
| Some | Max flow (Ford–Fulkerson) with vertex capacities, once per red vertex | `O(\|R\| · m)` | undirected graphs (`?!` on directed) |
| Many | Bellman–Ford with weight −1 on edges into red vertices | `O(nm)` | DAGs, undirected forests, undirected graphs with one red vertex, plus trivial cases |
| Few | 0-1 BFS with weight 1 on edges into red vertices | `O(n + m)` | all graphs |
| Alternate | Reachability along edges with exactly one red endpoint | `O(n + m)` | all graphs |

## Requirements

Python 3 with `networkx`, which `many.py` uses. The test script and the
table script also need `pandas`, and the table script needs `tqdm`:

```sh
pip install networkx pandas tqdm
```

## Recreating results.txt

From the repository root:

```sh
python run_all.py
```

This runs every solution on every graph in `data/` and writes:

- `results.txt`: tab-separated table with columns
  `Instance name, n, A, F, M, N, S` (Alternate, Few, Many, None, Some).
  `?!` means the problem is NP-hard and the instance is outside the graph
  class our algorithm solves.
- `timings.txt`: the same table with the running time of each program in seconds.

To regenerate the LaTeX table for the report (instances with n ≥ 500):

```sh
python utils/large_table.py     # writes results_table.tex
```

## Running a single instance

Each program reads one instance on standard input and prints the answer:

```sh
python few.py < data/G-ex.txt
```

## Tests

```sh
python utils/test.py            # check all solutions against utils/test.csv
python utils/make_expected.py   # regenerate expected answers (brute force)
```
