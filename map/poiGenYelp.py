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
    ['chinese, All', 'italian, All']
ABBRV = {\
    'W' : 'West',\
    'S' : 'South',\
    'E' : 'East',\
    'N' : 'North'\
    }
SLEEP = 20 # how long to sleep between categories
MATCH_RATIO = .70 # minimum match ratio
# --------------------------------------------------------------------------


#--------------------------parse config file--------------------------------
# all fields can be modified in boundingBoxes.txt
bBoxFile = open('boundingBoxes.txt', "r")
lines = bBoxFile.readlines()

# Bounding box used for computation
boundBox = lines[0].replace('(','').replace(')','').rstrip('\n').split(',') # lol i'll fix later

# getting road segments for start/end id computation
name = lines[1].rstrip('\n')
roadSegmentInput = "./generated_map_data/roadSegments{}.csv".format(name)
roadSegments = []
with open(roadSegmentInput, "r") as f:
    for line in f:
        items = line.rstrip().split(',')
        roadSegments.append(items)

# Location used for computation.
location = lines[2].rstrip('\n')

# Output filename
ouputFile = './generated_map_data/poiYelp{}.csv'.format(name)
bBoxFile.close()
# --------------------------------------------------------------------------

'''
Check if given coordinates are within the bounding box
Input : float latitude, float longitude
'''
def withinBoundBox(lat, lon):
    a = lat > float(boundBox[0])
    b = lat < float(boundBox[2])
    c = lon > float(boundBox[1])
    d = lon < float(boundBox[3])
    return a and b and c and d

'''
Expand any abbreviations present in an address
Input : an array of strings
No return value, modifies given array
'''
def expandAbbrv(addressArr):
    for i in range(len(addressArr)):
        if addressArr[i] in ABBRV.keys():
            addressArr[i] = ABBRV[addressArr[i]]

'''
Get the segments closest to a set of coordinates
Input: float latitude, float longitude, array of road segments
Returns array of road segments
'''
def getImmediateSegments(latIn, longIn, roadSegmentArray):
    immediateSegments = []
    minDistance = sys.float_info.max
    for segment in roadSegmentArray:
        distance1 = geopy.distance.distance((latIn, longIn), (segment[2], segment[3])).km
        if distance1 < minDistance:
            minDistance = distance1
            immediateSegments = []
            immediateSegments.append(segment)
        elif distance1 == minDistance:
            immediateSegments.append(segment)
    return immediateSegments

'''
Return an array of road segments with names matching a given address
Input : address string, array of road segments
Returns an array of road segments
'''
def filterNames(address,roadSegmentArray):
    # split address string into workable array
    x = address.split()
    # ignore address housenumber
    y = x[1:len(x)]
    expandAbbrv(y)
    # transform split address back into string
    poiStreet = " ".join(str(z) for z in y)
    filteredArr = []
    for segment in roadSegmentArray:
        s = SequenceMatcher(None, segment[7], poiStreet)
        if s.ratio() > MATCH_RATIO:
            filteredArr.append(segment)
    return filteredArr


'''
Input : float latitude, float longitude, string address
returns the closest road segment to a given lat/long coordinate.
 return value is of of the same form as a line in roadSegmentsXXX.csv
    [startid, endid, lat1, lon1, lat2, lon2, distance, name]
'''
def getClosestSegment(latIn, longIn, address):
    # filter using name matching and then getting immediateSegments
    filteredArr = filterNames(address, roadSegments)
    arr = getImmediateSegments(latIn, longIn, filteredArr)
    # if name matching fails, only used immediateSegments
    if len(arr) == 0:
        arr = getImmediateSegments(latIn, longIn, roadSegments)
    # find closest segment out of filtered segments
    closestSegment = None
    for segment in arr:
        distance = geopy.distance.distance((latIn, longIn), (segment[3], segment[4])).km
        if distance < segment[5]:
            return segment
    return arr[0]

'''
Write a response to file
Input : yelpfusion response, string file
No return value, writes output to file
'''
def writeResponse(response, file):
    business_data = response.json()
    # write in form address, lat, long, rating
    for biz in business_data['businesses']:
        print(biz)
        address = biz['location']['address1']
        latitude = biz['coordinates']['latitude']
        longitude = biz['coordinates']['longitude']
        rating = biz['rating']
        # sometimes businesses are missing specific info we need, so
        # we check that it has all the necessary information
        if all (k is not None for k in (latitude, longitude, address, rating)):
            # what road segment is the poi on
            segment = getClosestSegment(latitude, longitude, address)
            row =\
                address.replace(',', '') + "," +\
                str(latitude) + "," +\
                str(longitude) + "," +\
                str(rating) + "," +\
                str(segment[0]) + "," +\
                str(segment[1]) + "\n"
            # yelp's api is sometimes innacurate, returning values outside the specified location
            # for this reason we double check if a location is within our bounding box
            if withinBoundBox(latitude, longitude):
                file.write(row)


'''
Per the yelp FAQ, 'The API can only return up to 1,000 results at this time'
To get around this, we query a category until it reaches the max results, sleep
a bit, then move on to the next category
'''
writeFile = open(ouputFile, 'w')
for category in CATEGORIES_LESS:
    OFFSET=0
    for i in range(RANGE):
        # Define the parameter API call
        PARAMETER  = {'categories' : category,
                     'limit' : LIMIT,
                     'offset' : OFFSET,
                     'location' : location}
        # API Call
        response = requests.get(url=ENDPOINT, params = PARAMETER, headers = HEADERS)
        # if response is ok proceed writing to file
        if response.status_code == 200:
            writeResponse(response, writeFile)
            # set offset for next API call
            OFFSET += LIMIT+1
        # if response is bad, we've probably reached the last page of results and should break
        elif response.status_code == 400:
            print('Reached max for category {}'.format(category))
            print('Sleeping for {} seconds'.format(SLEEP))
            time.sleep(SLEEP)
            break
writeFile.close()
