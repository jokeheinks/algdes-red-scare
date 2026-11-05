import networkx as nx

n, m, r = [int(x) for x in input().split()]
s, t = input().split()
vertices = []
R = set()

for _ in range(n):
    v = input().split()
    vertices.append(v[0])
    if v[-1] == "*":
        R.add(v[0])

G = {n: set() for n in vertices}
G_inv = {n: set() for n in vertices}

for _ in range(m):
    u, direction, v = input().split()
    if direction == "->":
        G[u].add(v)
        G_inv[v].add(u)
    else:
        G[u].add(v)
        G[v].add(u)
        G_inv[u].add(v)
        G_inv[v].add(u)


def bfs(G, start, R) -> set:
    frontier = {start}
    visited = set()
    reach = set()

    while frontier:
        curr = frontier.pop()
        if curr in R:
            reach.add(curr)
        if curr in visited:
            continue
        visited.add(curr)
        frontier.update(G[curr])

    return reach


def some(G: dict, R: set, start: str, target: str) -> bool:
    if not R:
        return False

    s_reach = bfs(G, start, R)
    t_reach = bfs(G_inv, target, R)

    return bool(s_reach | t_reach)


print(some(G, R, s, t))
