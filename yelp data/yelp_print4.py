"""
This python file simply print the data when you run it
"""


import argparse
import json
import pprint
import requests
import sys
import urllib

OFFSET=0

#Define the API Key, define the endpoint and define the header
API_KEY = 'pdXJAlG5dNPgd3oqnypNJr1T7jihvqBzsrRMWPheuxR8IdN1CllWkLXaf0I6Y43igep_58Np2VFBQRwWEDCLYY_KnGZNfpKS8TeIYgV6wFX25xZVcx-LTbth9HyIXHYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization' : 'Bearer %s' % API_KEY}



#Define the parameter for every 50 sample after that
PARAMETER  = {'term' : 'dinner',
             'limit' : 50,
             'offset' :OFFSET,
             'radius' : 10000,
             'location' : 'Newark,DE'}

#Make a request to the yelp API for first call
response = requests.get(url=ENDPOINT, params = PARAMETER, headers = HEADERS)


#convert the JSON string to a Dictionary
business_data = response.json()


#used to print keys 
print(business_data.keys())


"""for biz in business_data['businesses']:
    print(biz)"""

    

#for biz in business_data['businesses']:
    #print(biz)
    #print("loation:",biz['location']['address1'],"latitude:",biz['coordinates']['latitude'],"longitude:",biz['coordinates']['longitude'],"rating:", biz['rating'])
    

for biz in business_data['businesses']:
    print("loation:",biz['location']['address1'],"latitude:",biz['coordinates']['latitude'],"longitude:",biz['coordinates']['longitude'],"rating:", biz['rating'])
