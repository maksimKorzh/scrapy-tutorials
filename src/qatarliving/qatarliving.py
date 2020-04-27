# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

# scraper class
class QatarLiving(scrapy.Spider):
    # scraper name
    name = 'qatarliving'
    
    # base_url
    base_url = 'https://www.qatarliving.com/classifieds/properties/apartment?'
    
    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'qatarliving.csv',
        # uncomment below to slow down the crawling
        # to fit site's "robots.txt" file requirements
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        #'DOWNLOAD_DELAY': 10
    }
    
    # crawler's entry point
    def start_requests(self):
        # loop over page range
        for page in range(0, 112):
            # generate next page URL
            next_page = self.base_url + urllib.parse.urlencode({'page': str(page)})
            
            # crawl next page URL
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
    
    # parse response
    def parse(self, res):
        '''
        # store response to local HTML file
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # read local HTML file
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        res = Selector(text=content)
        '''
        
        # loop over property cards
        for card in res.css('span[class="b-card b-card-mod-h property"]'):
            # data extraction logic
            features = {
                'type': card.css('p[class="b-ad-excerpt b-par-mod-clear b-line-mod-thin--mix-property"]::text')
                            .get()
                            .split(', ')[0],
                
                'price': ' '.join(card.css('div[class="b-card--el-price-conditions "] *::text')
                                      .getall())
                                      .replace('\n', '')
                                      .strip(),
                
                'address': card.css('p[class="b-ad-excerpt b-par-mod-clear b-line-mod-thin--mix-property"]::text')
                              .get()
                              .split(', ')[-1],
                
                'description': ''.join(card.css('p[class="b-card--el-description"] *::text')
                                           .getall()),
                                           
                'bedrooms': card.css('div[class="b-feature bedroom bedroom-mod-small"]')
                                .css('p[class="b-feature--el-value b-par-mod-clear b-line-mod-thin b-caption-name"]::text')
                                .get(),
                
                'bathrooms': card.css('div[class="b-feature bathroom bathroom-mod-small"]')
                                 .css('p[class="b-feature--el-value b-par-mod-clear b-line-mod-thin b-caption-name"]::text')
                                 .get(),
                
                'agency_name': card.css('div[class="b-card--el-agency"]')
                                   .css('a')
                                   .css('a::text')
                                   .get(),
                
                'agency_link': 'https://www.qatarliving.com' + 
                               str(card.css('div[class="b-card--el-agency"]')
                                       .css('a')
                                       .css('a::attr(href)')
                                       .get()),
                
                'image_url': card.css('div[class="b-card--el-header"]')
                                 .css('img::attr(src)')
                                 .get()
                
            }
            
            # store output to CSV
            yield features

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(QatarLiving)
    process.start()
    
    # debug data extraction logic
    #QatarLiving.parse(QatarLiving, '')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
