"""Some: is there an s,t-path through at least one red vertex?

- Undirected graphs (exact, linear time): every simple s,t-path passes
  through exactly the 2-connected blocks on the s,t-path of the block-cut
  tree. Inside a 2-connected block, for any entry x, exit y != x and any
  third vertex z there is an x,y-path through z (Menger). So the answer is
  True iff some red vertex lies in one of those blocks.
- Directed acyclic graphs (exact): every walk is a path, so the answer is
  True iff some red r has s ->* r ->* t.
- Directed graphs with cycles: NP-hard in general. We answer whatever can be
  decided by reachability and print '?' otherwise.
"""
import networkx as nx

from utils.graph import block_path, read_graph


def some(G, R, s, t, directed):
    if s == t:
        return s in R
    if not nx.has_path(G, s, t):
        return False
    if s in R or t in R:
        return True

    if not directed:
        U = G.to_undirected()
        return any(nodes & R for nodes, _, _, _ in block_path(U, s, t))

    via = nx.descendants(G, s) & nx.ancestors(G, t) & R
    if not via:
        return False
    if nx.is_directed_acyclic_graph(G):
        return True
    return "?"


if __name__ == "__main__":
    G, R, s, t, directed = read_graph()
    print(some(G, R, s, t, directed))
