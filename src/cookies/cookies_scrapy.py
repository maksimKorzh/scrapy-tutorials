###########################################
#
# Script to pass headers & cookies along 
#            with HTTP request
#        using "scrapy" framework
#
#                    by
#
#             Code Monkey King   
#
###########################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import json

# spider class
class HeadersCookies(scrapy.Spider):
    # spider name
    name = 'headerscookies'
    
    # urls
    url_request = 'https://enckllaec924.x.pipedream.net/'
    url_rightmove = 'https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E87490&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
    
    # custom headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # raw cookie string
    cookie_string = '_gcl_au=1.1.136040229.1590066423; _ga=GA1.2.1692634669.1590066423; ki_r=; _gid=GA1.2.1713292175.1590419428; _lr_uf_-dhjtrz=ce30d577-6f48-4fed-a8c7-f62a1ad0dfe0; _hjid=8d49fb07-ab72-43b4-8644-f1d940d27e8c; _lr_tabs_-dhjtrz%2Fpd={%22sessionID%22:0%2C%22recordingID%22:%224-fb21a045-34f8-42e7-a88e-7dee3bd00b7f%22%2C%22lastActivity%22:1590419503881}; ki_t=1590066423815%3B1590419428236%3B1590419506365%3B2%3B3; amplitude_id_eadd7e2135597c308ef5d9db3651c843requestbin.com=eyJkZXZpY2VJZCI6ImE2ZTc2ZGEyLTRhOGMtNDZjOS05OTQ4LTAyMjZkYTFmODkwNlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU5MDQxOTQyODEwOSwibGFzdEV2ZW50VGltZSI6MTU5MDQxOTU0NDQzNywiZXZlbnRJZCI6MTksImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjoxOX0=; _lr_hb_-dhjtrz%2Fpd={%22heartbeat%22:1590419624030}'
    
    # parse cookies
    def parse_cookies(self, raw_cookies):
        # parsed cookies
        cookies = {}
        
        # loop over cookies
        for cookie in raw_cookies.split('; '):    
            try:
                # init cookie key
                key = cookie.split('=')[0]
                
                # init cookie value
                val = cookie.split('=')[1]
                
                # parse raw cookie string
                cookies[key] = val
            
            except:
                pass
        
        return cookies
    
    # crawler's entry point
    def start_requests(self):
        # make HTTP GET request to "requestbin.com"
        yield scrapy.Request(
            url=self.url_rightmove,
            headers=self.headers,
            cookies=self.parse_cookies(self.cookie_string),
            callback=self.parse
        )
        
    # parse response
    def parse(self, response):
        print('\n\nRESPONSE URL: %s\n\n' % response.url)
    
        # extract raw cookies
        raw_cookies = '; '.join([
            cookie.decode('utf-8')
            for cookie in
            response.headers.getlist('Set-Cookie')
        ])
        
        print('\n\nSET COOKIE: %s\n\n' % raw_cookies)
        
        # make HTTP GET request to "requestbin.com"
        yield scrapy.Request(
            url=self.url_request,
            headers=self.headers,
            cookies=self.parse_cookies(raw_cookies),
            callback=self.parse
        )


# main driver
if __name__ == '__main__':
    # run spider
    process = CrawlerProcess()
    process.crawl(HeadersCookies)
    process.start()














        
        
        
        
        
        
