######################################
#
# Script to scrape movies data from
#    https://m.hindigeetmala.net
#
#                by
#
#         Code Monkey King
#
######################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import string
import csv

# scraper class
class Movies(scrapy.Spider):
    # scraper name
    name = 'indian_movies'
    
    # base URL
    base_url = 'https://m.hindigeetmala.net/movie/'
    
    # current page counter
    current_page = 1
    
    # crawler's entry
    def start_requests(self):
        # init output file
        with open('movies.csv', 'w') as f:
            f.write('Song Heading,Singer,Composer,Lyricist,Actor,Film (Year),Category\n')
    
        # loop over letters
        for letter in string.ascii_lowercase:
            # reset current page number
            self.current_page = 1
            
            # generate letter URL
            letter_url = self.base_url + letter + '.php'
            
            # crawl letter URL
            yield scrapy.Request(
                url=letter_url,
                meta={
                    'letter': letter
                },
                callback=self.parse_letter
            )
    
    # parse letter callback method
    def parse_letter(self, response):
        # extract letter
        letter = response.meta.get('letter')
        
        # loop over movie cards
        for card in response.css('div[class="col-xs-6 col-md-4 col-lg-3"]'):
            # extract movie URL
            movie_url = card.css('a::attr(href)').get()

            # crawl movie URL
            yield response.follow(
                url=movie_url,
                callback=self.parse_movie
            )
        
        # handle pagination for each letter
        try:
            total_pages = response.css('ul[class="pagination  pagination-sm pull-right pagination-skg"]')
            total_pages = total_pages.css('a[href*=page]::attr(href)').getall()
            total_pages = max([int(page.split('=')[-1]) for page in total_pages])
            
        
        except:
            total_pages = 1
        
        # increment current page
        self.current_page += 1
        
        # check if any pages to crawl left
        if self.current_page <= total_pages:
            # generate next page UR*L
            next_page = response.url.split('?')[0] + '?page=' + str(self.current_page)

            # print debug info
            print('\n\nCurrent letter: %s | Current page %s' % (letter, self.current_page))            
            
            # crawl next page URL
            yield response.follow(
                url=next_page,
                meta={
                    'letter': letter
                },
                callback=self.parse_letter
            )
        
        else:
            self.current_page = 1
    
    # parse movie callback method
    def parse_movie(self, response):
        # loop over rows of first two tables
        for row in response.css('table')[:-1].css('tr'):
            # extract items
            items = [
                ''.join(col.css(' *::text').getall())
                for col in
                row.css('td')
            ]
            
            # work only with non-empty items
            if len(items):
                # open file stream to append data
                with open('movies.csv', 'a') as f:
                    # create CSV writer
                    writer = csv.writer(f)
                    
                    # write current row to file
                    writer.writerow(items[1:])


# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Movies)
    process.start()















































