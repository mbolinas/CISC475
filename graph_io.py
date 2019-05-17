import networkx as nx

#purpose of file:
#after the algorithm has been run, we have a set of POIs that are 'valid'
#the script that displays the map takes in a file containing all the POIs
#so this file will write to file the POIs that were relevant for a specific location


#takes in a set of POIs and intersects that set with the set
#of all POIs (./map/res_mapping_road_based.csv by default, change this as you change the area)


#this function runs an intersection on the set of all POIs in the graph
#with the set of non-dominated POIs, and writes the result in
#a .csv file named after the road the algorithm was run on.
#currently, the set of all POIs is hard-coded in res_f, but it can be overwritten
#and parameterized fairly easily
def export_poi_set(road_name, poi_set):
	result = open("./map/road_" + road_name + ".csv", "w")
	res_f = open("./map/res_mapping_road_based.csv", "r")
	count = 0
	for s in res_f:
		items = s.rstrip().split(',')
		#this intersect algorithm runs in O(n^2), there may be a better alternative
		for name in poi_set:	
			if (items[0] == name):
				if(count != 0):
					result.write("\n")
				result.write(s)
				count = count + 1

#returns a graph from a pickle file
def reconstruct_graph(filein):
	src = "./map/graph.csv"
	#src = "./map/res_mapping_road_based.csv"
	try:
		graph_src = open(src, "r")
		graph = file_to_graph(graph_src)
		graph_src.close()
		return graph
	except IOError as error:
		print("ERROR:\nCould not open" + src + "\nMake sure file exists and can be accessed")
		return None

def file_to_graph(filein):
	try:
		G = nx.read_gpickle(filein)
		return G
	except IOError as error:
		print("ERROR:\nCould not open" + src + "\nMake sure file exists and can be accessed")
		return None


