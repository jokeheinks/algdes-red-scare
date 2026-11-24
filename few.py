"""Few: minimum number of red vertices on any s,t-path.

Every red vertex costs 1, so this is a shortest-path problem with vertex
weights 0/1, solved by 0-1 BFS in O(n + m). A cheapest walk can always be
shortcut to a simple path without picking up more red vertices, so the
answer is exact on every graph.
"""
from collections import deque

from utils.graph import read_graph


def few(G, R, s, t) -> int:
    def w(v):
        return 1 if v in R else 0

    dist = {s: w(s)}
    queue = deque([s])
    done = set()
    while queue:
        u = queue.popleft()
        if u in done:
            continue
        done.add(u)
        if u == t:
            return dist[u]
        for v in G[u]:
            d = dist[u] + w(v)
            if v not in dist or d < dist[v]:
                dist[v] = d
                if w(v):
                    queue.append(v)
                else:
                    queue.appendleft(v)
    return -1


if __name__ == "__main__":
    G, R, s, t, _ = read_graph()
    print(few(G, R, s, t))
