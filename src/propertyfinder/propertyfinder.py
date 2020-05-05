# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

# property finder scraper class
class PropertyFinder(scrapy.Spider):
    # scraper name
    name = 'propertyfinder'
    
    # base URL
    base_url = 'https://www.propertyfinder.bh/en/search?'
    
    # string query parameters
    params = {
        'c': 1,
        'ob': 'mr',
        'page': ''
    }
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'propertyfinder.csv'
    }
    
    # craler's entry
    def start_requests(self):
        # crawl pages
        for page in range(1, 10):   # crawl 10 pages, change "10" to whatever page naumber to crawl
            # increment current page to crawl
            self.params['page'] = str(page)
            
            # generate next page URL
            next_page = self.base_url + urllib.parse.urlencode(self.params)
            
            # crawl next page URL
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
    
    # parse respone
    def parse(self, res):
        '''
        # store HTML response to the local file
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # load local HTML file
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        res = Selector(text=content)
        '''
        
        # loop over property cards
        for card in res.css('div[class="card-list__item"]'):
            # extract features
            features = {
                'title': card.css('h2[class="card__title card__title-link"]::text')
                             .get(),

                'listing_url': 'https://www.propertyfinder.bh' + card.css('a[class="card card--clickable"]::attr(href)')
                                                                     .get(),
                
                'address': card.css('p[class="card__location"]::text')
                               .get(),
                
                'price': card.css('span[class="card__price-value"]::text')
                             .get()
                             .replace('\n', '')
                             .strip() + ' BHD',
                
                'type': card.css('p[class="card__property-amenity card__property-amenity--property-type"]::text')
                            .get(),
                
                'bedrooms': '',
                
                'bathrooms': '',
                
                'floor_area': card.css('p[class="card__property-amenity card__property-amenity--area"]::text')
                                  .get(),
                
                'telephone': '',
                
                'latitude': '',
                
                'longitude': ''
                             
            }
            
            # try to extract bedrooms
            try:
                bedrooms = card.css('p[class="card__property-amenity card__property-amenity--bedrooms"]::text')
                bedrooms = bedrooms.get().strip()
                
                features['bedrooms'] = bedrooms
            
            except:
                features['bedrooms'] = 'N/A'

            # try to extract bathrooms
            try:
                bathrooms = card.css('p[class="card__property-amenity card__property-amenity--bathrooms"]::text')
                bathrooms = bathrooms.get().strip()
                
                features['bathrooms'] = bathrooms
            
            except:
                features['bathrooms'] = 'N/A'

            
            # extract additional data script
            try:
                script = json.loads(res.css('script[type="application/ld+json"]::text').get())

            except Exception as e:
                print(e)
            
            # try to extract phone number
            try:
                # loop over cards' JSON data
                for card in script[0]['itemListElement']:
                    if features['listing_url'] == card['url']:
                        features['telephone'] = card['mainEntity']['telephone']

            except Exception as e:
                print(e)
            
            # try to extract geo coordinates
            try:
                # loop over cards' JSON data
                for card in script[0]['itemListElement']:
                    if features['listing_url'] == card['url']:
                        features['latitude'] = card['mainEntity']['geo']['latitude']
                        features['longitude'] = card['mainEntity']['geo']['longitude']
            except:
                pass
            
            # fix 'N/A' vaules for phones
            if features['telephone'] == '':
                features['telephone'] = 'N/A'

            # fix 'N/A' vaules for coordinates
            if features['latitude'] == '':
                print('N/A')
                features['latitude'] = 'N/A'
                features['longitude'] = 'N/A'

            # store output to CSV
            yield features
        
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(PropertyFinder)
    process.start()
    
    # fake HTTP response
    #PropertyFinder.parse(PropertyFinder, '')














