# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# city scraper class
class CityScraper(scrapy.Spider):
    # scraper/spider name
    name = 'cityscraper'
    
    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # base URL
    base_url = 'https://atlas.immobilienscout24.de'
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'german_cities.csv'
    }
    
    # crawler's entry
    def start_requests(self):
        # area HTML content
        content = ''
        
        # open "area.html" local file to extract area URLs from
        with open('area.html', 'r') as f:
            for line in f.read():
                content += line
        
        # extract area URLs
        selector = Selector(text=content)
        for area in selector.css('div[class="grid geo-element-list"]').css('a::attr(href)'):
            next_area = self.base_url + area.get()
        
            # crawl areas
            yield scrapy.Request(url=next_area, headers=self.headers, callback=self.parse)
    
    # parse response
    def parse(self, res):
        # district URLs raw script content
        district_urls = ''
        
        # loop over all available script tags on the page
        for script in res.css('script'):
            if 'window.IS24.PropertyBook.onPageletReceiveSuccessful("subHierarchyInfo"' in script.get():
                district_urls = script.get()
        
        # check district URLs availability
        if district_urls is not None:
            district_urls = district_urls.split('window.IS24.PropertyBook.onPageletReceiveSuccessful("subHierarchyInfo",')[1]
            district_urls = district_urls.split(');')[0].strip()
            district_urls = json.loads(district_urls)
            
            # loop over district urls
            for item in district_urls:
                destrict_name = item['key'].split('/orte/deutschland/')[-1]
                
                # write output
                yield { 'url': destrict_name }
                

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(CityScraper)
    process.start()



















