"""
This file attempts to get the start/end lat/long coordinates of all roads
within a given bounding box (min lat, min long, max lat, max long) and write them
to a CSV.

Code works well for block areas, with most road segments accurately
represent by the generated coordinates. Much more innacurate outside of
city blocks.
"""

import overpy
import csv
import geopy.distance

api = overpy.Overpass()
bBoxFile = open('boundingBoxes.txt', "r")

# Bounding box used for computation. Set in boundingBoxes.txt
lines = bBoxFile.readlines()
boundBox = lines[0]
# Output filename
ouputFile = './generated_map_data/roadSegments{}.csv'.format(lines[1].rstrip('\n'))
bBoxFile.close()

# queryKey/queryValues: which map features will be part of our result.
# List if all map features:
#   https://wiki.openstreetmap.org/wiki/Map_Features
queryKey = 'highway'
queryValues = "primary|secondary|residential|tertiary"

#API Call
#Fetch all ways and nodes within a bounding box and store in 'result'.
result = api.query("way{} ['{}'~'{}'];(._;>;);out body;".format(boundBox, queryKey, queryValues))

'''
Getting information from result
wayNodes: array of arrays
    [[wayNode_1, ... , wayNode_n], [wayNode_1, ... , wayNode_n], ... , n]
'''
allWays = []
for way in result.ways:
    allWays.append(way)

'''
Get distance between 2 lat/long coordinates
'''
def latLongDistance(lat1, lon1, lat2, lon2):
    return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

'''
Input: an array of way nodes
Returns a tuple of the two nodes who have the maximum distance
between each other and the distance.
'''
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
    return (nodeX, nodeY, max)

'''
Write to CSV in form:
    startid, endid, start lat, start long, end lat, end long, distance
'''
with open(ouputFile,'wb') as file:
    for way in allWays:
        # the 2 nodes of maximum distance
        # should accurately represent most road's
        # start and end points.
        tup = maxBetweenNodes(way.nodes)
        file.write(str(tup[0].id)+ ',') # start id
        file.write(str(tup[1].id)+ ',') # end id
        file.write(str(tup[0].lat)+ ',') # start lat
        file.write(str(tup[0].lon) + ',') # start long
        file.write(str(tup[1].lat) + ',') # end lat
        file.write(str(tup[1].lon) + ',') #  end long
        file.write(str(tup[2]) + ',') # distance
        file.write(way.tags.get("name", "n/a") + '\n')
