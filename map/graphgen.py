import networkx as nx
import matplotlib.pyplot as plt


data = open("road_segment.csv").read()


G = nx.read_edgelist(data, delimiter=',', nodetype=str, data=[('weight',int),('att1',int)])
for e in G.edges():
    print e

pos = nx.spring_layout(G,scale=1)

node_labels = nx.get_node_attributes(G,'state')
nx.draw_networkx_labels(G, pos, labels = node_labels)
edge_labels = nx.get_edge_attributes(G,'state')
nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)

nx.draw(G,pos, with_labels=True)
plt.savefig('this.png')
plt.show() 