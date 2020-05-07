###############################################
#
# Switzerland yellow pages scraper (local.ch)
#
###############################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json
import csv
import os.path

# yellow pages scraper class
class Local(scrapy.Spider):
    # scraper/spider name
    name = 'local'
    
    # base URL
    base_url = 'https://www.local.ch/'
    
    # string query parameters
    params = {
        'page': 1
    }
    
    # current page counter
    current_page = 1
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        # uncomment below settings to limit crawling speed
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1,
    }
    
    # crawler's entry point
    def start_requests(self):
        # init field names
        field_names = [
            'name',
            'category',
            'details_url',
            'rating_stars',
            'address',
            'opening_status',
            'corona_status',
            'email',
            'phone',
            'website',
            'book_a_table'
        ]

        # reset output file
        with open('local.csv', 'w') as f:
            f.write(','.join(field_names) + '\n')
    
        # make initial HTTP request
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_categories
        )
    
    # parse categories
    def parse_categories(self, response):
        # extract category selectors
        category_selectors = response.css('div[class="multi-col-list js-super-topic-list"]')
        
        # extract category names
        category_names = category_selectors.css('a[class="js-gtm-event"]::text').getall()
        
        # extract category URLs
        category_links = category_selectors.css('a[class="js-gtm-event"]::attr(href)').getall()
        
        # loop over category links
        for index in range(0, len(category_links)):
            # init category URL and name
            category = category_links[index]
            name = category_names[index]
            
            # reset current page counter for each category
            self.current_page = 1
            
            # crawl categories recursively
            yield response.follow(
                url=category,
                headers=self.headers,
                callback=self.parse_cards
            )
            
    # parse cards
    def parse_cards(self, response):
        # loop over service cards
        for card in response.css('div[class="entry-card entry-card-highlight entry-card-yellow"]'):
            # extract card features
            features = {
                'name': ''.join([
                                    item.strip('\n') for item in
                                    card.css('h2[class="lui-margin-vertical-zero card-info-title"] *::text')
                                        .getall()
                                    if item != '\n'
                                ]),

                'category': ', '.join([
                                        item for item in
                                        card.css('div[class="card-info-category"] *::text')
                                            .getall()
                                        if item != '\n' and item != ' • '
                                   ]),

                'details_url': card.css('a[class="card-info clearfix js-gtm-event"]::attr(href)')
                                   .get(),

                'rating_stars': card.css('span[class="short-summary-ratings-value lui-font-bold"]::text')
                                    .get(),
                
                'address': ''.join([
                                        item for item in
                                        
                                        card.css('div[class="card-info-address"] *::text')
                                            .getall()
                                        
                                        if item != '\n'
                                   ]),
                
                'opening_status': ''.join([
                                        item for item in
                                        
                                        card.css('div[class="card-info-open hidden-print"] *::text')
                                            .getall()
                                        
                                        if item != '\n' and item != '\n\n'
                                   ]),
                
                'corona_status': ''.join([
                                        item for item in
                                        
                                        card.css('div[class="icon-coronavirus-alt"] *::text')
                                            .getall()
                                        if item != '\n'
                                   ]),
                
                'email': ''.join([
                                      item for item in
                                      
                                      card.css('a[class="js-gtm-event js-kpi-event action-button text-center hidden-xs action-button-default"]')
                                          .css('span *::text')
                                          .getall()

                                      if item != '\n' and item != 'E-Mail'
                                  ]),
                
                'phone': ''.join([
                                      item.strip('\n') for item in
                                      
                                      card.css('a[class="js-gtm-event js-kpi-event action-button text-center hidden-md hidden-lg action-button-default"]')
                                          .css('span *::text')
                                          .getall()

                                      if item != '\n'
                                  ]),
               
               'website': ''.join([
                                      item for item in
                                      
                                      card.css('a[class="js-gtm-event js-kpi-event action-button text-center action-button-default"]')
                                          .css('span *::text')
                                          .getall()

                                      if item != '\n' and item != 'Website'
                                  ]),
               
               'book_a_table': card.css('a[class="js-gtm-event action-button text-center action-button-primary hidden-print"]::attr(href)')
                                   .get()
                
            }

            # write output to CSV file
            with open('local.csv', 'a') as f:
                # create CSV dictionary writer
                writer = csv.DictWriter(f, features.keys())
                
                # write CSV row
                writer.writerow(features)
        
        #####################
        # try to crawl pages
        #####################
        try:
            # increment current page counter
            self.current_page += 1
        
            # extract number of search results
            search_results = response.css('div[class="search-header-results-title"]::text').get()
            search_results = int(search_results.split()[0])
            
            # extract total pages to crawl
            total_pages = int(search_results / 10) + 1
            
            # crawl next page condition
            if self.current_page <= total_pages:
                # update page number
                self.params['page'] = self.current_page
                
                # generate next page url
                next_page = response.url.split('&page=')[0] + '&' + urllib.parse.urlencode(self.params)
                    
                # print debug info
                print('\n\nPage %s out of %s pages' % (self.current_page, total_pages))
                
                # crawl next page
                yield response.follow(
                    url=next_page,
                    headers=self.headers,
                    callback=self.parse_cards
                )
        
        except Exception as e:
            self.current_page = 1
            print(e)
    
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Local)
    process.start()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
