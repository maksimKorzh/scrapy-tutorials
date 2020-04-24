# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib


# scraper class
class Colleges(scrapy.Spider):
    # scraper name
    name = 'colleges'
    
    # base URL
    base_url = 'https://www.niche.com/colleges/search/all-colleges/?'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {     
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'colleges.csv',
           
        # enable the middleware
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},

        # enable crawlera
        'CRAWLERA_ENABLED': True,

        # the APIkey you get with your subscription
        'CRAWLERA_APIKEY': 'your_api_key'
    }
    
    # proxies
    proxies = []
    current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        
        for page in range(1, 254):
            try:
                # next page
                next_page = self.base_url + urllib.parse.urlencode({'page': str(page)})

                #print(next_proxy)
                yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)

            except Exception as e:
                print(e)
    
    # parse response
    def parse(self, res):
        # loop over college cards
        for card in res.css('li.search-results__list__item'):
            # extract data
            features = {
                'name': card.css('h2.search-result__title::text')
                            .get(),
                
                'type': card.css('li.search-result-tagline__item::text')
                            .get(),
                
                'location': card.css('li.search-result-tagline__item::text')
                                .getall()[2],
                
                'website': card.css('a.search-result__link::attr(href)')
                               .get(),
                
                #'feedback': ' '.join(card.css('p.search-result-feature *::text')
                #                        .getall())
            }
            
            # print extracted data
            #print(json.dumps(features, indent=2))
    
            # store output
            yield features

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Colleges)
    process.start()
    
    
    
    
    
    
    
    
    
    
    
