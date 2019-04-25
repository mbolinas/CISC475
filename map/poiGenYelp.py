"""
Adapted from Muhan's code

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

RANGE = 17 # how many pages to get
LIMIT = 50 # number of results from a single call; max 50,min 20

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

print(boundBox)
print(location)

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
Writing to CSV
'''
with open(ouputFile, 'w') as writeFile:
    OFFSET=1
    for i in range(RANGE):
        # Define the parameter for the first LIMIT samples
        PARAMETER  = {'term' : 'restaurants',
                     'limit' : LIMIT,
                     'offset' : OFFSET,
                     'location' : location}
        # API Call
        response = requests.get(url=ENDPOINT, params = PARAMETER, headers = HEADERS)
        # store response
        business_data = response.json()
        # write in form address, lat, long, rating
        for biz in business_data['businesses']:
            address = biz['location']['address1']
            latitude = biz['coordinates']['latitude']
            longitude = biz['coordinates']['longitude']
            rating = biz['rating']
            row = address + "," + str(latitude) + "," + str(longitude) + "," + str(rating)+"\n"
            # yelp's api is sometimes innacurate, returning values outside the specified location
            # for this reason we double check if a location is within our bounding box
            if withinBoundBox(latitude, longitude):
                writeFile.write(row)
        # set offset for next API call
        OFFSET += LIMIT
