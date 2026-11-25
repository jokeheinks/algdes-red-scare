from collections import defaultdict


class Max_Flow:
    def __init__(self, START, TARGET, G) -> None:
        self.start = START
        self.target = TARGET
        self.G = G

    def augmenting_path(self) -> tuple | int:
        frontier = {self.start}
        path = dict()
        success = False

        while frontier:
            node = frontier.pop()
            for out in self.G[node]:
                if out not in path and self.G[node][out] > 0:
                    frontier.add(out)
                    path[out] = (node, self.G[node][out])
                    if out == self.target:
                        success = True
                        break

        if not success:
            return -1
        else:
            n = self.target
            flow = float("inf")
            res = []
            while n != self.start:
                res.append(n)
                flow = min([flow, path[n][1]])
                n = path[n][0]
            res.append(self.start)
            return flow, res[::-1]

    def max_flow(self) -> int:
        max_flow = 0
        while True:
            augment = self.augmenting_path()
            if augment == -1:
                return max_flow

            flow, path = augment
            max_flow += flow
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.G[u][v] -= flow
                self.G[v][u] += flow


n, m, r = [int(x) for x in input().split()]
s, t = input().split()
vertices = []
R = set()

G = defaultdict(lambda: defaultdict(float))
START = "$START"
TARGET = "$TARGET"

G[s + ".out"][TARGET] = 1
G[t + ".out"][TARGET] = 1

for _ in range(n):
    v = input().split()
    vertices.append(v[0])
    G[v[0] + ".in"][v[0] + ".out"] = 1
    if v[-1] == "*":
        R.add(v[0])

# G = {n: set() for n in vertices}
directed = False
for _ in range(m):
    u, direction, v = input().split()
    if direction == "--":
        G[u + ".out"][v + ".in"] = float("inf")
        G[v + ".out"][u + ".in"] = float("inf")
    else:
        directed = True
        print("?!")
        exit()

solved = False
for v in R:
    G_c = defaultdict(lambda: defaultdict(float))
    for d in G:
        G_c[d] = G[d].copy()
    G_c[START][v + ".out"] = 2
    flow = Max_Flow(START, TARGET, G_c)
    if flow.max_flow() == 2:
        solved = True
        break

print(solved)
