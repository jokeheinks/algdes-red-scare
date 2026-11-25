# Red Scare: Solutions and Test Cases

This file describes the solutions to the five Red Scare problems (see
`doc/red-scare.pdf`), the reasons behind each algorithm, and how the test
cases were built.

## Files

| File | Purpose |
|---|---|
| `none.py` | Problem **None** (unchanged) |
| `some.py` | Problem **Some** (rewritten) |
| `many.py` | Problem **Many** (new) |
| `few.py` | Problem **Few** (new) |
| `alternate.py` | Problem **Alternate** (unchanged) |
| `utils/graph.py` | Shared input parser and block-cut-tree helper used by `some.py` and `many.py` |
| `utils/brute_force.py` | Reference solver that tries every simple path (small graphs only) |
| `utils/make_expected.py` | Regenerates `utils/test.csv` with expected answers from the reference solver |
| `utils/test.py` | Runs every solution on every row of `utils/test.csv` |
| `run_all.py` | Runs every solution on every graph in `data/` and writes `results.txt` and `timings.txt` |
| `results.txt` | All answers, tab-separated, in the format from `doc/report.tex` |
| `timings.txt` | Running time in seconds of every program on every instance |
| `test-cases/<problem>/` | Handmade test graphs, grouped by the problem they mainly target |
| `alternate - test cases /` | Earlier handmade Alternate tests (kept in place) |

## How to run

Run everything from the repository root, because the scripts import `utils.graph`:

```sh
python few.py < data/G-ex.txt              # one problem on one graph
python run_all.py                          # all graphs in data/ -> results.txt (about 2 min)
python utils/test.py                       # all solutions against utils/test.csv
python utils/make_expected.py              # rebuild expected answers after adding tests
```

The scripts depend on `networkx`; the test runner also uses `pandas`.

A program prints `?` when the graph is outside the class it can solve in
polynomial time. The assignment explicitly allows this.

## Input conventions

- Graphs are stored as a `networkx.DiGraph`. An undirected edge `u -- v` is
  stored as both `u -> v` and `v -> u`.
- A graph counts as *directed* if its input file has at least one `->` edge.
  All directed graphs in `data/` (`increase-*`, `ski-*`) are acyclic; all
  others are undirected.
- If `s = t`, the only s,t-path is the single vertex `s` (length 0). It
  contains one red vertex if `s` is red and none otherwise.

---

## None: shortest path internally avoiding R

**Algorithm (`none.py`, unchanged):** BFS from `s`. A red vertex other than
`s` may be reached, which is how a red `t` is allowed, but the search never
expands out of it. As a result, red vertices can only be endpoints of the path.

**Why it is correct:** BFS on unweighted graphs finds shortest paths. Never
expanding red vertices is exactly the "no red internal vertex" condition. A
shortest walk never repeats a vertex, so it is a path. Time `O(n + m)`, exact
on all graphs.

## Few: minimum number of red vertices on an s,t-path

**Algorithm (`few.py`):** give each vertex weight 1 if red and 0 otherwise,
and find the path of minimum total vertex weight with 0-1 BFS. A step into a
non-red vertex goes to the front of a deque, a step into a red vertex to the
back. The answer is `red(s) + dist(t)`, or `-1` if `t` is unreachable.

**Why it is correct:** this is Dijkstra with weights in {0, 1}, which 0-1 BFS
handles in `O(n + m)`. Dijkstra may return a walk, but if a walk repeats a
vertex we can cut out the loop between the two visits. That never adds red
vertices, so the optimal walk gives an optimal simple path. Exact on all graphs.

## Some: is there an s,t-path through at least one red vertex?

**Why the old version was wrong:** it checked only whether a red vertex could
be reached from `s` or `t`. That accepts *walks*, such as going to a red
vertex and coming back the same way, which are not paths. This is exactly the
trap the `wall-z` and `wall-n` graphs are built to catch. It also combined the
two reachability sets with `|` instead of `&`, and never checked that `t` was
reachable at all. It failed 24 of the test cases.

**New algorithm (`some.py`):**

