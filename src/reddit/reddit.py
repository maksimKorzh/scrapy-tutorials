##########################################
#
# Script to scrape posts from reddit.com
#
#                   by
#
#            Code Monkey King
#
##########################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
import json

# scraper class
class Reddit(scrapy.Spider):
    # scraper name
    name = 'reddit_scraper'
    
    # base URL
    base_url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/Gold?'
    
    # string query parameters
    params = {
      "rtj": "only",
      "redditWebClient": "web2x",
      "app": "web2x-client-production",
      "allow_over18": "",
      "include": "identity",
      "after": "t3_he8jq5",
      "dist": "2",
      "layout": "card",
      "sort": "hot",
      "geo_filter": "UA"
    }
    
    # crawler's entry point
    def start_requests(self):
        # generate API URL
        url = self.base_url + urlencode(self.params)
        
        # make initial HTTP request
        yield scrapy.Request(
            url=url,
            callback=self.parse_page
        )
    
    # parse page callback method
    def parse_page(self, response):
        # parse JSON response to python dictionary data type
        json_data = json.loads(response.text)
        
        
        # loop over posts
        for post in json_data['posts']:
            # extract post URL
            post_url = json_data['posts'][post]['permalink']
            print(post_url)
            
            # make HTTP request to the given post URL
            yield response.follow(
                url=post_url,
                callback=self.parse_post
            )
        
        # update string query parameters
        self.params['after'] = json_data['token']
        self.params['dist'] = json_data['dist']
        
        # generate API URL
        url = self.base_url + urlencode(self.params)
        
        # print debug info
        print('\n\nScroling page... | next URL: %s\n\n' % url)
        
        # make recursive HTTP request to the next "infinite scroll" page
        yield scrapy.Request(
            url=url,
            callback=self.parse_page
        )
    
    # parse post callback method
    def parse_post(self, response):
        # extract post data
        post = {
            'title': response.css('h1[class="_eYtD2XCVieq6emjKBH3m"]::text').get(),
            'description': response.css('p[class="_1qeIAgB0cPwnLhDF9XSiJM"]::text').get(),
            'comment': response.css('p[class="_1qeIAgB0cPwnLhDF9XSiJM"]::text').getall() 
        }
        
        # write JSONL output
        with open('posts.jsonl', 'a') as f:
            f.write(json.dumps(post, indent=2) + '\n')

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Reddit)
    process.start()










