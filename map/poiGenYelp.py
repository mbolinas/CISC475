'''
Adapted from Muhan's auto_csv.py code

Generate poi's in a given area (set in boundingBoxes.txt), along with
the startid's and endid's of the road segment a poi lies on.

This file will depend on a roadSegmentXXX.csv corresponding
to the area you want to generate poi's for. Please generate that using
roadSegmentGen.py before attempting to use this file.

Generated start/end node id's are still rough with some poi's not mapped to the
correct road segment. I'm still thinking of ways to get the most accurate id's

Expect long runtimes
'''
import requests
import sys
import geopy.distance
import time

#Define the API Key, define the endpoint and define the header
API_KEY = 'pdXJAlG5dNPgd3oqnypNJr1T7jihvqBzsrRMWPheuxR8IdN1CllWkLXaf0I6Y43igep_58Np2VFBQRwWEDCLYY_KnGZNfpKS8TeIYgV6wFX25xZVcx-LTbth9HyIXHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization' : 'Bearer %s' % API_KEY}

#--------------------------constants--------------------------------
RANGE = 50 # the max pages we try to get
LIMIT = 50 # number of results from a single call; max 50,min 20
# Categories to query. Full list here:
    # https://www.yelp.com/developers/documentation/v3/all_category_list
CATEGORIES =\
    ['breakfast_brunch, All', 'chinese, All', 'buffets, All',\
    'bars, All', 'nightlife, All', 'italian, All', 'japanese, All',\
    'latin, All', 'steak, All', 'turkish, All', 'vietnamese, All',\
    'vegan, All', 'vegetarian, All', 'sushi, All' , 'soup, All',\
    'sandwiches, All', 'spanish, All', 'mexican, All', 'korean, All',\
    'kebab, All', 'indpak, All', 'hotdog, All', 'filipino']
CATEGORIES_LESS =\
    ['chinese, All']

