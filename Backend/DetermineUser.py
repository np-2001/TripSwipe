import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.parse import quote
import pprint


YELP_API_KEY= "RytzLV4FkRl2FcHDc9nGBYu8ZbQBXneST-ddi-U6EUUwpe_9bEEyx_IzUzZPShmOcUGrOwPK5YEW9ZVIMxnl71jEsVFqApqRzn7uXV5l5xau_2_jY_c88_85q6MaZnYx"

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

DEFAULT_TERM = 'dinner'
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

        return response.json()

    def categorizeActivity(self):
        '''
        Categorizes activity
        '''
        pass

    def addToJSON(self):
        '''
        Following activity categorization and swipe, add to JSON with user preference
        '''
        pass

    
def main():
    user = DetermineUser()
    pprint.pprint(user.recieveActivity())

if __name__ == '__main__':
    main()