##################################################
#
# Script to scrape dynamically rendered content
#         fed by AJAX "POST" request
#
#                       by
#
#                Code Monkey King
#
##################################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from scrapy.selector import Selector
import json

# AJAX data scraper
class AjaxScraper(scrapy.Spider):
    # scraper/spider name
    name = 'ajax'
    
    # base URL
    base_url = 'https://www.pdfdrive.com/ebook/ajax'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'books.csv'
    }
    
    # form data payload
    params = {
        'id': '33405148',
        'pagecount': '',
        'name': 'Half+Girlfriend+by+Chetan+Bhagat',
        'start': '0'
    }
    
    # crawler's entry
    def start_requests(self):
        # loop over "page" range
        for page in range(0, 4):
            # calculate next page's starting data index
            self.params['start'] = str(page * 20)
            
            # mimic AJAX call
            yield FormRequest(
                url=self.base_url,
                headers=self.headers,
                formdata=self.params,
                callback=self.parse
            )
    
    # parse response
    def parse(self, response):
        '''
        # write HTML response to local file
        with open('res.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # load local HTML file to extract data
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''
        
        # loop over book cards
        for card in response.css('li'):
            # data extraction logic
            features = {
                'title': ''.join(list(filter(None, [
                             text.get().replace('\n', '')
                             for text in
                             card.css('a *::text')
                         ]))),
                
                'url': 'https://www.pdfdrive.com' + card.css('a::attr(href)')
                                                         .get(),
                
                'pages': card.css('span[class="fi-pagecount "]::text')
                             .get(),
                
                'year': card.css('span[class="fi-year "]::text')
                             .get(),
                
                'size': card.css('span[class="fi-size hidemobile"]::text')
                             .get(),
                
                'downloads': card.css('span[class="fi-hit"]::text')
                             .get(),
                
                'description': ''.join(card.css('div[class="file-right"] *::text')
                                   .getall())
                                   .split('Downloads')[-1]
                                   .replace('\n', '')
                                   .strip(),
                
                'thumbnail': card.css('img::attr(src)')
                                 .get()
            }
            
            # store output to CSV file
            yield features
        
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(AjaxScraper)   
    process.start()
    
    # data extraction debugging
    #AjaxScraper.parse(AjaxScraper, '')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