ABBRV_POSTAL = {\
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
ABBRV_OTHER = {\
    'W' : 'West',\
    'S' : 'South',\
    'E' : 'East',\
    'N' : 'North',\
    'St' : 'Saint'
    }

SLEEP = 20 # how long to sleep between categories

POI_ID = 0 # global variable to assign unique id's to poi's
# --------------------------------------------------------------------------

#--------------------------parse config file--------------------------------
# all fields can be modified in boundingBoxes.txt
bBoxFile = open('bBoxConfig.txt', "r")
lines = bBoxFile.readlines()
name = lines[1].rstrip('\n')

# Bounding box used for computation
BOUND_BOX = lines[0].replace('(','').replace(')','').rstrip('\n').split(',')

# getting road segments for start/end id computation
roadSegmentInput = "./generated_map_data/roadSegments{}.csv".format(name)

# Location used for computation.
LOCATION = lines[2].rstrip('\n')

# Output filename
OUTPUT_FILENAME = './generated_map_data/poiYelp{}.csv'.format(name)
bBoxFile.close()
# --------------------------------------------------------------------------

'''
Parse a road segment file into a dictionary
'''
def get_road_segments(road_segment_input):
    dict = {}
    with open(road_segment_input, "r") as f:
        for line in f:
            items = line.rstrip().split(',')
            name = items[7].replace("'", "")
            if name not in dict:
                dict[name] = [items]
            else:
                dict[name].append(items)
    return dict

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

    # expand last token, which is generally a postal abbreviation
    if y[len(y)-1] in ABBRV_POSTAL:
        y[len(y)-1] = ABBRV_POSTAL[y[len(y)-1]]

    # expand any other abbreviations
    for i in range(len(y)-1):
        if y[i] in ABBRV_OTHER:
            y[i] = ABBRV_OTHER[y[i]]

    # transform split address back into string
    expanded = " ".join(z.encode("utf-8") for z in y)
    return expanded

'''
Input
    lat/lon : float lat/lon coordinates
    segment_array : array of road segments
Output
    Returns array of road segments who share the closest intersection to
    the given coordinates
'''
def get_immediate_segments(lat, long, segment_dict):
    immediate_segments = []
    min_distance = sys.float_info.max
    for key in segment_dict.keys():
        for segment in segment_dict[key]:
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
    segment : a road segment
Output
    The ratio of the distance of the given coordinates on the road segment
'''
def calculateRatio(lat, long, segment):
    distance_APoi =\
        geopy.distance.distance((lat, long), (segment[2], segment[3])).km
    distance_BPoi =\
        geopy.distance.distance((lat, long), (segment[4], segment[5])).km

    return distance_APoi / (distance_APoi + distance_BPoi)

'''
Input
    lat/lon : float lat/lon coordinates
    address : a string
Output
    returns the closest road segment to a given lat/long coordinate.
    return value is of of the same form as a line in roadSegmentsXXX.csv
        [startid, endid, lat1, lon1, lat2, lon2, distance, name]
'''
def get_closest_segment(lat, long, address, segment_dict):
    address_expanded = expand_abbrv(address)
    immediate_segments = []

    # attempt to use address matching
    if address_expanded in segment_dict:
        immediate_segments = segment_dict[address_expanded]

    # if address matching fails, use get_immediate_segments()
    if len(immediate_segments) == 0:
        immediate_segments = get_immediate_segments(lat, long, segment_dict)

    # find closest segment out of immediate segments
    for segment in immediate_segments:
        #print(segment[7])
        '''
        if (lat > segment[2] and lat < segment[4] and lon > segment[3] and lon < segment[5])\
            or (lat < segment[2] and lat > segment[4] and lon < segment[3] and lon > segment[5]):
            return segment
        '''
        distanceA = geopy.distance.distance((lat, long), (segment[2], segment[3])).km
        distanceB = geopy.distance.distance((lat, long), (segment[4], segment[5])).km
        if distanceA < segment[6] and distanceB < segment[6]:
            return segment

    return None

'''
Input
    response : yelpfusion response
    file : the file to write to
Output
    No return value, writes output to file
'''
def writeResponse(response, file, segment_dict):
    global POI_ID
    business_data = response.json()
    for biz in business_data['businesses']:
        address = biz['location']['address1']
        latitude = biz['coordinates']['latitude']
        longitude = biz['coordinates']['longitude']
        rating = biz['rating']
        price = None
        if 'price' in biz:
            price = biz['price']
        # sometimes businesses are missing specific info we need, so
        # we check that it has all the necessary information
        if all (k is not None for k in (address, latitude, longitude, rating, price)) and len(address.split()) > 2:
            # road segment the poi is on
            segment = get_closest_segment(latitude, longitude, address, segment_dict)
            # ratio of poi's distance on road segment
            if segment is not None:
                ratio = calculateRatio(latitude, longitude, segment)

                row =\
                    str(POI_ID) + "," +\
                    address.encode("utf-8").replace(',', '') + "," +\
                    str(latitude) + "," +\
                    str(longitude) + "," +\
                    str(rating) + "," +\
                    price.encode("utf-8") + "," +\
                    str(segment[0]) + "," +\
                    str(segment[1]) + "," +\
                    str(ratio) + "\n"
                print(row)
                # yelp's api is sometimes innacurate, returning values outside the specified location
                # for this reason we double check if a location is within our bounding box
                if withinBoundBox(latitude, longitude):
                    # increment id
                    POI_ID += 1
                    try:
                        file.write(row)
                    except Exception as e:
                        print(e)

def main():
    start_time = time.time()
    road_segment_dict = get_road_segments(roadSegmentInput)
    #print(road_segment_dict)

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
            response = requests.get(url=ENDPOINT, params=PARAMETER, headers=HEADERS)

            # if response is ok proceed writing to file
            if response.status_code == 200:
                print('Writing response...')
                writeResponse(response, f, road_segment_dict)
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
    print("Runtime: {} minutes.".format((time.time() - start_time) / 60))


if __name__ == '__main__':
    main()
