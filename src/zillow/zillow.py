# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

# zillow scraper class
class ZillowScraper(scrapy.Spider):
    # scraper/spider name
    name = 'zillow'
    
    # base URL
    base_url = 'https://www.zillow.com/atlanta-ga/2_p/?'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # string query parameters
    params = {
        'searchQueryState': '{"pagination":{"currentPage":2},"usersSearchTerm":"Atlanta, GA","mapBounds":{"west":-85.03461392480469,"east":-84.19965298730469,"south":33.51431227246054,"north":34.094000649051324},"regionSelection":[{"regionId":37211,"regionType":6}],"isMapVisible":true,"filterState":{},"isListVisible":true}'
    }
    
    # custom settings
    custom_settings = {
        # uncomment below settings to slow down the scraper
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1
    }
    
    # crawler's entry point
    def start_requests(self):
        # loop over page range ( change "8" to whatever number of pages to crawl)
        for page in range(1, 8):
            # parse params
            parsed_params = json.loads(self.params['searchQueryState'])
            
            # init next page
            parsed_params['pagination']['currentPage'] = str(page)
            
            # update string query parameters
            self.params['searchQueryState'] = json.dumps(parsed_params).replace(' ', '')
            
            # init next page URL
            next_page = self.base_url + urllib.parse.urlencode(self.params)
            
            # crawl next page URL
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_links)
            
    # parse card links
    def parse_links(self, res):
        # extract card links
        card_links = res.css('ul[class="photo-cards photo-cards_wow photo-cards_short"]')
        card_links = card_links.css('li')
        card_links = card_links.css('a.list-card-link::attr(href)')
        
        # loop over property cards
        for card in card_links:
            # crawl property listing page recursively
            yield res.follow(url=card.get(), headers=self.headers, callback=self.parse_listing)
            
    # parse property listing
    def parse_listing(self, res):
        '''
        # store listing HTML to local file
        with open('res.html', 'w') as f:
            f.write(res.text)
        '''
        
        '''
        # local listing HTML content
        content = ''
        
        # load local listing HTML file to extract data from it
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        res = Selector(text=content)
        '''
        
        # extract feature list
        features = {
            'price': ''.join(res.css('div[class="ds-chip"]')
                                  .css('h3[class="ds-price"] *::text')
                                  .getall()),
            
            'address': ''.join(res.css('div[class="ds-chip"]')
                                  .css('h1[class="ds-address-container"] *::text')
                                  .getall()),
            
            'bedrooms': ' '.join(res.css('div[class="ds-chip"]')
                                  .css('span[class="ds-bed-bath-living-area"] *::text')
                                  .getall())
                                  .replace('  ', '|')
                                  .replace('| ', ':')
                                  .split()[0]
                                  .replace(':bd', ''),

            'bathrooms': ' '.join(res.css('div[class="ds-chip"]')
                      .css('span[class="ds-bed-bath-living-area"] *::text')
                      .getall())
                      .replace('  ', '|')
                      .replace('| ', ':')
                      .split()[1]
                      .replace(':ba', ''),
            
            'floor_area': ' '.join(res.css('div[class="ds-chip"]')
                      .css('span[class="ds-bed-bath-living-area"] *::text')
                      .getall())
                      .replace('  ', '|')
                      .replace('| ', ':')
                      .split()[2]
                      .replace(':', ' '),
            
            'zestimate': ''.join(res.css('div[class="ds-chip"]')
                                    .css('div[class="ds-chip-removable-content"] *::text')
                                    .getall())
                                    .split('\u00ae:\u00a0')[-1],
            
            'description': res.css('div[class="Text-aiai24-0 sc-feJyhm erkQcD"]::text')
                              .get(),
            
            'agent_info': {
                
                'agent_name': res.css('ul[class="cf-listing-agent-info"] *::text')
                                 .getall()[0],                              

                'agent_phone': res.css('ul[class="cf-listing-agent-info"] *::text')
                                 .getall()[1]
            },
            
            'facts_and_features': {},
            
            'tax_history': {},
            
            'monthly_cost': {},
            
            'nearby_schools': [
                                ' '.join(Selector(text=school).css(' *::text').getall()) for school in
                                res.css('ul[class="ds-nearby-schools-list"]')
                                   .css('li[class="sc-cMhqgX ikQQNx"]')
                                   .getall()
                              ],
            
            'coordinates': {
                'latitude': '',
                'longitude': ''
            }

        }
        
        # try to extract facts and features
        try:
            facts = res.css('ul[class="ds-home-fact-list"]')
            facts = '|'.join(facts.css('li *::text').getall()).replace(':|', ':').split('|')
            
            # loop over facts
            for fact in facts:
                features['facts_and_features'][fact.split(':')[0]] = fact.split(':')[1]
        except:
            pass
        
        # try to extract tax history
        try:
            tax_history = ''.join([' '.join(Selector(text=ul).css('li *::text').getall()) for ul in res.css('ul[class="sc-dqBHgY kQzYMy"]').getall() if 'Tax assessed value:' in ul])
            
            # store tax history
            features['tax_history'] = {
                'Tax assessed value': tax_history.split('Tax assessed value:')[1].split()[0],
                'Annual tax amount': tax_history.split('Annual tax amount:')[1].split()[0]
            }
        
        except:
            pass
        
        # try to extract monthly cost
        try:
            monthly_cost = res.css('div[class="sc-1b8bq6y-6 kKSvPL"] *::text').getall()
            monthly_cost = '|'.join(monthly_cost).replace('|$', ':$').replace('Chevron Down', '')
            monthly_cost = [item.replace('|', ' ').strip().replace('Utilities ', 'Utilities:') for item in monthly_cost.split('||')]
            
            # loop over monthly cost table
            for item in monthly_cost:
                features['monthly_cost'][item.split(':')[0]] = item.split(':')[1]
        except:
            pass
        
        # try to extract coordinates
        script = [script for script in res.css('script[type="application/ld+json"]').getall() if 'latitude' in script][0]
        script = Selector(text=script).css('::text').get()
        script = json.loads(script)

        # store coordinates
        features['coordinates']['latitude'] = script['geo']['latitude']
        features['coordinates']['longitude'] = script['geo']['longitude']
        
        # store output to JSON file
        with open('zillow.jsonl', 'a') as f:
            f.write(json.dumps(features, indent=2) + '\n')

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ZillowScraper)
    process.start()
    
    # debug data extraction logic
    #ZillowScraper.parse_listing(ZillowScraper, '')
    
    
    
    
    
    
    
    
    
    
