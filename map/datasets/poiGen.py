"""

"""

import overpy
import csv

api = overpy.Overpass()
ouputFile = './generated/poiNewark.csv'
city = 'Newark, DE'

'''
boundBoxAll:
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
    lat, long
'''
with open(ouputFile,'wb') as file:
    for node in poiNodes:
        file.write(str(node.lat)+ ',') # lat
        file.write(str(node.lon)) # long
        file.write('\n') # long
