"""
This file attempts to get the start/end lat/long coordinates of all roads
within a given bounding box (min lat, min long, max lat, max long) and write them
to a CSV.

Code works well for block areas, with most road segments accurately
represent by the generated coordinates. More innacurate outside of
city blocks.

Bounding box and output filename can be modifed in bBoxConfig.txt
"""
import overpy
import csv
import geopy.distance
import time

api = overpy.Overpass()

#-------------------------------constants----------------------------------
# queryKey/queryValues: which map features will be part of our result.
# List if all map features:
#   https://wiki.openstreetmap.org/wiki/Map_Features
QUERY_KEY = 'highway'
QUERY_VALUES = "primary|secondary|residential|tertiary"
# --------------------------------------------------------------------------

#--------------------------parse config file--------------------------------
bBoxFile = open('bBoxConfig.txt', "r")

# Bounding box used for computation
lines = bBoxFile.readlines()
BOUND_BOX = lines[0]

OUTPUT_FILENAME = './generated_map_data/roadSegments{}.csv'.format(lines[1].rstrip('\n'))

bBoxFile.close()
# --------------------------------------------------------------------------

'''
Parse an api result into a workable data structure
Input
    result : an API call result.
Output
    returns a 2d array of ways and waynodes in form:
        [[wayNode_0, ... , wayNode_n], [wayNode_0, ... , wayNode_n], ... , n]
'''
def parse_result(result):
    arr = []
    for way in result.ways:
        arr.append(way)
    return arr

'''
Input
    way_node_array : an array of way nodes
Output
    Returns an array of the two nodes who have the maximum distance
    between each other, as well as the distance between them.
        Form: [node_X, node_Y, distance]
'''
def max_between_nodes(way_node_array):
    max = 0
    node_X = None
    node_Y = None
    for i in range(len(way_node_array)-1):
        lat1 = way_node_array[i].lat
        lon1 = way_node_array[i].lon
        for j in range(i+1, len(way_node_array)):
            lat2 = way_node_array[j].lat
            lon2 = way_node_array[j].lon
            distance = geopy.distance.distance((lat1, lon1), (lat2, lon2)).km
            if distance > max:
                max = distance
                node_X = way_node_array[i]
                node_Y = way_node_array[j]
    return [node_X, node_Y, max]

'''
Input
    array of ways
Output
    returns an array of road segments
        [(startNode0, endNode0, distance), (startNode1, endNode1, distance), ... , n]
'''
def get_segments(way_array):
    segments = []
    for way in way_array:
        # the 2 nodes of maximum distance
        # should accurately represent most road's
        # start and end points.
        seg = max_between_nodes(way.nodes)
        seg.append(way.tags.get("name", "n/a"))
        segments.append(seg)
    return segments

'''
Input
    filename : name of file to write
    segment_array : array of road segments
Output
    No return value, write to CSV in form:
        name, latitude, longitude, type, id
'''
def write_road_segments(filename, segment_array):
    with open(filename,'wb') as f:
        for seg in segment_array:
            try:
                f.write(str(seg[0].id)+ ',') # start id
                f.write(str(seg[1].id)+ ',') # end id
                f.write(str(seg[0].lat)+ ',') # start lat
                f.write(str(seg[0].lon) + ',') # start long
                f.write(str(seg[1].lat) + ',') # end lat
                f.write(str(seg[1].lon) + ',') #  end long
                f.write(str(seg[2]) + ',') # distance
                f.write(seg[3].encode('utf-8').replace(',', '') + '\n') # name
            except Exception as e:
                print(e)
def main():
    start_time = time.time()
    # API Call
    print('Querying API...')
    result = api.query(\
        "way{} ['{}'~'{}'];(._;>;);out body;"\
        .format(BOUND_BOX, QUERY_KEY, QUERY_VALUES))

    # parse result into all_ways
    print('Parsing result...')
    all_ways = parse_result(result)

    print('Getting segments...')
    segments = get_segments(all_ways)

    print('Writing to {}'.format(OUTPUT_FILENAME))
    write_road_segments(OUTPUT_FILENAME, segments)

    print("Runtime: {} minutes.".format((time.time() - start_time) / 60))

if __name__ == '__main__':
    main()
