# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

# scraper calss definition
class SlickDeals(scrapy.Spider):
    # spider name
    name = 'slickdeals'
    
    # base URL
    base_url = 'https://slickdeals.net/computer-deals/?'
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'slickdeals.csv'
    }
    
    # crawler's entry point
    def start_requests(self):
        # loop over page range
        # alter page range accordignly, e.g.
        # (1, 10) or whatever available range
        for page in range(1, 8):
            url = self.base_url + urllib.parse.urlencode({'page': page})
            yield scrapy.Request(url=url, callback=self.parse)
            #break
    
    # parse content
    def parse(self, res):
        '''
        # store response to HTML
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        
        '''
        # init content
        content = ''
        
        # load and parse HTML response
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # fake response object selector
        res = Selector(text=content)
        '''
        
        # loop over product cards
        for card in res.css('ul.categoryGridDeals').css('li.fpGridBox'):
            items = {
                'title': card.css('a.bp-c-link::text')
                             .get(),
                
                'link': 'https://slickdeals.net' + 
                         card.css('a.bp-c-link::attr(href)')
                             .get(),
                
                'price': '',
                
                'likes': card.css('span.likesLabel')
                            .css('span.count::text')
                            .get()
            }
            
            # try to extract price
            try:
                items['price'] = card.css('div.itemPrice::text').get().replace('\n', '').strip()
            except Exception as e:
                #print(e)
                items['price'] = 'N/A'

            
            # store output results
            yield items
            
            # print results
            #print(json.dumps(items, indent=2))
        
        
            
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(SlickDeals)
    process.start()
    
    # debug selectors
    #SlickDeals.parse(SlickDeals, '')
    
    
    
