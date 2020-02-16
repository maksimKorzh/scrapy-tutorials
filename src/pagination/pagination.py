import scrapy
from scrapy.crawler import CrawlerProcess

class Pagination(scrapy.Spider):
    name = 'pagination'
    start_urls = []
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }
    
    def __init__(self):
        url = 'http://scrapingkungfu.herokuapp.com/chamber_3?page='
        
        for page in range(1, 5):
            self.start_urls.append(url + str(page))
        
    def parse(self, response):
        print('response url:', response.url)

# run scraper
process = CrawlerProcess()
process.crawl(Pagination)
process.start()
        
        
