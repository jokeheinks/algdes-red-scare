
"""
Many Return the maximum number of red vertices on any path from
s to t. To be precise, let P be the set of s, t-paths and let r(p) denote
the number of red vertices on a path p. Return max{ r(p): p ∈ P }.
If no path from s to t exists, return ‘-1’. In Gex, the answer is ‘2’
(because of the path 0, 5, 6, 7, 3.)
"""
# for this problemn I will be uhsing bellman_ford_path method from networkx library to find the path from s to t and then count the number of red vertices in that path.

import networkx as nx

n, m, r = [int(x) for x in input().split()]
s, t = input().split()
vertices= []
R = set()
G = nx.DiGraph()






for i in range(n): # check and read the vertices and their colors
    parts = input().split()
    vertex = parts[0]
    if len(parts) == 2:
        vertices.append(vertex)
        R.add(vertex)
        G.add_node(vertex)
#        print(f"Vertex {vertex} is red")
    else:
        vertices.append(vertex)
        G.add_node(vertex)
#        print(f"Vertex {vertex} is not red")

#if there are no vertices, then we cannot find a path from s to t

if n == 0 : 
    print("?")
    exit()

for i in range(m): # check and read the edges

    edge = input().strip()
    # check if a graph is directed or not by checking if the edge is in the form of u--v or u->v
    if "--" in edge:
#        print("graph is undirected, giving up")
        print("?")
        exit()
    if "->" in edge:
        u, v = edge.split("->")

        #check if the destination vertex is red
        if v.strip() in R:
            G.add_edge(u.strip(), v.strip(), weight=-1) # all weights as -1
        else:
            G.add_edge(u.strip(), v.strip(), weight=0) # all weights as 0 

# if there are no edges, then t is unreachable from s, so we return -1



# now let's see if the reading was successful
"""
print(f"n: {n}, m: {m}, r: {r}")
print(f"s: {s}, t: {t}")
print(f"vertices: {vertices}")
print(f"R: {R}")
"""
# the reading is indeed successfull and very correct

# now we move onto the algorithm implementation part. W
# we will be using bellfam's ford alg here.

# First we need to check if the graph is direct and acyclic
if nx.is_directed_acyclic_graph(G) == False:
    print("?")
    exit()

else:
#    print("Graph is directed and acyclic, proceeding with Bellman-Ford algorithm")
#    print(f"Finding path from {s} to {t} using Bellman-Ford algorithm")
    try:
        final_list = nx.bellman_ford_path(G, source=s, target=t)
    except:
        print("-1")
        exit()
#    print(f"Path from {s} to {t} is: {final_list}")

# print the total unmber of red vertices in the path from s to t
red_count = 0
for vertex in final_list:
    if vertex in R:
        red_count += 1
print(red_count)
