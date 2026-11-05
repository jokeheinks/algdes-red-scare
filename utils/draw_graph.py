import networkx as nx
import matplotlib.pyplot as plt

n, m, r = [int(x) for x in input().split()]
s, t = input().split()
vertices = []
R = []

for _ in range(n):
    v = input().split()
    vertices.append(v[0])
    if v[-1] == "*":
        R.append(v[0])

edges = []
directed_edges = []
for _ in range(m):
    edge_text = input()
    if edge_text.find("->") != -1:
        directed_edges.append(edge_text.split("->"))
    else:
        edges.append(edge_text.split("--"))

G = nx.Graph()

if directed_edges:
    assert not edges  # Mixed edgetypes not implemented
    G = nx.DiGraph()

G.add_nodes_from(vertices)
G.add_edges_from(edges)

color_map = []
for node in G:
    if node in R:
        color_map.append("red")
    else:
        color_map.append("lightblue")

pos = nx.spring_layout(G)

nx.draw(G, with_labels=True, node_color=color_map, pos=pos)

labeled_points = {s: "Start", t: "Target"}
for point, label in labeled_points.items():
    x, y = pos[point]
    plt.text(
        x,
        y + 0.1,
        s=label,
        bbox=dict(facecolor="None", alpha=0.5),
        horizontalalignment="center",
    )

plt.show()
