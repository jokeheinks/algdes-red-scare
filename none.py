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

for _ in range(m):
    u, direction, v = input().split()
    if direction == "->":
        G[u].add(v)
    else:
        G[u].add(v)
        G[v].add(u)


def none(G, start, target, R) -> bool:
    frontier = {start}
    visited = set()

    while frontier:
        curr = frontier.pop()
        if curr == target:
            return True
        if curr in R or curr in visited:
            continue
        visited.add(curr)
        frontier.update(G[curr])
    return False


print(none(G, s, t, R))
