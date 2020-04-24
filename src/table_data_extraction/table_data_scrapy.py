# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# scraper class
class TableData(scrapy.Spider):
    # scraper name
    name = 'table_data'
    
    # start urls
    start_urls = ['https://www.enchantedlearning.com/wordlist/']
    
    # parse response
    def parse(self, res):
        # extract links
        table = Selector(text=res.css('table[border="1"]').get())
        titles = table.css('a::text').getall()
        urls = table.css('a::attr(href)').getall()
        
        # init links list
        links = []
        
        # loop over titles and links
        for index in range(0, len(titles)):
            links.append({
                'title': titles[index],
                'url': urls[index]
            })
        
            # follow links recursively
            next_url = urls[index]
            yield res.follow(url=next_url, callback=self.parse_link)
    
    # parse link
    def parse_link(self, res):
        print('RECURSIVE LINK RESPONSE:', res.text)
        
        
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(TableData)
    process.start()
