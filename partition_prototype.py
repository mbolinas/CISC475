import networkx as nx

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 5), (3, 6), (3, 7), (4, 6), (5, 7), (5, 9), (6, 8), (7, 9)])

shared = []
matrix = []
l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for x in range(1, 10):
    matrix.append([[], [], [], [], [], [], [], [], []])

matrix[0][0].append(0)
matrix[0][1].append(1)
matrix[0][2].append(1)
matrix[0][3].append(2)
matrix[0][4].append(2)
matrix[0][5].append(2)
matrix[0][6].append(2)
matrix[0][7].append(3)
matrix[0][8].append(3)

matrix[1][0].append(1)
matrix[1][1].append(0)
matrix[1][2].append(1)
matrix[1][3].append(1)
matrix[1][4].append(2)
matrix[1][5].append(1)
matrix[1][6].append(3)
matrix[1][7].append(2)
matrix[1][8].append(3)

matrix[2][0].append(1)
matrix[2][1].append(1)
matrix[2][2].append(0)
matrix[2][3].append(2)
matrix[2][4].append(1)
matrix[2][5].append(1)
matrix[2][6].append(1)
matrix[2][7].append(2)
matrix[2][8].append(2)

matrix[3][0].append(2)
matrix[3][1].append(1)
matrix[3][2].append(2)
matrix[3][3].append(0)
matrix[3][4].append(3)
matrix[3][5].append(1)
matrix[3][6].append(3)
matrix[3][7].append(2)
matrix[3][8].append(4)

matrix[4][0].append(2)
matrix[4][1].append(2)
matrix[4][2].append(1)
matrix[4][3].append(3)
matrix[4][4].append(0)
matrix[4][5].append(2)
matrix[4][6].append(1)
matrix[4][7].append(3)
matrix[4][8].append(1)

matrix[5][0].append(2)
matrix[5][1].append(1)
matrix[5][2].append(1)
matrix[5][3].append(1)
matrix[5][4].append(2)
matrix[5][5].append(0)
matrix[5][6].append(3)
matrix[5][7].append(1)
matrix[5][8].append(3)

matrix[6][0].append(2)
matrix[6][1].append(3)
matrix[6][2].append(1)
matrix[6][3].append(4)
matrix[6][4].append(1)
matrix[6][5].append(3)
matrix[6][6].append(0)
matrix[6][7].append(4)
matrix[6][8].append(1)

matrix[7][0].append(3)
matrix[7][1].append(2)
matrix[7][2].append(2)
matrix[7][3].append(2)
matrix[7][4].append(3)
matrix[7][5].append(1)
matrix[7][6].append(4)
matrix[7][7].append(0)
matrix[7][8].append(4)

matrix[8][0].append(3)
matrix[8][1].append(3)
matrix[8][2].append(2)
matrix[8][3].append(4)
matrix[8][4].append(1)
matrix[8][5].append(3)
matrix[8][6].append(1)
matrix[8][7].append(4)
matrix[8][8].append(0)




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
    
    
#finds the closest node to node n
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

