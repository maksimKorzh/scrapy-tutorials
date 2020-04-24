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
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 4,
        'DOWNLOAD_TIMEOUT': 10,        
    }
    
    # proxies
    proxies = []
    current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):
        # make HTTP request to get free proxies
        proxy_res = requests.get('https://free-proxy-list.net')
        
        # init scrapy selector
        response = Selector(text=proxy_res.text)
        
        # extract proxies
        table = response.css('table')
        rows = table.css('tr')
        cols = [row.css('td::text').getall() for row in rows]
        
        # init proxies
        for col in cols:
            if col and col[4] == 'elite proxy' and col[6] == 'yes':
                self.proxies.append('https://' + col[0] + ':' + col[1])
        
        # crawl pages        
        for page in range(1, 254):
            try:
                # next page
                next_page = self.base_url + urllib.parse.urlencode({'page': str(page)})
                
                # rotate proxy
                next_proxy = self.proxies[self.current_proxy]

                #print(next_proxy)
                yield scrapy.Request(url=next_page, headers=self.headers, meta={'proxy': next_proxy}, callback=self.parse)

            except Exception as e:
                print(e)
                print('EXCEPTION')
    
    # parse response
    def parse(self, res):
        # rotate proxy every 5 requests
        self.current_proxy += 1
        print('CURENT PROXY:', self.proxies[self.current_proxy], '\n\n')
        
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
    
    
    
    
    
    
    
    
    
    
    
