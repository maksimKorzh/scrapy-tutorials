##############################################################
#
# Script to scrape location ID and area ID from willhaben.at
#                         
#                             by
#
#                      Code Monkey King
#
##############################################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import json

# willhaben location IP class
class WillhabenLocation(scrapy.Spider):
    # scraper/ spider name
    name = 'willhaben'
    
    # base URL
    base_url = 'https://autocomplete.willhaben.at/autocomplete/location?'
    
    # string query parameters
    params = {
        'source': 'desktop',
        'term': ''
    }
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'postcodes.json'
    }
    
    # postcodes list
    postcodes = []
    
    # init class constructor
    def __init__(self):
        # postcodes content
        content = ''
    
        # open postcodes file
        with open('austrian_postcodes.txt', 'r') as f:
            for line in f.read():
                content += line
        
        # init postcodes
        self.postcodes = list(filter(None, content.split('\n')))
    
    # crawler's entry point
    def start_requests(self):
        # loop over postcodes
        for postcode in self.postcodes:
            # init string query paramaters
            self.params['term'] = postcode
            
            # generate next postcode url
            next_postcode = self.base_url + urllib.parse.urlencode(self.params)
            
            # crawl next postcode url
            yield scrapy.Request(
                url=next_postcode,
                headers=self.headers,
                callback=self.parse
            )
    
    # parse response
    def parse(self, response):
        # parse response
        data = json.loads(response.text)
        
        # extract location ID data
        locations = data[0]['entries']
        
        # loop over locations
        for location in locations:
            # write location to output JSON file
            yield location
    
    
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(WillhabenLocation)
    process.start()  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
