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
import collections
import csv

api = overpy.Overpass()
ouputFile = 'intersectionsPhilly.csv'

'''
boundBoxAll:
    Some example bounding boxes (these are not exact since we are limited to
    specifying a box while most cities are obviously not shaped that way):
        City, State: (min lat, min long, max lat, max long)
boundBox:
    bounding box used for computation.
queryTags:
    which tags will be part of our result.
n_interesect:
    n_interesect is the minumum amount of roads to be considered
    an intersection.
    ie 2 will return intersections of 2 or more roads.
'''
boundBoxAll = {\
    'Newark, DE' : "'(39.614244,-75.837469,32.319778,-75.742246)'",\
    'Los Angeles, CA' : '(33.702967, -118.669821, 34.338940, -118.152887)',\
    'Tuscon, AZ' : '(32.003473, -111.059614, 32.320246,-110.736815)',\
    'Philadelphia, PA' : '(39.872422, -75.263458, 40.137522, -74.955755)'\
    }
boundBox = boundBoxAll['Philadelphia, PA']
queryTags = "'primary|secondary|residential|tertiary'"
n_interesect = 2

#API Call
#Fetch all ways and nodes within a bounding box and store in 'result'.
result = api.query("way{} ['highway'~{}];(._;>;);out body;".format(boundBox, queryTags))

'''
Getting information from result
NodeIDs: Array of all nodeIDs in bounding box
nodeInfo: Dictionary of form nodeID:nodeInfo
    nodeInfo is array of [name, tags(highway, walkway, etc.), latitude, longitude]
'''
nodeIDs = []
nodeInfo = {}
for way in result.ways:
    name = way.tags.get("name", "n/a")
    tags = way.tags.get("highway", "n/a")
    for node in way.nodes:
        n = [name, tags, node.lat, node.lon]
        nodeInfo[node.id] = n
        nodeIDs.append(node.id)

'''
To find intersections we look for ID's that appear more than once,
indicating multiple roads instersect at that location. Thus we can filter out
any ID's that only appear once.
n_interesect can be used to specify the minumum amount of roads to be considered
an intersection.
'''
duplicateIDs =\
    [item for item, count in collections.Counter(nodeIDs).items() if count >= n_interesect]

#print(len(nodeIDs))
#print(len(duplicateIDs))

'''
Write to CSV in form:
    nodeID, tag, latitude, longitude
'''
with open(ouputFile,'wb') as file:
    # each id left in duplicateIDs will be an intersection
    for id in duplicateIDs:
        file.write(nodeInfo[id][0].encode('utf-8') + ',')
        file.write(nodeInfo[id][1].encode('utf-8') + ',')
        file.write(str(nodeInfo[id][2]) + ',')
        file.write(str(nodeInfo[id][3]))
        file.write('\n')
