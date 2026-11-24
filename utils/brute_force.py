"""Brute-force reference solver for all five Red Scare problems.

Enumerates every simple s,t-path, so it is exponential and only meant for
small graphs (it is used to compute the expected answers in utils/test.csv).

Usage: python utils/brute_force.py < graph.txt
Prints one line: none some many few alternate
"""
import sys


def parse(stream):
    tokens = stream.read().split("\n")
    lines = iter(l for l in tokens if l.strip())
    n, m, _ = (int(x) for x in next(lines).split())
    s, t = next(lines).split()
    R = set()
    G = {}
    for _ in range(n):
        v = next(lines).split()
        G[v[0]] = []
        if v[-1] == "*":
            R.add(v[0])
    for _ in range(m):
        u, d, v = next(lines).split()
        G[u].append(v)
        if d == "--":
            G[v].append(u)
    return G, R, s, t


def solve(G, R, s, t):
    best_none = -1
    some = False
    many = -1
    few = -1
    alternate = False

    path = [s]
    on_path = {s}

    def record():
        nonlocal best_none, some, many, few, alternate
        reds = sum(v in R for v in path)
        length = len(path) - 1
        if all(v not in R for v in path[1:-1]):
            if best_none == -1 or length < best_none:
                best_none = length
        some = some or reds > 0
        many = max(many, reds)
        few = reds if few == -1 else min(few, reds)
        if all((a in R) != (b in R) for a, b in zip(path, path[1:])):
            alternate = True

    def dfs(u):
        if u == t:
            record()
            return
        for v in G[u]:
            if v not in on_path:
                on_path.add(v)
                path.append(v)
                dfs(v)
                path.pop()
                on_path.remove(v)

    sys.setrecursionlimit(100000)
    dfs(s)
    return best_none, some, many, few, alternate


if __name__ == "__main__":
    print(*solve(*parse(sys.stdin)))
