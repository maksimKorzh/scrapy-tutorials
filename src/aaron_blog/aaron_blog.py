#######################################
#
# Script to scrape Aaron S articles
# 
#                by
#
#         Code Monkey King
#
#######################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import json

# article scraper class
class ArticleScraper(scrapy.Spider):
    # scraper/ spider name
    name = 'articles'
    
    # base URL
    base_url = 'https://towardsdatascience.com/@u40as7'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 1
    }
    
    # crawler's entry point
    def start_requests(self):
        # make initial HTTP request to base URL
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_cards
        )
    
    # parse article cards
    def parse_cards(self, response):
        # loop over article cards
        for card in response.css('div[class="streamItem streamItem--postPreview js-streamItem"]'):
            # extract article card features
            features = {
                'title': card.css('h3::text')
                             .get(),
                
                'published_date': card.css('time::attr(datetime)')
                                      .get(),
                
                'article_link': card.css('a[class="link link--darken"]::attr(href)')
                                    .get(),
                
                'article_content': ''
            }
            
            # crawl article URL
            yield response.follow(
                url=features['article_link'],
                headers=self.headers,
                meta={
                    'article': features
                },
                callback=self.parse_article
            )
    
    # parse article content
    def parse_article(self, response):
        # extract article features
        article = response.meta.get('article')
        
        # extract article content
        article['article_content'] = response.css('article[class="meteredContent"] *::text')
        article['article_content'] = '\n'.join(article['article_content'].getall())
        
        # write output to file
        with open(article['title'], 'w') as f:
            f.write(
                article['title'] + '\n' + 
                article['published_date'] + '\n\n' +
                article['article_link'] + '\n\n\n\n' +
                article['article_content']
            )
    
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ArticleScraper)
    process.start()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
