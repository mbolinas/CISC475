import networkx as nx
import matplotlib.pyplot as plt


#data = open("road_segment.csv", "r")

filein = ""
if(filein == ""):
	print("Please specify a file to read in (modify this file or call file_to_graph(filename) )")
else:
	file_to_graph(filein)


def file_to_graph(filename):
	data = open(filename, "r")
	G = nx.read_edgelist(data, delimiter=',', nodetype=str, data=[('start_latitude',float),('start_longitude',float),('end_latitude',float),('end_longitude',float),('weight',float)])
	nx.write_gpickle(G, 'graph_pickle')


'''
for e in G.edges():
    print e

pos = nx.spring_layout(G,scale=1)

#node_labels = nx.get_node_attributes(G,'state')
#nx.draw_networkx_labels(G, pos, labels = node_labels)
edge_labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)

nx.draw(G,pos, with_labels=True)
plt.savefig('this.png')
plt.show()
'''

'''
Serializes graph to graph_pickle
Can be read using read_gpickle(path)
'''
