"""
This file attempts to find all intersections within a given
bounding box (min lat, min long, max lat, max long) and write them
to a CSV

Some known issues:
    - Points written to the CSV with certain tags (like 'service' or 'footway')
    seem to be noise and don't represent an intersection. These should probably
    be filtered out.

    - Probably more.
"""

import overpy
import csv
import geopy.distance

api = overpy.Overpass()
ouputFile = 'test.csv'

'''
boundBoxAll:
    Some example bounding boxes (these are not exact since we are limited to
    specifying a box while most cities are obviously not shaped that way):
        City, State: (min lat, min long, max lat, max long)
boundBox:
    bounding box used for computation.
queryTags:
    which tags will be part of our result.
'''
boundBoxAll = {\
    'Newark, DE' : '(39.614244,-75.837469,32.319778,-75.742246)',\
    'Los Angeles, CA' : '(33.702967, -118.669821, 34.338940, -118.152887)',\
    'Tuscon, AZ' : '(32.003473, -111.059614, 32.320246,-110.736815)',\
    'Philadelphia, PA' : '(39.872422, -75.263458, 40.137522, -74.955755)'\
    }
boundBox = boundBoxAll['Philadelphia, PA']
queryTags = "'primary|secondary|residential|tertiary'"

#API Call
#Fetch all ways and nodes within a bounding box and store in 'result'.
result = api.query("way{} ['highway'~{}];(._;>;);out body;".format(boundBox, queryTags))

'''
Getting information from result
wayNames: Array of all way names in bounding box
nodeInfo: Dictionary of form way:wayNodes
    wayNodes is array of [wayNode_1, wayNode_2, ... , wayNode_n]
'''
wayNodes = []
#allNodesCSV = open('allNodesCSV.csv', 'wb')
for way in result.ways:
    name = way.tags.get("name", "n/a")
    #tags = way.tags.get("highway", "n/a")
    wayNodes.append(way.nodes)
    '''
    allNodesCSV.write(name.encode('utf-8') + ',')
    allNodesCSV.write(tags.encode('utf-8') + ',')
    allNodesCSV.write(str(node.lat) + ',')
    allNodesCSV.write(str(node.lon))
    allNodesCSV.write('\n')
    '''
#allNodesCSV.close()

'''
Get distance between 2 lat/long coordinates
'''
def latLongDistance(lat1, lon1, lat2, lon2):
    return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

def maxBetweenNodes(wayNodeArray):
    max = 0
    nodeX = None
    nodeY = None
    for i in range(len(wayNodeArray)-1):
        lat1 = wayNodeArray[i].lat
        lon1 = wayNodeArray[i].lon
        for j in range(i+1, len(wayNodeArray)):
            lat2 = wayNodeArray[j].lat
            lon2 = wayNodeArray[j].lon
            distance = latLongDistance(lat1, lon1, lat2, lon2)
            if distance > max:
                max = distance
                nodeX = wayNodeArray[i]
                nodeY = wayNodeArray[j]
    return (nodeX, nodeY)

testDistanceCSV = open('testDistance.csv', 'wb')
for nodeArray in wayNodes:
    tup = maxBetweenNodes(nodeArray)
    testDistanceCSV.write(str(tup[0].lat)+ ',')
    testDistanceCSV.write(str(tup[0].lon) + ',')
    testDistanceCSV.write(str(tup[1].lat) + ',')
    testDistanceCSV.write(str(tup[1].lon) + '\n')
testDistanceCSV.close()

#print(maxBetweenNodes(arr))

'''
Write to CSV in form:
    nodeID, tag, latitude, longitude
'''
def writeCSV():
    with open(ouputFile,'wb') as file:
        # each id left in duplicateIDs will be an intersection
        for id in duplicateIDs:
            file.write(nodeInfo[id][0].encode('utf-8') + ',')
            file.write(nodeInfo[id][1].encode('utf-8') + ',')
            file.write(str(nodeInfo[id][2]) + ',')
            file.write(str(nodeInfo[id][3]))
            file.write('\n')
#writeCSV()