1. If `s = t`: the answer is whether `s` is red.
2. If `t` is not reachable from `s`: `False`.
3. If `s` or `t` is red: `True`, because any s,t-path works.
4. **Undirected graph:** split the graph into its 2-connected blocks and build
   the block-cut tree. Take the blocks on the tree path from `s` to `t`. The
   answer is `True` iff one of those blocks contains a red vertex.
5. **Directed acyclic graph:** `True` iff some red `r` has `s ->* r ->* t`.
6. **Directed graph with cycles:** if no red vertex lies between `s` and `t`
   by reachability, answer `False`. Otherwise print `?`.

**Why step 4 is correct:**

- Every simple s,t-path visits exactly the blocks on the block-cut-tree path
  between `s` and `t`, in order. It enters each block at one vertex `x` and
  leaves at another vertex `y` (a cut vertex, or `s`/`t` themselves). It
  cannot visit any other block, because that would require passing through a
  cut vertex twice.
- Inside a 2-connected block, for any two distinct vertices `x`, `y` and any
  third vertex `z`, there is an x,y-path through `z`. This follows from
  Menger's theorem: there are two vertex-disjoint paths from `z` to `{x, y}`.
- The paths chosen inside different blocks only share the cut vertices that
  join them, so they combine into one simple s,t-path.
- Hence a red vertex can be on some s,t-path iff it lies in one of those
  blocks.

Biconnected components take linear time, so this is `O(n + m)`.

**Why step 5 is correct:** in a DAG no walk can repeat a vertex, so the walk
`s ->* r ->* t` is already a path.

**Why directed graphs with cycles are not solved:** Some on general directed
graphs is NP-hard. Deciding whether there is a path `s -> r -> t` through a
given vertex `r` is closely related to the directed two-disjoint-paths
problem, which Fortune, Hopcroft and Wyllie showed is NP-complete. None of the
`data/` instances are in this case.

## Many: maximum number of red vertices on an s,t-path

**Hardness:** Many is NP-hard. Reduction from Hamiltonian path: colour every
vertex red. Then the answer is `n` exactly when there is a Hamiltonian s,t-path.
So we only solve well-defined special classes, as the assignment allows.

**Algorithm (`many.py`):**

1. If `s = t`: `1` if `s` is red, otherwise `0`. If `t` is unreachable: `-1`.
   If there are no red vertices: `0`.
2. **Directed acyclic graph:** longest-path DP in topological order:
   `best[v] = max over edges u -> v of best[u] + red(v)`, starting with
   `best[s] = red(s)`. Every walk in a DAG is a path, so the DP is exact.
   Time `O(n + m)`. This solves every `increase-*` and `ski-*` instance.
3. **Undirected graph where every block on the s,t block-cut-tree path is a
   single edge or a simple cycle** (trees, cacti, `wall-z-*`, `wall-n-*`):
   - The path must pass through these blocks in order, as argued for Some, so
     their entry and exit vertices are always on it.
   - In an edge block nothing else can be picked up.
   - In a cycle block the path goes from entry to exit along one of the two
     arcs, so it takes the arc with more red vertices.
   - The answer is the sum of these choices. Time `O(n + m)`.
4. **Anything else** (undirected graphs with richer blocks, directed graphs
   with cycles): print `?`.

## Alternate: is there an alternating s,t-path?

**Algorithm (`alternate.py`, unchanged):** delete every edge whose two
endpoints have the same colour, then check reachability from `s` to `t`.

**Why it is correct:** in the remaining graph every edge joins a red vertex
to a non-red one. Any walk there is alternating, and cutting a loop out of the
walk keeps it alternating, so a walk exists iff a path does. Time `O(n + m)`,
exact on all graphs.

---

## Test cases

### What was added

There are 44 small handmade graphs in `test-cases/`, plus the 19 earlier
Alternate tests in `alternate - test cases /`. Each graph targets a mistake
that is easy to make:

