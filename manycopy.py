

"""
Many: maximum number of red vertices on a simple s-t path.

Polynomial special cases:
  - directed acyclic graphs,
  - undirected forests.

General graphs with at most 22 vertices are solved exactly by
visited-set memoisation.  Larger unsolved instances print '?'.
"""

import sys
from collections import deque
from functools import lru_cache


lines = iter(sys.stdin.buffer.read().splitlines())
first = next(lines).split()
n, m, r = map(int, first)
s, t = next(lines).split()
s = s.decode()
t = t.decode()

names = []
red = set()
for _ in range(n):
    parts = next(lines).split()
    name = parts[0].decode()
    names.append(name)
    if len(parts) > 1 and parts[1] == b"*":
        red.add(name)

index = {name: i for i, name in enumerate(names)}
adj = [set() for _ in range(n)]
out = [set() for _ in range(n)]
incoming = [0] * n
directed = False
undirected = False
for _ in range(m):
    u, arrow, v = next(lines).split()
    u = u.decode()
    v = v.decode()
    ui = index[u]
    vi = index[v]
    if arrow == b"->":
        directed = True
        adj[ui].add(vi)
        out[ui].add(vi)
        incoming[vi] += 1
    else:
        undirected = True
        adj[ui].add(vi)
        adj[vi].add(ui)


def dag_answer():
    indegree = incoming.copy()
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    topological = []
    while queue:
        u = queue.popleft()
        topological.append(u)
        for v in out[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(topological) != n:
        return None

    start = index[s]
    target = index[t]
    value = [-10**18] * n
    value[start] = int(names[start] in red)
    for u in topological:
        if value[u] == -10**18:
            continue
        for v in out[u]:
            candidate = value[u] + int(names[v] in red)
            if candidate > value[v]:
                value[v] = candidate
    return -1 if value[target] == -10**18 else value[target]


def is_directed_dag():
    indegree = incoming.copy()
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in out[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == n


def forest_answer():
    # A BFS run from s is enough because a unique path exists between
    # every pair of vertices in an undirected forest.
    start = index[s]
    target = index[t]
    parent = [-1] * n
    parent[start] = start
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if parent[v] == -1:
                parent[v] = u
                queue.append(v)
    if parent[target] == -1:
        return -1

    answer = 0
    u = target
    while True:
        answer += int(names[u] in red)
        if u == start:
            break
        u = parent[u]
    return answer


def is_undirected_forest():
    if directed or undirected:
        return False
    edge_count = sum(len(neighbors) for neighbors in adj) // 2
    seen = [False] * n

    def visit(start):
        seen[start] = True
        stack = [(start, -1)]
        while stack:
            u, parent = stack.pop()
            for v in adj[u]:
                if v == parent:
                    continue
                if seen[v]:
                    return False
                seen[v] = True
                stack.append((v, u))
        return True

    component_count = sum(not seen[u] and visit(u) for u in range(n))
    # For a simple undirected graph, a forest has |E| = |V| - components.
    return edge_count == n - component_count


def exact_answer():
    start = index[s]
    target = index[t]
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def search(u, visited):
        if u == target:
            return int(names[u] in red)

        best = -1
        for v in adj[u]:
            if visited & (1 << v):
                continue
            suffix = search(v, visited | (1 << v))
            if suffix != -1:
                candidate = int(names[u] in red) + suffix
                best = max(best, candidate)
        return best

    answer = search(start, (1 << start))
    return answer if answer != -1 else -1


if directed and not undirected:
    answer = dag_answer()
elif is_undirected_forest():
    answer = forest_answer()
elif n <= 22:
    answer = exact_answer()
else:
    answer = "?"

print(answer)

