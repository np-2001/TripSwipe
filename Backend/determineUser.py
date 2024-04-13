import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.parse import quote
import pprint

from dotenv import load_dotenv
import os

# Load the environment file
load_dotenv('secrets.env')

# Retrieve the API key
YELP_API_KEY = os.getenv('YELP_API_KEY')


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

DEFAULT_TERM = 'tourist attractions'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3


class DetermineUser:
    def __init__(self):
        toJSON = {}

    def swipe(self, yes):
        '''
        Used to determine if user likes activity
        '''
        pass

    def recieveActivity(self):
        '''
        Generate activity from Yelp API
        '''
        url_params = {
            'term': DEFAULT_TERM .replace(' ', '+'),
            'location': DEFAULT_LOCATION.replace(' ', '+'),
            'limit': SEARCH_LIMIT
        }
        url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))

        headers = {
            'Authorization': 'Bearer %s' % YELP_API_KEY,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)

        self.toJSON = response.json()

        return response.json()

    def categorizeActivity(self):
        '''
        Categorizes activity
        '''
        pprint.pprint(self.toJSON)

    def addToJSON(self):
        '''
        Following activity categorization and swipe, add to JSON with user preference
        '''
        pass

    
def main():
    user = DetermineUser()
    user.recieveActivity()

    user.categorizeActivity()

if __name__ == '__main__':
    main()