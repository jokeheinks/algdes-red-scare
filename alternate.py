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


def alternate(G, start, target, R) -> bool:
    frontier = {start}
    visited = set()

    while frontier:
        curr = frontier.pop()
        if curr == target:
            return True
        if curr in visited:
            continue
        visited.add(curr)

        curr_is_red = curr in R
        frontier.update([n for n in G[curr] if (n in R) != curr_is_red])
    return False


print(alternate(G, s, t, R))
