"""
Adapted from Muhan's auto_csv.py code

This python file write the data into a csv file using a automatic way
The file will have 50*(1+RANGE) samples.
The file generate 10000 samples.
If we want to query 500 samples, set RANGE=9, for example.
"""
import csv
import argparse
import json
import pprint
import requests
import sys
import urllib
import geopy.distance
import time

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
SLEEP = 20 # how long to sleep between categories

#Define the API Key, define the endpoint and define the header
API_KEY = 'pdXJAlG5dNPgd3oqnypNJr1T7jihvqBzsrRMWPheuxR8IdN1CllWkLXaf0I6Y43igep_58Np2VFBQRwWEDCLYY_KnGZNfpKS8TeIYgV6wFX25xZVcx-LTbth9HyIXHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization' : 'Bearer %s' % API_KEY}

bBoxFile = open('boundingBoxes.txt', "r")
lines = bBoxFile.readlines()
# Bounding box used for computation. Set in boundingBoxes.txt
boundBox = lines[0].replace('(','').replace(')','').rstrip('\n').split(',') # lol i'll fix later
# Output filename. Set in boundingBoxes.txt
ouputFile = './generated_map_data/poiYelp{}.csv'.format(lines[1].rstrip('\n'))
# Location used for computation. Set in boundingBoxes.txt
location = lines[2].rstrip('\n')
bBoxFile.close()

#print(boundBox)
#print(location)

'''
Check if given coordinates are within the bounding box
'''
def withinBoundBox(lat, lon):
    a = lat > float(boundBox[0])
    b = lat < float(boundBox[2])
    c = lon > float(boundBox[1])
    d = lon < float(boundBox[3])
    return a and b and c and d

'''
Write a response to file
'''
def writeResponse(business_data, file):
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
            row =\
                address.replace(',', '') + "," +\
                str(latitude) + "," +\
                str(longitude) + "," +\
                str(rating)+"\n"
            # yelp's api is sometimes innacurate, returning values outside the specified location
            # for this reason we double check if a location is within our bounding box
            if withinBoundBox(latitude, longitude):
                file.write(row)

'''
Per the yelp FAQ, 'The API can only return up to 1,000 results at this time'
To get around this, we query a category until it reaches the max results, sleep
a bit, then move on to the next category
'''
with open(ouputFile, 'w') as writeFile:
    for category in CATEGORIES:
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
                business_data = response.json()
                writeResponse(business_data, writeFile)
                # set offset for next API call
                OFFSET += LIMIT+1
            # if response is bad, we've probably reached the last page of results and should break
            elif response.status_code == 400:
                print('End of category {}'.format(category))
                print('Sleeping for {} seconds'.format(SLEEP))
                time.sleep(SLEEP)
                break
