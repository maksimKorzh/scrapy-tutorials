import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

class Olx(scrapy.Spider):
    name = 'olx'
    
    url = 'https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&location=1000001&location_facet_limit=20&user=1708c08dd02x5e692f19'
    
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    def __init__(self):
        with open('results.csv', 'w') as csv_file:
            csv_file.write('title,description,location,features,date,price\n')
    
    def start_requests(self):
        for page in range(0, 5):
            yield scrapy.Request(url=self.url + '&page=' + str(page), headers=self.headers, callback=self.parse)
    
    def parse(self, res):
        data = res.text
        data = json.loads(data)
        
        for offer in data['data']:
            items = {
                'title': offer['title'],
                'description': offer['description'].replace('\n', ' '),
                'location': offer['locations_resolved']['COUNTRY_name'] + ', ' +
                            offer['locations_resolved']['ADMIN_LEVEL_1_name'] + ', ' +
                            offer['locations_resolved']['ADMIN_LEVEL_3_name'] + ', ' +
                            offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name'],
                'features': offer['main_info'],
                'date': offer['display_date'],
                'price': offer['price']['value']['display']
            }
            
            print(json.dumps(items, indent=2))
            
            with open('results.csv', 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=items.keys())
                writer.writerow(items)
    
    

# run scraper
process = CrawlerProcess()
process.crawl(Olx)
process.start()

# debug
#Olx.parse(Olx, '')
