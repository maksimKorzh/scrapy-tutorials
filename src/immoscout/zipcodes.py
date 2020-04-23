# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import json

# zipcodes scraper class
class Zipcodes(scrapy.Spider):
    # scraper/spider name
    name = 'immoscout'
    
    # base url
    base_url = 'https://rest-api.immoscout24.ch/v4/en/locations?'
    
    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'zipcodes.json'
    }
    
    # crawler's entry point
    def start_requests(self):
        # zipcodes list
        zipcodes = ''
        
        # open "zipcodes.txt" file
        with open('zipcodes.txt', 'r') as f:
            for line in f.read():
                zipcodes += line
        
        # init zipcodes
        zipcodes = zipcodes.split('\n')
        
        # loop over zipcodes
        for zipcode in zipcodes:
            url = self.base_url + urllib.parse.urlencode({'term': str(zipcode)})
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
    
    # parse HTTP response
    def parse(self, res):
        try:
            # init response data as python dictionary type
            data = json.loads(res.text)
            label = 'postcode-' + data[0]['label'].replace(' ', '-').lower()
            
            # store label
            with open('label.txt', 'a') as f:
                f.write(label + '\n')
            
            # store json response
            yield data[0]

        except:
            pass

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Zipcodes)
    process.start()
