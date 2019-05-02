import numpy
import networkx as nx

# The Road Network Model is an undirected weighted planar graph
# G = (V,E)
# V is a set of road junctions, E is a set of road segments

# Given a list of edges, returns the one with the lowest weight
def get_lowest_weight(graph, list_of_edges):
    dict = {}
    set = {}
    for edge in list_of_edges:
        dict[edge] = graph.get_edge_data(edge)['weight']
    for value in dict.items():
        set.add(value)
    min_weight = min(set)
    return dict.get(min_weight)

# Returns a sequence of edges that connect src to dest,
#    where the cumulative weight is minimized
# src and dest are vertices in the graph
def shortest_path(graph, src, dest):
    path = {}
    if src not in graph or dest not in graph:
        raise TypeError('Invalid input')
    if src == dest:
        return path
    # Create a set of all nodes in the graph
    all_nodes = set(graph.V)
    # n is the number of nodes in the graph
    n = graph.number_of_nodes()
    current_node = src
    cumulative_weight = 0
    # Visit the neighbors of the current node
    while (current != dest):
        neighbors = graph.neighbors(current)
        current = get_lowest_weight(graph, neighbors)
        path.add(current)
    return path

# Uses the NetworkX built-in function
def shortest_path_nx(graph, src, dest):
    return nx.dijkstra_path(graph, src, dest)

# creates a n X n matrix
# stores the shortest path from each node to every other node
def create_matrix(graph):
    n = len(graph.V)
    matrix = numpy.zeros((n,n))
    for i in range(n):
        for j in range(n):
            path = shortest_path(graph, i, j)
            matrix[i][j] = path
    return matrix

