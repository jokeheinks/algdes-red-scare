"""Shared input parsing and graph helpers for the Red Scare solutions."""
import sys

import networkx as nx


def read_graph(stream=sys.stdin):
    """Parse a Red Scare instance.

    Returns (G, R, s, t, directed) where G is an nx.DiGraph (every undirected
    edge is stored in both directions) and `directed` tells whether the input
    contained any '->' edge.
    """
    lines = iter(l for l in stream.read().split("\n") if l.strip())
    n, m, _ = (int(x) for x in next(lines).split())
    s, t = next(lines).split()
    G = nx.DiGraph()
    R = set()
    for _ in range(n):
        v = next(lines).split()
        G.add_node(v[0])
        if v[-1] == "*":
            R.add(v[0])
    directed = False
    for _ in range(m):
        u, d, v = next(lines).split()
        G.add_edge(u, v)
        if d == "--":
            G.add_edge(v, u)
        else:
            directed = True
    return G, R, s, t, directed


def block_path(U, s, t):
    """For an undirected graph U and connected vertices s != t, return the
    2-connected blocks on the s,t-path of the block-cut tree, as a list of
    (block_vertices, block_edges, entry, exit) tuples.

    Every simple s,t-path visits exactly these blocks, in this order, entering
    each block at `entry` and leaving at `exit`.
    """
    blocks = list(nx.biconnected_component_edges(U))
    block_nodes = [set(x for e in edges for x in e) for edges in blocks]
    cut = set(nx.articulation_points(U))

    T = nx.Graph()
    for i, nodes in enumerate(block_nodes):
        for v in nodes & cut:
            T.add_edge(("B", i), ("C", v))

    def tree_node(v):
        if v in cut:
            return ("C", v)
        return ("B", next(i for i, b in enumerate(block_nodes) if v in b))

    a, b = tree_node(s), tree_node(t)
    path = [a] if a == b else nx.shortest_path(T, a, b)

    result = []
    entry = s
    for k, (kind, x) in enumerate(path):
        if kind == "C":
            entry = x
            continue
        exit_ = path[k + 1][1] if k + 1 < len(path) else t
        result.append((block_nodes[x], blocks[x], entry, exit_))
    return result
