# packages
import scrapy
from scrapy.crawler import CrawlerProcess

# chess games scraper class
class ChessGamesScraper(scrapy.Spider):
    # spider name
    name = 'chess_games_scraper'
    
    # base url
    base_url = 'https://lichess.org/@/Kingscrusher-YouTube/search'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # start crawling
    def start_requests(self):
        # lichess specific API key
        key_id = 1584694629328
        
        # loop over pages
        for page in range(1, 50):   # set max pages up to 1500 up to
            next_page = self.base_url + '?page=' + str(page) + '&perf=2&sort.field=d&sort.order=desc&_=' + str(key_id)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_game_list)
            key_id += 1
    
    # parse game list
    def parse_game_list(self, res):
        # extract game links
        games = res.css('a.game-row__overlay::attr(href)').getall()
        
        # loop over game links
        for game in games:
            yield res.follow(url=game, headers=self.headers, callback=self.parse_game)
    
    # parse game
    def parse_game(self, res):
        # extract PGN game
        pgn = res.css('div.pgn::text').get()
        
        # write PGN game to file
        with open('kingscrusher.pgn', 'a') as f:
            f.write(pgn + '\n\n\n')

# main driver
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ChessGamesScraper)
    process.start()
