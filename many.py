"""Many: maximum number of red vertices on any s,t-path.

NP-hard in general (with all vertices red it is the longest path problem),
so we solve it exactly on two well-defined graph classes and print '?'
otherwise:

- Directed acyclic graphs: longest-path DP in topological order, O(n + m).
- Undirected graphs whose blocks on the s,t-path of the block-cut tree are
  all single edges or simple cycles (e.g. trees, cacti): the path is forced
  through each block, and in a cycle it takes whichever of the two arcs
  holds more red vertices.
"""
import networkx as nx

from utils.graph import block_path, read_graph


def many_dag(G, R, s, t):
    best = {s: int(s in R)}
    for u in nx.topological_sort(G):
        if u not in best:
            continue
        for v in G[u]:
            best[v] = max(best.get(v, -1), best[u] + int(v in R))
    return best.get(t, -1)


def cycle_arcs(nodes, edges, x, y):
    """Internal vertices of the two x,y-arcs of a cycle block."""
    adj = {v: [] for v in nodes}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    arcs = []
    for first in adj[x]:
        arc, prev, cur = [], x, first
        while cur != y:
            arc.append(cur)
            prev, cur = cur, next(v for v in adj[cur] if v != prev)
        arcs.append(arc)
    return arcs


def many_undirected(G, R, s, t):
    U = G.to_undirected()
    total = int(s in R)
    for nodes, edges, x, y in block_path(U, s, t):
        total += int(y in R)
        if len(edges) == 1:
            continue
        if len(edges) != len(nodes):  # not a simple cycle
            return "?"
        total += max(sum(v in R for v in arc) for arc in cycle_arcs(nodes, edges, x, y))
    return total


def many(G, R, s, t, directed):
    if s == t:
        return int(s in R)
    if not nx.has_path(G, s, t):
        return -1
    if not R:
        return 0
    if not directed:
        return many_undirected(G, R, s, t)
    if nx.is_directed_acyclic_graph(G):
        return many_dag(G, R, s, t)
    return "?"


if __name__ == "__main__":
    G, R, s, t, directed = read_graph()
    print(many(G, R, s, t, directed))
