



def reconstruct_graph():
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
	count = 0
	for line in filein:
		parsedline = line.rstrip().split(",")
		print("line " + str(count) + ": " + parsedline[0])
		count = count + 1
	return 1

graph = reconstruct_graph()