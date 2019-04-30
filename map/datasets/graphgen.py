import csv
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt



#distance between two coordinates
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def file_to_graph(filename):
        data = open(filename, "r")
        G = nx.read_edgelist(data, delimiter=',', nodetype=str, data=[('start_latitude',float),('start_longitude',float),('end_latitude',float),('end_longitude',float),('weight',float)])

        #set all nodes to intersection type
        nodetype = []
        nx.set_node_attributes(G, nodetype, 'type')
        nodetype.append('intersection')
        #for n in G.nodes(data=True):
        #    print n
        

        with open("res_mapping_road_based.csv") as res_csv:
                reader = csv.reader(res_csv,delimiter=",")

                edgenum = 9999
                
                for row in reader:
                        #format: [name,lat,long,maplat,maplong,rating,startnode,endnode]
                        #find edge with matching nodes, and append this node
                        rowData = G.get_edge_data(row[6],row[7])
                        x1 = rowData["start_longitude"]
                        y1 = rowData["start_latitude"]
                        x2 = rowData["end_longitude"]
                        y2 = rowData["end_latitude"]

                        print "\nRoad segment: x1: " + str(x1) + " y1: " + str(y1) + " x2: " + str(x2) + " y2: " + str(y2)
                        print "POI: lat: " + row[3] + " long: " + row[4]
                        print "calcdist for segment: " + str(sqrt(pow((x2-x1),2) + pow((y2-y1),2)))
                        print "list dist: " + str(rowData["weight"])
                        print "haversine: " + str(haversine(x1,y1,x2,y2))
                        print "haversine accuracy: " + str((rowData["weight"]-(rowData["weight"] - haversine(x1,y1,x2,y2)))/rowData["weight"]*100)
                        #delete orgininal edge, make a new node and two new edges, one
                        #to each original node from the new node
                        #G.remove_edge(row[6],row[7])
                        G.add_edge(row[6],edgenum,weight=haversine(x1,y1,float(row[4]),float(row[3])))
                        G.add_edge(row[7],edgenum,weight=haversine(x2,y2,float(row[4]),float(row[3])))
                        print "new dist: "
                        print G.get_edge_data(row[6],edgenum)["weight"]
                        print G.get_edge_data(row[7],edgenum)["weight"]
                        print "total: " + str(G.get_edge_data(row[7],edgenum)["weight"] + G.get_edge_data(row[6],edgenum)["weight"])
                        edgenum = edgenum + 1


        #for e in G.edges():
        #        print e

        nx.write_gpickle(G, 'graph_pickle')


        #############################
        ### Old code for displaying image of the graph (needs some work with spacing, sizing, etc.)
        #############################

        #pos = nx.spring_layout(G,scale=1)

        #node_labels = nx.get_node_attributes(G,'state')
        #nx.draw_networkx_labels(G, pos, labels = node_labels)
        #edge_labels = nx.get_edge_attributes(G,'weight')
        #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)

        #nx.draw(G,pos, with_labels=True)
        #plt.savefig('this.png')
        #plt.show()
        ############################################################

#road segment file (start node, end node, start_lat, start_long, end_lat, end long, weight/distance)
filein = "road_segment.csv"

if(filein == ""):
        print("Please specify a file to read in (modify this file or call file_to_graph(filename) )")
else:
        file_to_graph(filein)


'''
Serializes graph to graph_pickle
Can be read using read_gpickle(path)
'''
