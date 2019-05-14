import networkx as nx

#Separates input graph into two subgraphs, starting with the two nodes with the greatest shortest path between them, and collects the nodes they share

#Requires a 3-d shortest path matrix (matrix[start][end][distance]) and the original graph G


G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 5), (3, 6), (3, 7), (4, 6), (5, 7), (5, 9), (6, 8), (7, 9)])

shared = []
matrix = []
l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for x in range(1, 10):
    matrix.append([[], [], [], [], [], [], [], [], []])


#Creates two graphs starting with the nodes farthest from each other in the inital graph. Populates them using the next_node() function 
def subgraph_generation():
    G1 = nx.Graph()
    G2 = nx.Graph()

    max_distance = 0;
    start_points = []
    for i in range (0, 9):
        for j in range (0, 9):
            if max_distance < matrix[i][j][0]:
                max_distance = matrix[i][j][0]
                start_points = [i+1, j+1]

    n1 = start_points[0]
    n2 = start_points[1]

    G.remove_nodes_from(start_points)
    G1.add_node(n1)
    G2.add_node(n2)
    

    while len(G)>=1:
        next_node(G1, G2, list(G1.nodes), list(G2.nodes))


    print("G1 nodes: " + str(list(G1.nodes)))
    print("G2 nodes: " + str(list(G2.nodes)))
    print("Shared nodes: " + str(shared))

    
    
#finds and adds the next nodes to G1 and G2, and if they are the same node, adds it to the shared list
def next_node(g1, g2, node_list1, node_list2):
    new1 = None
    dist1 = None
    for i in range(0, 9):
        for j in node_list1:
            if (dist1 > matrix[j-1][i][0] or dist1==None) and j-1 != i and g1.has_node(i+1)==False and G.has_node(i+1)==True:
                new1 = i+1
                dist1 = matrix[j-1][i][0]
                connecting = j

    if new1 != None:
        g1.add_node(new1)
        g1.add_edge(j, new1)

    new2 = None
    dist2 = None
    for i in range(0, 9):
        for j in node_list2:
            if (dist2 > matrix[j-1][i][0] or dist2==None) and j-1 != i and g2.has_node(i+1)==False and G.has_node(i+1)==True:
                new2 = i+1
                dist2 = matrix[j-1][i][0]
                connecting = j
    if new2 != None:
        g2.add_node(new2)
        g2.add_edge(j, new2)
        

    if new1 == new2:
        shared.append(new1)
        G.remove_node(new1)
        return None

    if new1 != None:
        G.remove_node(new1)

    if new2 != None:
        G.remove_node(new2)
    
    
#print(nx.shortest_path_length(G,source=4, target=9))
subgraph_generation()

