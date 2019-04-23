import networkx as nx

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 5), (3, 6), (3, 7), (4, 6), (5, 7), (5, 9), (6, 8), (7, 9)])

print(list(G.edges))
