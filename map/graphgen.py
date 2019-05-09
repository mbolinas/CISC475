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



def file_to_graph(roadSegmentFilename, poiFilename):
    G = nx.Graph()
    # a rewrite of file_to_graph
    with open(roadSegmentFilename) as rseg:
        #format: [node1,node2,lat1,long1,lat2,long2,weight]
        reader = csv.reader(rseg,delimiter=",")
        for row in reader:
            node1 = row[0]
            node2 = row[1]
            lat1 = row[2]
            long1 = row[3]
            lat2 = row[4]
            long2 = row[5]
            length = row[6]
            G.add_node(node1,latitude=lat1,longitude=long1,nodetype="intersection")
            G.add_node(node2,latitude=lat2,longitude=long2,nodetype="intersection")
            G.add_edge(node1,node2,weight=length)

#    for e in G.edges(data=True):
#        print e

#    for n in G.nodes(data=True):
#        print n
            
    with open(poiFilename) as pois:
        #format: [name,lat,long,maplat,maplong,rating,startnode,endnode]
        #the lat and long is the real lat and long, while the mapping lat and long is
        #the place along an actual segment which it is assigned to.
        reader = csv.reader(pois,delimiter=",")
        for row in reader:
            #poi data
            name = row[0]
            lat = row[1]
            lng = row[2]
            maplat = row[3]
            maplng = row[4]
            rate = row[5]
            node1 = row[6]
            node2 = row[7]
            #data for endpoints of poi's road segment. has nodetype, latitude, and longitude
            node1Data = G.node[node1]
            node2Data = G.node[node2]
            
            #add poi as node
            G.add_node(name,latitude=maplat,longitude=maplng,reallat=lat,reallong=lng,rating=rate,nodetype="poi")
            #add edge to each endpoint
            G.add_edge(node1,name,weight=haversine(float(node1Data['longitude']),float(node1Data['latitude']),float(maplng),float(maplat)))
            G.add_edge(node2,name,weight=haversine(float(node2Data['longitude']),float(node2Data['latitude']),float(maplng),float(maplat)))
        
    nx.write_gpickle(G, 'graph_pickle')

#road segment file (start node, end node, start_lat, start_long, end_lat, end long, weight/distance)
filein = "road_segment.csv"
poifilein = "res_mapping_road_based.csv"
if(filein == ""):
        print("Please specify a file to read in (modify this file or call file_to_graph(filename) )")
else:
        file_to_graph(filein, poifilein)


'''
Serializes graph to graph_pickle
Can be read using read_gpickle(path)
'''
