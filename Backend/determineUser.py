import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.parse import quote
import pprint
import random
import requests
import json

from dotenv import load_dotenv
import os

# Load the environment file
load_dotenv('secrets.env')

# Retrieve the API key
YELP_API_KEY = os.getenv('YELP_API_KEY')


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

terms = ['outdoor', 'exercise', 'relax', 'hiking', 'tourist attractions', 'popular dinner', 'popular lunch', 'popular breakfast', 'popular attractions', 'hidden gems', 'nature', 'garden', 'water', 'shopping', 'learning', 'kid friendly', 'nightlife', 'bars', 'sports', 'Landmarks & Historical Buildings']
locations = ['Cancun, Mexico', 'Tokyo, Japan', 'Paris, France', 'Barcelona, Spain', 'New York City, New York', 'Los Angeles, California', 'Rio, Brazil', 'Zurich, Switzerland', 'Miami, Florida']
SEARCH_LIMIT = 1


class TravelAttractionData:
    def __init__(self):
        self.toJSON = {}
        self.categories = []

    def recieveActivity(self):
        '''
        Generate activity from Yelp API
        '''
        url_params = {
            'term': random.choice(terms).replace(' ', '+'),
            'location': random.choice(locations).replace(' ', '+'),
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
        self.categories = []
        for i in self.toJSON["businesses"][0]["categories"]:
            self.categories.append(i["title"])

        return self.categories

class Swipe:
    def __init__(self, TravelAttractionData):
        self.touristAttraction = TravelAttractionData
        self.json = {}
    
    def newAttraction(self):
        self.touristAttraction = TravelAttractionData()
        self.touristAttraction.recieveActivity()

    def swipe(self, yes):
        '''
        Functionality for direction swiped by user
        '''
        self.touristAttraction.categorizeActivity()

        if yes:
            for i in self.touristAttraction.categories:
                self.json[i] = True
        else:
            for i in self.touristAttraction.categories:
                self.json[i] = False
    
def main():
    user = TravelAttractionData()
    user.recieveActivity()
    swipe = Swipe(user)
    swipe.swipe(True)

    swipe.newAttraction()
    swipe.swipe(True)

    swipe.newAttraction()
    swipe.swipe(True)

    swipe.newAttraction()
    swipe.swipe(True)
    
     # Convert dictionary to JSON format
    json_data = json.dumps(swipe.json)

    print(json_data)
    
    # Make a GET request with the JSON data as parameters
    response = requests.get('http://localhost:5000/generate-locations', params={'data': json_data})
    
    # Print the response from the server
    print(response.text)
    



if __name__ == '__main__':
    main()