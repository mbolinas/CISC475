"""
This file attempts to find all intersections within a given
bounding box (min lat, min long, max lat, max long) and write them
to a CSV.

Bounding box and output filename can be modifed in bBoxConfig.txt
"""
import overpy
import collections
import csv
import time

api = overpy.Overpass()

#-------------------------------constants----------------------------------
# queryKey/queryValues: which map features will be part of our result.
# List if all map features:
#   https://wiki.openstreetmap.org/wiki/Map_Features
QUERY_KEY = 'highway'
QUERY_VALUES = "primary|secondary|residential|tertiary"

# n_interesect is the minumum amount of roads to be considered
# an intersection. ie 2 will return intersections of 2 or more roads.
N_INTERSECT = 2
# --------------------------------------------------------------------------

#--------------------------parse config file--------------------------------
bBoxFile = open('bBoxConfig.txt', "r")
lines = bBoxFile.readlines()

# Bounding box used for computation
BOUND_BOX = lines[0]

OUTPUT_FILENAME =\
    './generated_map_data/intersections{}.csv'\
    .format(lines[1].rstrip('\n'))

bBoxFile.close()
# --------------------------------------------------------------------------

'''
Parse an api result into a workable data structures.
Input
    result : an API call result
Output
    No return value, writes to arr and dict
    arr: Array of all nodeIDs in bounding box
    dict: Dictionary of form nodeID:nodeInfo
        nodeInfo is array of
        [name, tags(highway, walkway, etc.), latitude, longitude]

'''
def parse_result(result, arr, dict):
    for way in result.ways:
        name = way.tags.get("name", "n/a")
        tags = way.tags.get("highway", "n/a")
        for node in way.nodes:
            n = [name, tags, node.lat, node.lon]
            dict[node.id] = n
            arr.append(node.id)

'''
Input
    id_array : array of node id's
Output
    returns an array of only the items that appear multiple times in id_array
'''
def get_duplicates(id_array):
    duplicates =\
        [item for item,\
         count in collections.Counter(id_array).items() if count >= N_INTERSECT]
    return duplicates

'''
Input
    filename : name of file to write
    id_array : array of node id's
    info_dict : dictionary of form nodeID:nodeInfo
Output
    No return value, write to CSV in form:
        name, latitude, longitude, type, id
'''
def write_intersections(filename, id_array, info_dict):
    with open(filename,'wb') as f:
        for id in id_array:
            try:
                f.write(info_dict[id][0].encode('utf-8').replace(',', '') + ',') # name
                f.write(str(info_dict[id][2]) + ',') # lat
                f.write(str(info_dict[id][3]) + ',') # long
                f.write(info_dict[id][1].encode('utf-8') + ',') # type
                f.write(str(id) + '\n') # id
            except Exception as e:
                print(e)

def main():
    start_time = time.time()
    # API call
    print('Querying API...')
    result =\
        api.query(\
        "way{} ['{}'~'{}'];(._;>;);out body;"\
        .format(BOUND_BOX, QUERY_KEY, QUERY_VALUES))

    # parse result into nodeIDs and nodeInfo
    node_IDs = []
    node_info = {}
    print('Parsing result...')
    parse_result(result, node_IDs, node_info)

    # To find intersections we look for ID's that appear more than once,
    # indicating multiple roads instersect at that location. Thus we can
    # filter out any ID's that only appear once.
    print('Getting duplicates...')
    duplicate_IDs = get_duplicates(node_IDs)

    print('Writing to {}'.format(OUTPUT_FILENAME))
    write_intersections(OUTPUT_FILENAME, duplicate_IDs, node_info)

    print("Runtime: {} minutes.".format((time.time() - start_time) / 60))

if __name__ == '__main__':
    main()
