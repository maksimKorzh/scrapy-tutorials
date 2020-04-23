# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

# scraper class
class Immoscout(scrapy.Spider):
    # scraper/spider name
    name = 'immoscout'
    
    # base URL
    base_url = 'https://www.immoscout24.ch/en/real-estate/rent/'
    
    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # string query parameters
    params = {
        'pn': '',
        'r': 0
    }
    
    # current page crawled
    current_page = 1
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'immoscout.csv'
    }
    
    # crawler's entry
    def start_requests(self):
        # zipcodes
        zipcodes = ''
        
        # open "label.txt" file
        with open('label.txt', 'r') as f:
            for line in f.read():
                zipcodes += line
        
        # init zipcodes
        zipcodes = zipcodes.split('\n')
        
        # init zipcodes count
        count = 1
        
        # loop over zipcodes
        for zipcode in zipcodes:
            # reset current_page
            self.current_page = 1
        
            # init string query params
            self.params['pn'] = self.current_page
            
            # generate zipcode URL to crawl
            url = self.base_url + zipcode + '?' + urllib.parse.urlencode(self.params)
            
            # crawl given zipcode
            yield scrapy.Request(url=url, headers=self.headers, meta={'zipcode': count, 'total': len(zipcodes)}, callback=self.parse)
            
            # increment ziocodes count
            count += 1
    
    # parse content
    def parse(self, res):
        '''
        # store HTML response to debug selectors
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        '''
        # local HTML content
        content = ''
        
        # load HTML response from local file to debug selectors
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        res = Selector(text=content)
        '''
        
        # extact data from meta container
        count = res.meta.get('zipcode')
        total = res.meta.get('total')

        # loop over property cards
        for card in res.css('div[class="sc-18zf79l-0 cpuXZS"]'):
            # property features
            features = {
                'title': card.css('h2[class="bkivry-0 csYOrJ qjwil1-6 iCnXmG"]::text')
                             .getall()[1],
                
                'details': ''.join(card.css('h3[class="bkivry-0 kXCbXB qjwil1-5 iCnXmF"] *::text')
                                       .getall()),
                
                'address': card.css('div[class="qjwil1-7 iCnXmH"]')
                               .css('a[class="bkivry-0 sc-1u0if05-0 eKnuaM"] *::text')
                               .get(),
                
                'price': card.css('h3[class="bkivry-0 eDrwLl"]::text')
                             .get(),
                
                'image': card.css('div[class="r5r22j-0 loCtpM swiper-slide"]')
                             .css('img::attr(src)')
                             .get()
            }
            
            # print extracted data
            #print(json.dumps(features, indent=2))
            
            # store output to CSV
            yield features
            
        # crawl pages if available
        try:
            try:
                # increment current page by 1
                self.current_page += 1
                
                # extract number of total pages
                total_pages = max([int(page) for page in res.css('div[class="bkivry-0 sc-AykKC kHMyVR"] *::text').getall() if page.isdigit()])
            except:
                total_pages = 1
                self.current_page -= 1
            
            # increment page number string query parameter
            self.params['pn'] = self.current_page
            
            # create next page URL to crawl
            next_page = res.url.split('?')[0] + '?' + urllib.parse.urlencode(self.params)
            
            # print debugging info
            self.log('Crawling zipcode %s out of %s zipcodes' % (count, total))
            self.log('Crawling page %s out of %s pages' % (self.current_page, total_pages))
            
            # crawl next page URL if available
            if self.current_page <= total_pages:
                # crawl next page within a given zipcode recursively
                yield scrapy.Request(url=next_page, headers=self.headers, meta={'zipcode': count, 'total': total}, callback=self.parse)
                

        except Exception as e:
            print(e)
        

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Immoscout)
    process.start()
    
    # debug data extraction
    #Immoscout.parse(Immoscout, '')
    
    
    
    
    
    
    
    
    
    
    
    
