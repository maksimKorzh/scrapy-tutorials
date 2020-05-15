##########################################################
#
# Script to scrape Austrian real estate properties data
#                   from willhabe.at
#
#                          by
#
#                   Code Monkey King
#
##########################################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json
import csv

# willhaben scraper class
class WillhabenScraper(scrapy.Spider):
    # scraper / spider name
    name = 'willhaben'
    
    # base URL
    base_url = 'https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?'
    
    # string query parameters
    params = {
        'areaId': '',
        'parent_areaid': '',
        'page': 1
    }

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 1
    }

    # current page counter
    current_page = 1
    
    # postcodes
    postcodes = []
    
    # init constructor
    def __init__(self):
        # postcodes content
        content = ''
        
        # open "postcodes.json" file
        with open('postcodes.json', 'r') as f:
            for line in f.read():
                content += line
        
        # parse postcodes
        self.postcodes = json.loads(content)
        
        # init CSV output file
        with open('willhaben.csv', 'w') as f:
            f.write(','.join([
                'title',
                'price',
                'floor_area',
                'location',
                'agency',
                'image_url']
            ) + '\n')
    
    # crawler's entry point
    def start_requests(self):
        # loop over postcodes
        for postcode in self.postcodes:
            # postcodes counter
            count = 1
            
            # reset current page counter
            self.current_page = 1
            
            # init string query parameters
            self.params['areaId'] = postcode['areaId']
            self.params['parent_areaid'] = postcode['provinceAreaId']
            
            # generate next postcode URL
            next_postcode = self.base_url + urllib.parse.urlencode(self.params)
            
            # crawl next postcode URL
            yield scrapy.Request(
                url=next_postcode,
                headers=self.headers,
                meta = {
                    'postcode': postcode['label'],
                    'count': count
                },
                callback=self.parse_cards
            )
            
            # increment postcodes counter
            count += 1
    
    # parse property cards
    def parse_cards(self, response):
        # extract meta data
        postcode = response.meta.get('postcode')
        count = response.meta.get('count')
        
        '''
        # store response locally as HTML file
        with open('response.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local response content
        content = ''
        
        # load local HTML file
        with open('response.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector manually
        response = Selector(text=content)
        '''
        
        # print debug info
        print('Postcode %s: %s out of %s postcodes' % (postcode, count, len(self.postcodes)))
        
        # feature list
        features = []
        
        # loop over property cards
        for card in response.css('article[class="search-result-entry  "]'):
            # property card features
            feature = {
                'title': card.css('span[itemprop="name"]::text')
                             .get()
                             .replace('\n', '')
                             .strip(),
                
                'price': card.css('p[class="tp-info-3"]::text')
                             .get(),
                
                'floor_area': card.css('span[class="desc-left"]::text')
                                  .get()
                                  .replace('\n', '')
                                  .strip(),
                
                'location': card.css('div[class="address-lg w-brk-ln-1 "]::text')
                               .get()
                               .replace('\n', '')
                               .strip()
                               .replace('               ', ''),
                
                'agency': '',
                
                'image_url': card.css('img[itemprop="image"]::attr(src)')
                                 .get()
            }
            
            # extract agency name
            try:
                feature['agency'] = card.css('span[class="organisationName"]::text')
                feature['agency'] = feature['agency'].get()
                feature['agency'] = feature['agency'].replace('\n', '').strip()
            
            except:
                pass
            
            # append feature to feature list
            features.append(feature)
        
        # extract JSON data from script tag
        script = [
            script.get() for script in
            response.css('script')
            if 'var tmsJson = ' in script.get()
        ]
        
        # extract JSON part of the script
        json_data = script[0].split('var tmsJson = ')[-1].split('}};')[0] + '}}'
        
        # parse JSON data
        json_data = json.loads(json_data)
        
        # parse search results
        json_data['tmsData']['search_results'] = urllib.parse.unquote(json_data['tmsData']['search_results'])
        
        # parse search results
        search_results = json.loads(json_data['tmsData']['search_results'])
        
        # loop over card indexes
        for index in range(0, len(features)):
            try:
                features[index]['price'] = search_results[index + 1]['price']

                with open('willhaben.csv', 'a') as f:
                    # create CSV dictionary writer
                    writer = csv.DictWriter(f, fieldnames=features[index].keys())
                    
                    # write CSV row
                    writer.writerow(features[index])
            except:
                pass

        # handle pagination crawling
        try:
            # extract search results number
            found_results = int(response.css('span[id="search-count"]::text').get().replace('.', ''))
            
            # calculate total pages to crawl number
            total_pages = int(found_results / 24) + 1
            
            # increment curent page counter
            self.current_page += 1
            
            # init string query parameters
            self.params['page'] = self.current_page
            
            # generate next page URL
            next_page = self.base_url + urllib.parse.urlencode(self.params)
            
            # check if next page is available
            if self.current_page <= total_pages:
                # print debug info
                print('PAGE %s out of %s pages' % (self.current_page, total_pages))
                
                # crawl next page URL
                yield response.follow(
                    url=next_page,
                    headers=self.headers,
                    meta = {
                        'postcode': postcode,
                        'count': count
                    },
                    callback=self.parse_cards
                )

        except:
            pass

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(WillhabenScraper)
    process.start()
    
    # debug data extraction logic
    #WillhabenScraper.parse_cards(WillhabenScraper, '')














