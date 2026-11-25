from collections import deque

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


def few(G, start, target, R) -> int:
    INF = float("inf")
    dist = {v: INF for v in G}
    dist[start] = 1 if start in R else 0
    dq = deque([start])

    while dq:
        curr = dq.popleft()
        for nxt in G[curr]:
            w = 1 if nxt in R else 0
            if dist[curr] + w < dist[nxt]:
                dist[nxt] = dist[curr] + w
                if w == 0:
                    dq.appendleft(nxt)
                else:
                    dq.append(nxt)

    return -1 if dist[target] == INF else dist[target]


print(few(G, s, t, R))