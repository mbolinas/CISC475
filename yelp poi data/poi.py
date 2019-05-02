"""
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

#Define the parameter for the first 50 samples
PARAMETER  = {'term' : 'dinner',
             'limit' : 50,
             'offset' :OFFSET,
             'radius' : 10000,
             'location' : 'Manhattan,NY'}


#Make a request to the yelp API for first call
response = requests.get(url=ENDPOINT, params = PARAMETER, headers = HEADERS)


#convert the JSON string to a Dictionary
business_data = response.json()

    
#this is used to print appropraite data
"""for biz in business_data['businesses']:
    #print(biz)
    print("loation:",biz['location']['address1'],"latitude:",biz['coordinates']['latitude'],"longitude:",biz['coordinates']['longitude'],"rating:", biz['rating'])"""


'''Next section is going to print the data into a csv file. '''

download_dir = "yelp_extend.csv" 
#where you want the file to be downloaded to 

csv = open(download_dir, "w") 
#"w" indicates that you're writing strings to the file

columnTitleRow = "address,latitude,longitude, rating, price(1 is cheapest)\n"
csv.write(columnTitleRow)

with open(download_dir, 'w') as writeFile:
    for biz in business_data['businesses']:
        address = biz['location']['address1']
        latitude = biz['coordinates']['latitude']
        longitude = biz['coordinates']['longitude']
        rating = biz['rating']
        if "price" not in biz:
                price = "NA"
        else: 
                price = biz['price'].count('$')          
        row = address + "," + str(latitude) + "," + str(longitude) + "," + str(rating)+ "," + str(price)+"\n"
        writeFile.write(row)


for i in range(RANGE):
    OFFSET +=50
    with open(download_dir, 'a') as addFile:
        for biz in business_data['businesses']:
            address = biz['location']['address1']
            latitude = biz['coordinates']['latitude']
            longitude = biz['coordinates']['longitude']
            rating = biz['rating']
            if "price" not in biz:
                    price = "NA"
            else: 
                    price = biz['price'].count('$')              
            row = address + "," + str(latitude) + "," + str(longitude) + "," + str(rating)+ "," + str(price)+"\n"
            addFile.write(row)    



