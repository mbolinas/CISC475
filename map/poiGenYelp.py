'''
Adapted from Muhan's auto_csv.py code

Generate poi's in a given area (set in boundingBoxes.txt), along with
the startid's and endid's of the road segment a poi lies on.

This file will depend on a roadSegmentXXX.csv corresponding
to the area you want to generate poi's for. Please generate that using
roadSegmentGen.py before attempting to use this file.

Generated start/end node id's are still rough with some poi's given id's that
are not accurate. I'm still thinking of ways to get the most accurate id's

Expect long runtimes
'''
import requests
import sys
import geopy.distance
import time
from difflib import SequenceMatcher

#Define the API Key, define the endpoint and define the header
API_KEY = 'pdXJAlG5dNPgd3oqnypNJr1T7jihvqBzsrRMWPheuxR8IdN1CllWkLXaf0I6Y43igep_58Np2VFBQRwWEDCLYY_KnGZNfpKS8TeIYgV6wFX25xZVcx-LTbth9HyIXHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization' : 'Bearer %s' % API_KEY}

#--------------------------constants--------------------------------
RANGE = 2 # the max pages we try to get
LIMIT = 50 # number of results from a single call; max 50,min 20
# Categories to query. Full list here:
    # https://www.yelp.com/developers/documentation/v3/all_category_list
categories_large =\
    ['breakfast_brunch, All', 'chinese, All', 'buffets, All',\
    'bars, All', 'nightlife, All', 'italian, All', 'japanese, All',\
    'latin, All', 'steak, All', 'turkish, All', 'vietnamese, All',\
    'vegan, All', 'vegetarian, All', 'sushi, All' , 'soup, All',\
    'sandwiches, All', 'spanish, All', 'mexican, All', 'korean, All',\
    'kebab, All', 'indpak, All', 'hotdog, All', 'filipino']
categories_less =\
    ['chinese, All']
CATEGORIES = categories_less

ABBRV = {\
    'W' : 'West',\
    'S' : 'South',\
    'E' : 'East',\
    'N' : 'North',\
    'St' : 'Street',\
    'Ave' : 'Avenue',\
    'Pl' : 'Place',\
    'Plz' : 'Plaza',\
    'Sq' : 'Square',\
    'Pkw' : 'Parkway',\
    'Ln' : 'Lane',\
    'Ct' : 'Court',\
    'Blvd' : 'Boulevard'\
    }

SLEEP = 20 # how long to sleep between categories
MATCH_RATIO = .97 # minimum match ratio
# --------------------------------------------------------------------------

#--------------------------parse config file--------------------------------
# all fields can be modified in boundingBoxes.txt
bBoxFile = open('bBoxConfig.txt', "r")
lines = bBoxFile.readlines()
name = lines[1].rstrip('\n')

# Bounding box used for computation
BOUND_BOX = lines[0].replace('(','').replace(')','').rstrip('\n').split(',') # lol i'll fix later

# getting road segments for start/end id computation
roadSegmentInput = "./generated_map_data/roadSegments{}.csv".format(name)
ROAD_SEGMENTS = []
with open(roadSegmentInput, "r") as f:
    for line in f:
        items = line.rstrip().split(',')
        ROAD_SEGMENTS.append(items)

# Location used for computation.
LOCATION = lines[2].rstrip('\n')

# Output filename
OUTPUT_FILENAME = './generated_map_data/poiYelp{}.csv'.format(name)
bBoxFile.close()
# --------------------------------------------------------------------------

'''
Input
    lat/lon : float lat/lon coordinates
Output
    returns true if coordinates within bounding box, else false
'''
def withinBoundBox(lat, lon):
    a = lat > float(BOUND_BOX[0])
    b = lat < float(BOUND_BOX[2])
    c = lon > float(BOUND_BOX[1])
    d = lon < float(BOUND_BOX[3])
    return a and b and c and d

'''
Input
    address : a string
Output
    Returns a string with all abbreviations expanded.
    Abbreviations can be defined in ABBRV
'''
def expand_abbrv(address):
    x = address.split() # split address string into workable array
    y = x[1:len(x)] # ignore address housenumber
    # expand any present abbreviations
    for i in range(len(y)):
        if y[i] in ABBRV.keys():
            y[i] = ABBRV[y[i]]
    # transform split address back into string
    expanded = " ".join(z.encode("utf-8") for z in y)
    return expanded

