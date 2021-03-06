"""
DEPRECATED - USE poiGenYelp.py
"""

import overpy
import csv

api = overpy.Overpass()
bBoxFile = open('boundingBoxes.txt', "r")

# Bounding box used for computation. Set in boundingBoxes.txt
lines = bBoxFile.readlines()
boundBox = lines[0]
# Output filename
ouputFile = './generated_map_data/poi{}.csv'.format(lines[1].rstrip('\n'))
bBoxFile.close()

# queryKey/queryValues: which map features will be part of our result.
# List if all map features:
#   https://wiki.openstreetmap.org/wiki/Map_Features
queryKey = 'amenity'
queryValues = "bar|cafe|restaurant|fast_food"

#API Call
#Fetch all within a bounding box and store in 'result'.
result = api.query("node{} ['{}'~'{}'];(._;>;);out body;".format(boundBox, queryKey, queryValues))

'''
Getting information from result
'''
poiNodes = []
for node in result.nodes:
    print(node.tags)
    poiNodes.append(node)

'''
Write to CSV in form:
    street, lat, long
'''
with open(ouputFile,'wb') as file:
    for node in poiNodes:
        address = 'N/A'
        # some nodes in openmaps don't have data on street number and name
        # so we have to check. Else we write N/A
        if all(key in node.tags for key in ['addr:housenumber', 'addr:street']):
            address = node.tags['addr:housenumber'].encode('utf-8') +\
            ' ' + node.tags['addr:street'].encode('utf-8')
        # need to remove commas since some street names with
        # commas end up split into different columns
        file.write(address.replace(',', '') + ',') # name
        file.write(str(node.lat) + ',') # lat
        file.write(str(node.lon) + ',') # long
        file.write(node.tags['name'] + '\n') # name
