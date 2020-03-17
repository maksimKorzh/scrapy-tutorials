# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import json
import string

class Urban(scrapy.Spider):
    name = 'urban'
    
    url = 'https://www.urbandictionary.com/popular.php?character='
    
    def start_requests(self):
        # clear output
        with open('urban.json', 'w') as f:
            f.write('')
        
        # loop over all the letters in alphabet
        for letter in string.ascii_uppercase:
            next_page = self.url + letter
            yield scrapy.Request(url=next_page, callback=self.parse)
            
            # comment to crawl ALL letters, but bear in ming it would TAKE TIME
            break
    
    def parse(self, res):
        # extract data
        links = []
        
        for item in res.css('ul.no-bullet').css('li'):
            word = item.css('a::text').get()
            short_description = requests.get('https://api.urbandictionary.com/v0/tooltip?term=' + word + 
                         '&key=ab71d33b15d36506acf1e379b0ed07ee').json()['string'].replace('\n', ' ').replace('\r', '').replace('<b>', '').replace('</b>', '')
        
            links.append({
                'word': word,
                'short_description': short_description,
                'link': item.css('a::attr(href)').get()
            })
            
            # uncomment break statement to crawl only the first word within a page
            # break

        # follow links recursively
        for link in links:
            yield res.follow(url=link['link'], meta={
                'short_description': link['short_description'],
                'word': link['word']
            }, callback=self.parse_link)
    
    def parse_link(self, res):
        # forward data from the above level
        word = res.meta.get('word')
        short_description = res.meta.get('short_description')
        
        # extract full description from link
        full_description = ' '.join(res.css('div.def-panel').css('div.meaning::text').getall())
        
        items = {
            'word': word,
            'short_description': short_description,
            'full_description': full_description
        }
        
        # write results
        with open('urban.json', 'a') as f:
            f.write(json.dumps(items, indent=2) + '\n')

        

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Urban)
    process.start()        
        
