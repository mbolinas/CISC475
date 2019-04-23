"""
This file attempts to get the start/end lat/long coordinates of all roads
within a given bounding box (min lat, min long, max lat, max long) and write them
to a CSV.

Known issues:
    Code works decently for block areas, with most road segments accurately
    represent by the generated coordinates. Much more innacurate outside of
    city blocks.

    Some coordinates are only slighly innacurate, sometimes stopping
    short of a road's real-world end. Other coordinates are much worse,
    giving points completely off the road
"""

import overpy
import csv
import geopy.distance

api = overpy.Overpass()
ouputFile = './generated/roadSegmentsManhattan.csv'

'''
Some example bounding boxes (these are not exact since we are limited to
specifying a box while most cities are obviously not shaped that way):
    'Newark, DE' : '(39.651363,-75.785638,39.700776,-75.723828)'
    'Los Angeles, CA' : '(33.702967, -118.669821, 34.338940, -118.152887)'
    'Tuscon, AZ' : '(32.003473, -111.059614, 32.320246,-110.736815)',
    'Philadelphia, PA' : '(39.872422, -75.263458, 40.137522, -74.955755)'
    'Manhattan, New York, NY' : '(40.700943, -74.008633, 40.879111, -73.910761)'
    'Paris, France' : '(48.816066, 2.227627, 48.903228, 2.467784)'
boundBox:
    bounding box used for computation.
queryTags:
    which tags will be part of our result.
'''
boundBox = '(40.700943, -74.008633, 40.879111, -73.910761)'
# List if all map features:
#   https://wiki.openstreetmap.org/wiki/Map_Features
queryKeys = 'highway'
queryValues = "primary|secondary|residential|tertiary"

#API Call
#Fetch all ways and nodes within a bounding box and store in 'result'.
result = api.query("way{} ['{}'~'{}'];(._;>;);out body;".format(boundBox, queryKeys, queryValues))

'''
Getting information from result
wayNodes: array of arrays
    [[wayNode_1, ... , wayNode_n], [wayNode_1, ... , wayNode_n], ... , n]
'''
wayNodes = []
for way in result.ways:
    name = way.tags.get("name", "n/a")
    wayNodes.append(way.nodes)

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
    for nodeArray in wayNodes:
        # the 2 nodes of maximum distance
        # should accurately represent most road's
        # start and end points.
        tup = maxBetweenNodes(nodeArray)
        file.write(str(tup[0].id)+ ',') # start id
        file.write(str(tup[1].id)+ ',') # end id
        file.write(str(tup[0].lat)+ ',') # start lat
        file.write(str(tup[0].lon) + ',') # start long
        file.write(str(tup[1].lat) + ',') # end lat
        file.write(str(tup[1].lon) + ',') #  end long
        file.write(str(tup[2]) + '\n') # distance
