###########################################################
#
# Script to scrape boxer rankings from https://box.live/
#
#                           by
#
#                    Code Monkey King
#
###########################################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# boxer rankings class
class BoxerRankings(scrapy.Spider):
    # scraper/spider name
    name = 'boxer_rankings'
    
    # base URL
    base_url = 'https://box.live/boxing-rankings/'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        # uncomment to slow down the crawling speed
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        #'DOWNLOAD_DELAY': 1
    }
    
    # crawlre's entry
    def start_requests(self):
        # make HTTP request to the base URL
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_boxer
        )
    
    # parse boxer data
    def parse_boxer(self, response):
        # boxer URLs
        boxer_urls = []
        
        # extract champion URLs
        champion_urls = response.css('div[class="rank_full_mini"]')
        champion_urls = champion_urls.css('a[href*="boxer"]::attr(href)')
        champion_urls = champion_urls.getall()
        
        # extract challanger URLs
        challenger_urls = response.css('div[class="rank_full_mini"]')
        challenger_urls = challenger_urls.css('ol').css('li')
        challenger_urls = challenger_urls.css('a::attr(href)')
        challenger_urls = challenger_urls.getall()
        
        # loop over champion URLs
        for url in champion_urls:
            # append champions to list
            boxer_urls.append(url)
        
        # loop over challenger URLs
        for url in challenger_urls:
            # append challangers to list
            boxer_urls.append(url)
        
        # boxer count
        count = 1
        
        # loop over boxer URLs
        for boxer_url in boxer_urls:
            # crawl boxer's profile
            yield response.follow(
                url=boxer_url,
                headers=self.headers,
                meta={
                    'count': count,
                    'total': len(boxer_urls)
                },
                callback=self.parse_profile
            )
            
            # increment boxer count
            count += 1
        
    # parse profile data
    def parse_profile(self, response):
        '''
        # store HTML response locally
        with open('profile.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # open local HTML file
        with open('profile.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''
        
        # extract current boxer count
        count = response.meta.get('count')
        total = response.meta.get('total')
        
        # print debug info
        print('\n\nBoxer #%s out of %s total boxers\n\n' % (count, total))
        
        # extract profile feature
        features = {
            'name': response.css('li[class="hightlight full-record"]')
                            .css('h1::text')
                            .get(),
            
            'image_url': response.css('div[class="single-fighter"]')
                                 .css('img::attr(src)')
                                 .get(),
            
            'record': response.css('span[class="record"]::text')
                              .get(),
            
            'titles': {
                'IBF': response.css('li[class="ibf-belt belt-row"]::text').get(),
                'WBO': response.css('li[class="wbo-belt belt-row"]::text').get(),
                'WBA': response.css('li[class="wba-belt belt-row"]::text').get()
            },
            
            'points_count': [],
            
            'stats': {
                'age': response.css('span[class="f-desc"]::text').getall()[0],
                'height': response.css('span[class="f-desc"]::text').getall()[1],
                'reach': response.css('span[class="f-desc"]::text').getall()[2],
                'stance': response.css('span[class="f-desc"]::text').getall()[3],
            },
            
            'full_record': {
                'wins': response.css('span[class="f-desc"]::text').getall()[4],
                'by_ko': response.css('span[class="f-desc"]::text').getall()[5],
                'ko_%': response.css('span[class="f-desc"]::text').getall()[6],
                'lost': response.css('span[class="f-desc"]::text').getall()[7],
                'stopped': response.css('span[class="f-desc"]::text').getall()[8],
                'draws': response.css('span[class="f-desc"]::text').getall()[9],
                'debut': response.css('span[class="f-desc"]::text').getall()[10],
                'pro_rds': response.css('span[class="f-desc"]::text').getall()[11]
            },
            
            'ranking': {},
            
            'division': ''.join([
                            text.get().split(' @ ')[-1]
                            for text in
                            response.css('li[class="hightlight full-record"]::text')
                            if '@' in text.get()
                        ]),
            
            'description': '\n'.join(response.css('div[class="expert-fighter-filters"]')
                                             .css('p::text')
                                             .getall()),
            
            'odds': [],
            
            'potential_fights': []        
        }
        
        # extract ranking
        try:
            features['ranking'] = {
                'wbo': response.css('span[class="f-desc"]::text').getall()[12],
                'ibf': response.css('span[class="f-desc"]::text').getall()[13],
                'wbc': response.css('span[class="f-desc"]::text').getall()[14],
                'wba': response.css('span[class="f-desc"]::text').getall()[15]
            }
        
        except:
            pass
        
        # extract points count keys
        points_count_keys = list(filter(None, [
                                text.get().replace('\n', '').strip()
                                for text in
                                response.css('span[class="points-count"]')
                                        .css('i::text')
                                if text.get() != ' < '
                            ]))
        
        # extract points count values
        points_count_vals = list(filter(None, [
                                text.get().replace('\n', '').strip()
                                for text in
                                response.css('span[class="points-count"]')
                                        .css('i')
                                        .css('small::text')
                                if text.get() != ' < '
                            ]))
        
        # loop over the range of points count
        for index in range(0, len(points_count_vals)):
            features['points_count'].append(
                {points_count_keys[index]: points_count_vals[index]}\
            )
        
        # extract odds
        for table in response.css('table[class="responsive boxing-betting-table"]'):
            # extract odds row
            odds_row = list(filter(None, [
                                text.get().replace('\n', '').replace(' ', '')
                                for text in
                                table.css('tr').css('span[class="dec odd"] *::text')
                            ]))
            
            # extract fighter name
            fighter_name = table.css('td[class="fighter_name"]').css('a::text').getall()
            
            features['odds'].append({
                'boxer': {
                    'name': fighter_name[0],
                    'williamhill': odds_row[0],
                    'unibet': odds_row[1],
                    'boyle': odds_row[2],
                    'ladbrokes': odds_row[3],
                    'skybet': odds_row[4],
                    'betway': odds_row[5],
                    'bwin': odds_row[6],
                    'betfred': odds_row[7],
                    'winner': odds_row[8]
                },
                
                'opponent': {
                    'name': fighter_name[1],
                    'williamhill': odds_row[9],
                    'unibet': odds_row[10],
                    'boyle': odds_row[11],
                    'ladbrokes': odds_row[12],
                    'skybet': odds_row[13],
                    'betway': odds_row[14],
                    'bwin': odds_row[15],
                    'betfred': odds_row[16],
                    'winner': odds_row[17]
                }
            })
        
        # extract potential fights
        for fight in response.css('div[class="boxer-area"]')[1:]:
            # extract potential date
            try:
                potential_date = fight.css('span[class="date potenclash"]::text').get()
                potential_date = potential_date.strip('\n').split(' : ')[-1]
            
            except:
                potential_date = 'N/A'
        
            features['potential_fights'].append({
                'opponent_name': fight.css('div[class="right"]')
                                      .css('a::attr(title)')
                                      .get(),
                
                'opponent_image_url': fight.css('div[class="right"]')
                                           .css('img::attr(src)')
                                           .get(),
                
                'opponent_record': fight.css('span.record-r *::text')
                                        .get()
                                        .strip('\n'),
                
                'potential_date': potential_date,
                
                'title_belts': {
                    'wbc': fight.css('li[class="wbc-belt belt-row"]::text')
                                .get(),
                    
                    'ibf': fight.css('li[class="ibf-belt belt-row"]::text')
                                .get(),
                    
                    'wba': fight.css('li[class="wba-belt belt-row"]::text')
                                .get(),

                    'wbo': fight.css('li[class="wbo-belt belt-row"]::text')
                                .get(),
                }
            })
        
        # print resulting dataset
        #print(json.dumps(features, indent=2))
        
        # write features to file
        with open('boxers.jsonl', 'a') as f:
            f.write(json.dumps(features, indent=2) + '\n')
        
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(BoxerRankings)
    process.start()
    
    # debug data extraction logic
    #BoxerRankings.parse_profile(BoxerRankings, '')










