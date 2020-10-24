#
# Script to scrape Lawyers from gtla.com 
#

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# gtla scraper class
class LawyersScraper(scrapy.Spider):
    # scraper name
    name = 'gtla'
    
    # base URL
    base_url = 'https://www.gtla.org/?&pg=findalawyer&diraction=SearchResults&fs_match=s&seed=505176&memPageNum='
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'lawyers.csv'
    }
    
    # crawler's entry point
    def start_requests(self):
        # loop over the range of pages
        for page in range(1, 11):
            # generate next page URL
            next_page = self.base_url + str(page)
            
            # crawl next page
            yield scrapy.Request(
                url=next_page,
                headers=self.headers,
                callback=self.parse_lawyers
            )
    
    # parse lawyers callback method
    def parse_lawyers(self, response):
        # loop over lawyer cards
        for card in response.css('div[class="span12 well"]'):
            # extract card features
            features = {
                'Name': card.css('span[class="MCDirectoryName"]')
                            .css('b::text')
                            .get()
                            .replace('\n', ''),
                
                'Photo URL': 'N/A',
                
                'Company': card.css('span[class="MCDirectoryCompany"]::text')
                               .get()
                               .replace('\n', ''),
                
                'Address': ''.join([
                               item for item in
                               card.css('div[itemprop="address"] *::text').getall()
                               if item != '\n'
                           ]).replace('\n', ''),

                'Phone': 'N/A',
                
                'Email': 'N/A',
                
                'Website': 'N/A',
                
                'Social links': 'N/A',
                
                'Champion member': 'no'
                
            }
            
            # extract contacts
            contacts = ''.join(card.css('div[class="MCDirectoryFieldsWrapper"] *::text').getall()).replace('\n\n', '\n').replace('\n', '|').split('|')[1:-1]                  
            
            # loop over contacts
            for item in contacts:
                if '@' in item:
                    features['Email'] = item.split(':')[-1].strip()
                
                elif 'http' in item:
                    features['Website'] = item.split('Website:')[-1].strip()
                
                else:
                    features['Phone'] = item.split(':')[-1].strip()
            
            # extract social links
            social_links = [
                url if 'http' in url else 'https://www.gtla.org' + url for url in
                card.css('div[style="padding:2px;"]').css('a::attr(href)').getall()
            ]
            
            features['Social links'] = social_links
            
            # extract photo
            photo_url = card.css('img[class="tsAppDirPhoto"]::attr(src)').get()
            
            if photo_url is not None:
                features['Photo URL'] = 'https://www.gtla.org/' + card.css('img[class="tsAppDirPhoto"]::attr(src)').get()
            
            # extract status
            status = card.css('img[class="directory-groupImage directory-groupImage-belowClassifications"]').get()

            if status is not None:
                features['Champion member'] = 'yes'
            
            # store data to CSV file
            yield features        

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(LawyersScraper)
    process.start()













