# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import json

##############################################
#
# Script to demonstrate how to pass cookies
#     within headers instead in Scrapy
#
#                     by
#
#              Code Monkey King
#
##############################################

# scraper class
class Scraper(scrapy.Spider):
    # name
    name = 'scraper'

    # custom headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'PHPSESSID=je2ihl1lhr92jech7j13bind4m; currentCurrency=EUR; _pubcid=27fb85ca-08bd-451b-b530-24d82ecb19ac; _ga=GA1.2.1782779244.1591116926; _fbp=fb.1.1591116927166.1660527984; __beaconTrackerID=bjslrvk08; pbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMO-IfC2hLDioNVmEbVWDvFJy2lmvjGeshZ0iR8SQ%22%2C%22ID5ID_CREATED_AT%22%3A%222020-01-21T16%3A44%3A03.879Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; _gid=GA1.2.320661592.1591258798; spitogatosHomepageMap=0; __gads=ID=1be9586193cfdbf7:T=1591258837:S=ALNI_Mbk6BSxt8QA47TPFhU2Gkm8M-kgeg; spitogatosS=areaIDs%255B0%255D%3D2022%26areaIDs%255B1%255D%3D2038%26areaIDs%255B2%255D%3D2610%26areaIDs%255B3%255D%3D2616%26areaIDs%255B4%255D%3D3011%26areaIDs%255B5%255D%3D6007%26areaIDs%255B6%255D%3D6013%26areaIDs%255B7%255D%3D6116%26areaIDs%255B8%255D%3D6119%26areaIDs%255B9%255D%3D384410%26propertyCategory%3Dresidential%26listingType%3Dsale%26priceHigh%3D30000; PHPSESSID=fs93223qkf61k8c6a5f589bsdh; eupubconsent=BO0eApgO0eApgAKAiAENAAAAgAAAAA; euconsent=BO0eApgO0eApgAKAiBENDM-AAAAv5r_7__7-_9f-_f__9uj3Gr_v_f__32ccL5tv3h_7v-_7fi_-0nV4u_1vft9ydk1-5ctDztp507iakiPHmqNeb1n_mz1eZpRP58E09j5335Ew_v8_v-b7BCPN9Y3v-8K94A; _hjid=43265493-46ec-47f4-91bc-c39f2bcbcf8c; pbjs-id5id_last=Thu%2C%2004%20Jun%202020%2011%3A49%3A32%20GMT; _cmpQcif3pcsupported=1; cto_bidid=LFJAfV9walJpTEZQNng3WUVENEsydG50ZlBYcSUyQjhaUk9kWldvZ1R2YWx5Ujc2RlZndjZmaG1kdFZHTTVwaTZFVXVkJTJCWmNRWVhLVzFjNzZWcW4weUc5cEdNSGg0dENiRGxsd1BEUFJvNTNHcWQ0TEElM0Q; cto_bundle=JgNool9wd2h5JTJCNDRTZSUyQmlVODJxUjNFbXdkJTJGWllPM2VSeEpDeHBtSkFVRFRFbG8waEhCdnBYRU81OHI0UG52Tld2WXhoZWpCVXdnZVB0T0E5dFE0MDVwRlclMkZRSWpyZlp4dWRoVURJdUg1aXN5SlF0RG9SVFZBMFdscnNZOXRtcUJWSlBtWmlXS3huZllWZXJ5TnJjTzdlJTJCZ3hBJTNEJTNE; DigiTrust.v1.identity=eyJpZCI6ImFUekp2K0ExNG8yc0dHektPb2NuaHcwVFlPK2tYSzJNSFRVY0dCWHV5Ukx3RkM0eEhFMC9IRm84SUE1VXNZMkxPekw2ZVFPallKWVFVeGhIK3h1ZGgrVEdubGRNcUZGQ0NTMWpSRDUwQUNoNW96UDFFM0xINzFoTlVvUmdVM3lkTHN5RU9pdzNCZmNUR0d5R1lSeGxKNHhpVDJ2U1czSDFwWEFrMXExSnpvSDdxcnQvWmRCNEI5VUoza0ZUZHdtd2ROR2swQUxYTEcxNnEwYjltMmhJSnpIYVl2b05UcW5zdGllclh3QjZob0hOWVNLMlBPdU82VlhoeXdrV05HQ0oyc2M5RUExbjMrWEZSaTkrblRQek5vSDlQNmJiWVRBRzhmTGlMNXptYWVQNElnaTFIeFh1aFVGT1pVb3ArMnc0V2ovTlFMaVdWb3hUWWRHVWtMais4dz09IiwidmVyc2lvbiI6MiwicHJvZHVjZXIiOiIxQ3JzZFVOQW82IiwicHJpdmFjeSI6eyJvcHRvdXQiOmZhbHNlfSwia2V5diI6NH0%3D; openedTabs=1; reese84=3:Hm8/pSyGIwWDxv4knMziRg==:nC9Zm0kP5S3R1uqsVV2MWuSDFiZeO0XIpyur2nat1JR+BOP7WgmHGykKqlOF7uV+X8/gsgaakSKQF4BwfsD4JiVTVZdrcF8guXteqYlQPY0S832tvdRxp8sEgxkIAebktUKX2iLHh0/9zobrjuE2a9khpSpI8rYzG7pIzz3pEX1/AUP0vozVAXQnZFTgJl7PeAflegDnnyv4p0fxQpmtRdTgee79lJiuy5myt1iP40EhymNZe90dELTs3bvN+Y9W5HzKL9kURNpvX6b0PNyX5aSBWJlWm03/DnDnFz5CYIG7TbA26yWeCJH0Go9eTdRTaCDK9zBYnVqgAu8WtmOe4dCofijXsAD3vC4Inaqry8Rnr0mR0oVbD6BYtGR00aqFqPslKjLp8Brbj+p+PusyHt16PdnU3BfBnZX1TmQvqTM=:rGACf+6e6spBl64VzTsk7REzG0iELo1Vb2wF8ZZKwhg=',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'COOKIES_ENABLED': False
    }
    
    # crawler's entry point
    def start_requests(self):
        # cookie string
        cookies_raw = 'PHPSESSID=je2ihl1lhr92jech7j13bind4m; currentCurrency=EUR; _pubcid=27fb85ca-08bd-451b-b530-24d82ecb19ac; _ga=GA1.2.1782779244.1591116926; _fbp=fb.1.1591116927166.1660527984; __beaconTrackerID=bjslrvk08; pbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMO-IfC2hLDioNVmEbVWDvFJy2lmvjGeshZ0iR8SQ%22%2C%22ID5ID_CREATED_AT%22%3A%222020-01-21T16%3A44%3A03.879Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; _gid=GA1.2.320661592.1591258798; spitogatosHomepageMap=0; __gads=ID=1be9586193cfdbf7:T=1591258837:S=ALNI_Mbk6BSxt8QA47TPFhU2Gkm8M-kgeg; spitogatosS=areaIDs%255B0%255D%3D2022%26areaIDs%255B1%255D%3D2038%26areaIDs%255B2%255D%3D2610%26areaIDs%255B3%255D%3D2616%26areaIDs%255B4%255D%3D3011%26areaIDs%255B5%255D%3D6007%26areaIDs%255B6%255D%3D6013%26areaIDs%255B7%255D%3D6116%26areaIDs%255B8%255D%3D6119%26areaIDs%255B9%255D%3D384410%26propertyCategory%3Dresidential%26listingType%3Dsale%26priceHigh%3D30000; PHPSESSID=fs93223qkf61k8c6a5f589bsdh; eupubconsent=BO0eApgO0eApgAKAiAENAAAAgAAAAA; euconsent=BO0eApgO0eApgAKAiBENDM-AAAAv5r_7__7-_9f-_f__9uj3Gr_v_f__32ccL5tv3h_7v-_7fi_-0nV4u_1vft9ydk1-5ctDztp507iakiPHmqNeb1n_mz1eZpRP58E09j5335Ew_v8_v-b7BCPN9Y3v-8K94A; _hjid=43265493-46ec-47f4-91bc-c39f2bcbcf8c; _hjAbsoluteSessionInProgress=1; pbjs-id5id_last=Thu%2C%2004%20Jun%202020%2011%3A49%3A32%20GMT; _cmpQcif3pcsupported=1; reese84=3:jxqIwTqiLz8mKueAzd9aow==:H0PTobQNDZdcAR/lsI4iYLAs63+mGPfIKbiYt7F1CvBOj2Tx2Qkoj20WvmGThGOy8ocix50Oute8jr0EXxf/zsBOUcC6hTDEaXWnTzpX0fgDHcLiFSwhZg3ywQreC8VN2baA1u2mjDyaLWt5H1gla6hxqCghCr8FgWNAKHulvILcztPdUnSZ50yCcPPU9jXgZV5hMim2/1KoU1thQWkLNHzveT7D7qxiqte5L1+kwSxAcU8FHmHZAYqZU/Z9iRdTOZK7rn09F3LipA/Cl2SAaTQ8Jmn78AKLUGNHA1AOYgLMZ8Y5SOrVFteQSDeCBDQXB+NIWAIHRCTTIB/Jn0dweVg/zbt2G1Q7SAwkQ8Rbd2LxcYASPOLMdP4tXrqZ3AeIGyVP//jyQcZzqnSHkH43812sXiby4zdfKaUs2UABwrc=:fsX7D49p3eP8J1+p8RQM6zmrYt0iU1xFMo4tuVKk28g=; openedTabs=1; cto_bidid=3OI-NV9walJpTEZQNng3WUVENEsydG50ZlBYcSUyQjhaUk9kWldvZ1R2YWx5Ujc2RlZndjZmaG1kdFZHTTVwaTZFVXVkJTJCWmNRWVhLVzFjNzZWcW4weUc5cEdNSG9majBVdktjSWZqU2VDRHowOXZMeHclM0Q; cto_bundle=wX9lHl9wd2h5JTJCNDRTZSUyQmlVODJxUjNFbXdkJTJGMmJ4ZDVaSjVpSUMyRjk4JTJGUjlZdEE4TWk3TndTSTFtUTlxckJrOFpQSEZ6TnlMMXdJJTJCbXc1emh4emEzYklRc3hZNXQyUUE1SFhEdVA3OXJ5djFqWU9icWo0dko4N01VZjMxTXF0YW5BMXBObUVKRHYzJTJCOUZSd1BIU2xXVkRMbFElM0QlM0Q; DigiTrust.v1.identity=eyJpZCI6IlVGcWFTZVNZR3NaYXN6ZEY1UzYwM3VLT25FaGl2WmRSN0VGRDBhRHl5Rm15L2E1RHdORzZwdlNnWHRXSHRIK2ZUbXFWaGkwOWxERWtZYmRwRThBckMwNUo5OWhoWVgyZFp4Zk11eW1IaVpRZkdRSWtoS1VMT2swVC9sVk9hVk5EdVM4VGhtdFZKYU4rYXdyN2o2ZjJYMzB5QlUwUWhSOWdIVXlmdVFTMmJwdllGWVNnUXZrVWxHNDZYZ3l3cEh6Q00vUzFwMGd2aXN5cnRSbnNTM3V2Slg4czQzb0tYTzUyYXk5MFhGMHlRNG1Jc0VYVXl2TDRpSGMxaEcvRUJTdjF3YzVWMTI1SGQrUzFseVJ1V0c1NGppVkw1ZklYWTE3dDNMZUo0dkxBNm54eWhjOVhjR2h0eFhvRGFlRDFtZWtOTkVHU3V3c0hnb1NwcjlxcnVNK2dwdz09IiwidmVyc2lvbiI6MiwicHJvZHVjZXIiOiIxQ3JzZFVOQW82IiwicHJpdmFjeSI6eyJvcHRvdXQiOmZhbHNlfSwia2V5diI6NH0%3D; _gat_UA-3455846-10=1; _gat_UA-3455846-3=1'

        # cookies dictionary
        cookies = {}
        
        # lop over cookies string
        for cookie in cookies_raw.split(';'):
            # init key value pairs
            key = cookie.strip().split('=')[0]
            val = cookie.strip().split('=')[-1]
            
            # init cookies
            cookies[key] = val
        
        print(json.dumps(cookies, indent=2))
    
        # make HTTP request
        yield scrapy.Request(
            #url='https://enckllaec924.x.pipedream.net',
            url='https://en.spitogatos.gr/search/results/residential/sale/r100/m2022m2038m2610m2616m3011m6007m6013m6116m6119m384410m/price_nd-30000?ref=homepageMapSearchSR',
            headers=self.headers,
            #cookies=cookies,
            callback=self.parse
        )
    
    # parse response
    def parse(self, response):
        print('\n\nResponse:', response.text)
        print('\n\nStatus:', response.status)

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Scraper)
    process.start()














