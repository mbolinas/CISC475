"""
Mostly Muhan's code. Adapted in a couple ways.

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

#define the variables
OFFSET=0
RANGE=199

#Define the API Key, define the endpoint and define the header
API_KEY = 'pdXJAlG5dNPgd3oqnypNJr1T7jihvqBzsrRMWPheuxR8IdN1CllWkLXaf0I6Y43igep_58Np2VFBQRwWEDCLYY_KnGZNfpKS8TeIYgV6wFX25xZVcx-LTbth9HyIXHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization' : 'Bearer %s' % API_KEY}

bBoxFile = open('boundingBoxes.txt', "r")
lines = bBoxFile.readlines()
# Output filename. Set in boundingBoxes.txt
download_dir = './generated_map_data/poiYelp{}.csv'.format(lines[1].rstrip('\n'))
# Location used for computation. Set in boundingBoxes.txt
location = lines[2].rstrip('\n')
bBoxFile.close()

#Define the parameter for the first 50 samples
PARAMETER  = {'term' : 'dinner',
             'limit' : 50,
             'offset' :OFFSET,
             'radius' : 10000,
             'location' : location}


#Make a request to the yelp API for first call
response = requests.get(url=ENDPOINT, params = PARAMETER, headers = HEADERS)


#convert the JSON string to a Dictionary
business_data = response.json()


#this is used to print appropraite data
"""for biz in business_data['businesses']:
    #print(biz)
    print("loation:",biz['location']['address1'],"latitude:",biz['coordinates']['latitude'],"longitude:",biz['coordinates']['longitude'],"rating:", biz['rating'])"""


'''Next section is going to print the data into a csv file. '''

csv = open(download_dir, "w")

#columnTitleRow = "address,latitude,longitude, rating\n"
#csv.write(columnTitleRow)

with open(download_dir, 'w') as writeFile:
    for biz in business_data['businesses']:
        address = biz['location']['address1']
        latitude = biz['coordinates']['latitude']
        longitude = biz['coordinates']['longitude']
        rating = biz['rating']
        row = address + "," + str(latitude) + "," + str(longitude) + "," + str(rating)+"\n"
        writeFile.write(row)


for i in range(RANGE):
    OFFSET +=50
    with open(download_dir, 'a') as addFile:
        for biz in business_data['businesses']:
            address = biz['location']['address1']
            latitude = biz['coordinates']['latitude']
            longitude = biz['coordinates']['longitude']
            rating = biz['rating']
            row = address + "," + str(latitude) + "," + str(longitude) + "," + str(rating)+"\n"
            addFile.write(row)
