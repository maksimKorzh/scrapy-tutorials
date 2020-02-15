import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesScraper(scrapy.Spider):
    # specify spider name, otherwise it won't work
    name = 'quotes'
    
    # these urls are crawled by default
    start_urls = ['http://quotes.toscrape.com']
    
    # callback function that fires after each HTTP request
    def parse(self, response):
        # casual way
        quotes = response.css('span.text::text').getall()
        authors = response.css('small.author::text').getall()
        
        for index in range(0, len(quotes)):
            data = {
                'author': authors[index],
                'quote': quotes[index]
            }
            
            print(json.dumps(data, indent=2))
    
        # pythonic way
        for quote in response.css('div.quote'):
            # yield might be used when you want to store output to CSV file
            yield {
                'author': quote.css('small.author::text').get(),
                'quote': quote.css('span.text::text').get()
            }
            
            
# run spider
process = CrawlerProcess()
process.crawl(QuotesScraper)
process.start()
