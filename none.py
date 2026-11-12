n, m, r = [int(x) for x in input().split()]
s, t = input().split()
vertices = []
R = set()

# Parse input to graph(Adjacency dict)
for _ in range(n):
    v = input().split()
    vertices.append(v[0])
    if v[-1] == "*":
        R.add(v[0])

G = {n: set() for n in vertices}

for _ in range(m):
    u, direction, v = input().split()
    G[u].add(v)
    if direction == "--":
        G[v].add(u)


def bfs(G: dict, start: str, target: str, R: set) -> int:
    next_frontier = [start]
    visited = set()
    steps = -1

    while next_frontier:
        frontier = next_frontier
        next_frontier = []
        steps += 1
        for curr in frontier:
            if curr == target:
                return steps
            if curr in visited:
                continue
            if (curr in R) and (curr != start):
                continue

            visited.add(curr)
            next_frontier.extend(G[curr])
    return -1


print(bfs(G, s, t, R))