| Folder | What the tests check |
|---|---|
| `none/` | The s–t edge counts even when both ends are red; red `s`/`t` are allowed; the shortest route is blocked by red; a red vertex next to `t`; edge direction is respected; `s = t` gives `0`; disconnected graphs give `-1` |
| `some/` | Red vertices that can only be reached by a walk, not a path: a red dead end, a bowtie (two cycles sharing one vertex), a small `wall-z` brick, a directed cycle. Also: red only reachable against the edge direction, red `s` or `t`, no red at all, `s = t` |
| `many/` | A longer path with more red beats a shorter one; `s`/`t` count toward the total; red that is only collectable by repeating a vertex (answer `0`); no path gives `-1`; an all-red cycle; a DAG |
| `few/` | A longer path with fewer red beats a shorter one; red that cannot be avoided; red endpoints; no path gives `-1`; `s = t` |
| `alternate/` | The s–t edge as an alternating path; a blocking same-colour edge; edge direction is respected; a longer alternating cycle |

### How the expected answers were obtained

Working out answers by hand is error-prone, so `utils/brute_force.py`
enumerates **every simple s,t-path** and reads off all five answers directly
from the definitions in the PDF. Because it follows the definitions word for
word, it is a trustworthy reference, but it takes exponential time.

It reproduces the PDF's answers for `G-ex` (3 / True / 2 / 0 / True).

`utils/make_expected.py` runs it on all handmade tests plus every graph in
`data/` with at most 50 vertices, and writes the results to `utils/test.csv`.
That gives 111 rows, each with expected answers for all five problems. Every
row is therefore a test for every problem, not only the one its folder is named
after.

### Results

On the 111 rows of `utils/test.csv`:

| Problem | Correct | `?` | Wrong |
|---|---|---|---|
| None | 111 | 0 | 0 |
| Some | 109 | 2 (directed graphs with cycles) | 0 |
| Many | 92 | 19 (outside the solvable classes) | 0 |
| Few | 111 | 0 | 0 |
| Alternate | 111 | 0 | 0 |

`utils/test.py` reports a `?` as `FAILED`, because it compares raw output with
the expected value.

All 154 graphs in `data/` finish, including the 5757-vertex word graphs.

- **Some:** answers every `data/` instance. It agrees with the PDF on all
  wall graphs up to 10,000 bricks: `wall-p` is True, and `wall-z` and `wall-n`
  are False, except the single-brick ones, where `s`, `t` and the red vertex
  share one cycle.
- **Many:** answers 65 of the 154 `data/` instances and prints `?` on the other 89.
- **Few:** answers every `data/` instance.

## Results on `data/` (`results.txt`)

`python run_all.py` runs every program on all 154 graphs in `data/` in about
1.5 minutes in total. The slowest single run is about 1.3 s (on
`common-2-5757`). It writes `results.txt` in the format required by
`doc/report.tex`: columns `Instance name, n, A, F, M, N, S`, booleans as
`true`/`false`, and `?!` where the problem is NP-hard and the graph is outside
our solvable class.

| Problem | Instances answered | `?!` |
|---|---|---|
| Alternate | 154 | 0 |
| Few | 154 | 0 |
| Many | 65 | 89 |
| None | 154 | 0 |
| Some | 154 | 0 |

**How the results were checked:**

- On the 48 instances with at most 50 vertices, every answer in `results.txt`
  equals the brute-force answer.
- On all 154 rows, the answers are consistent with each other:
  - Few and Many agree on whether an s,t-path exists.
  - Few ≤ Many.
  - Few ≥ 1 implies Some is true.
  - Where Many is known, Many ≥ 1 exactly when Some is true.
  - If no path exists, None, Some and Alternate also say so.

Many is answered on all `increase-*` and `ski-*` graphs (DAGs), all `wall-z-*`
and `wall-n-*` graphs (cacti), and every graph where `t` is unreachable from
`s` or there are no red vertices. The 89 `?!` entries are undirected graphs
with richer 2-connected structure (`grid`, `gnm`, `smallworld`, `rusty`,
`wall-p`, most `common`, `bht`, `G-ex`, `dodecahedron`).

### Adding a test

1. Put a graph in the usual input format into `test-cases/<problem>/`.
2. Run `python utils/make_expected.py`. Keep the graph small, since the
   reference solver tries every path.
3. Run `python utils/test.py`.