'''
Input
    segment_array : array of road segments
Output
    Returns an array of road segments who's names match the given address
'''
def filter_names(address,segment_array):
    poi_street_name = expand_abbrv(address)
    arr = []
    for segment in segment_array:
        s = SequenceMatcher(None, segment[7], poi_street_name)
        if s.ratio() > MATCH_RATIO:
            arr.append(segment)
    return arr

'''
Input
    lat/lon : float lat/lon coordinates
    segment_array : array of road segments
Output
    Returns array of road segments who share the closest intersection to
    the given coordinates
'''
def get_immediate_segments(lat, long, segment_array):
    immediate_segments = []
    min_distance = sys.float_info.max
    for segment in segment_array:
        distance =\
            geopy.distance.distance((lat, long), (segment[2], segment[3])).km
        if distance < min_distance:
            min_distance = distance
            immediate_segments = []
            immediate_segments.append(segment)
        elif distance == min_distance:
            immediate_segments.append(segment)
    return immediate_segments

'''
Input
    lat/lon : float lat/lon coordinates
    address : a string
Output
    returns the closest road segment to a given lat/long coordinate.
    return value is of of the same form as a line in roadSegmentsXXX.csv
        [startid, endid, lat1, lon1, lat2, lon2, distance, name]
'''
def get_closest_segment(lat, long, address, road_segment_arr):
    name_filtered_segments = filter_names(address, road_segment_arr)

    if len(name_filtered_segments) == 0:
        immediate_segments = get_immediate_segments(lat, long, ROAD_SEGMENTS)
    else:
        immediate_segments = get_immediate_segments(lat, long, name_filtered_segments)

    #print(immediate_segments)
    # find closest segment out of immediate segments
    for segment in immediate_segments:
        distance =\
            geopy.distance.distance((lat, long), (segment[2], segment[3])).km
        if distance < segment[6]:
            return segment

    return immediate_segments[0]

'''
Input
    response : yelpfusion response
    file : the file to write to
Output
    No return value, writes output to file
'''
def writeResponse(response, file):
    business_data = response.json()
    for biz in business_data['businesses']:
        #print(biz)
        address = biz['location']['address1']
        latitude = biz['coordinates']['latitude']
        longitude = biz['coordinates']['longitude']
        rating = biz['rating']
        # sometimes businesses are missing specific info we need, so
        # we check that it has all the necessary information
        if all(k is not None for k in (latitude, longitude, address, rating)):
            segment = get_closest_segment(latitude, longitude, address, ROAD_SEGMENTS)
            row =\
                address.encode("utf-8").replace(',', '') + "," +\
                str(latitude) + "," +\
                str(longitude) + "," +\
                str(rating) + "," +\
                str(segment[0]) + "," +\
                str(segment[1]) + "\n"
            # yelp's api is sometimes innacurate, returning values outside the specified location
            # for this reason we double check if a location is within our bounding box
            if withinBoundBox(latitude, longitude):
                file.write(row)


def main():
    # Per the yelp FAQ, 'The API can only return up to 1,000 results at this time'
    # To get around this, we query a category until it reaches the max results, sleep
    # a bit, then move on to the next category
    f = open(OUTPUT_FILENAME, 'w')
    for category in CATEGORIES:
        offset = 1
        for i in range(RANGE):
            PARAMETER  = {'categories' : category,
                         'limit' : LIMIT,
                         'offset' : offset,
                         'location' : LOCATION}
            # API Call
            print('Querying category "{}" from {} to {}...'.format(category, offset, offset+RANGE))
            response =\
                requests.get(url=ENDPOINT, params=PARAMETER, headers=HEADERS)

            # if response is ok proceed writing to file
            if response.status_code == 200:
                print('Writing response...')
                writeResponse(response, f)
                # set offset for next API call
                print('Done. Moving to next offset.')
                offset += LIMIT

            # if response is bad, we've probably reached the
            # last page of results and should break
            elif response.status_code == 400:
                print('Reached max for category {}'.format(category))
                print('Sleeping for {} seconds'.format(SLEEP))
                time.sleep(SLEEP)
                break
    f.close()

if __name__ == '__main__':
    main()
