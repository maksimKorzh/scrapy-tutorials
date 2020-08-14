#
#  POST request to feedo API by Code MOnkey King
#

# packages
import scrapy
from scrapy.crawler import CrawlerProcess

# feedo scraper
class Feedo(scrapy.Spider):
    # scraper name
    name = 'feedo'
    
    # base URL
    base_url = 'https://www.feedo.net/FeedoDisplayPages/CMSDisplayPages/ListallDocsNoTab_a.aspx'
    
    # custom headers
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "1090",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "_ga=GA1.2.383860836.1597127059; __gads=ID=cd5020188a9bc86c:T=1597127060:S=ALNI_MZQOUlpT_pHJIR4I82TjR5qVfo8Ug; _gid=GA1.2.914219102.1597399684; ASP.NET_SessionId=1e1vatnizhjgsvmrqghjcz2s; ASPSESSIONIDAUSRSRAR=KONLNOBDOIDJJCCFCGPBBIAJ",
        "Host": "www.feedo.net",
        "Origin": "//www.feedo.net",
        "Pragma": "no-cache",
        "Referer": "//www.feedo.net/FeedoDisplayPages/CMSDisplayPages/ListallDocsNoTab_a.aspx",
        "Sec-Fetch-Mode": "nested-navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    
    # POST request form data
    form_data = '__EVENTTARGET=btnLast&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTY2MjM3NDc3MQ9kFgICAQ9kFhACAQ8PFgIeBFRleHQFJ9mE2K3ZhSDYqNmC2LHZiSZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwO2RkAgMPFgIfAAWWAjxJZnJhbWUgb25sb2FkPSdqYXZhc2NyaXB0OnJlc2l6ZUlmcmFtZSh0aGlzKTsnIG9ucmVzaXplPSdqYXZhc2NyaXB0OnJlc2l6ZUlmcmFtZSh0aGlzKTsnIGRpcj0icnRsIiBuYW1lPSJEZXRhaWxlZCIgU3JjPUxpc3QzRGV0YWlsZWRBbGxDYXREb2NzX2EuYXNweD9DYXRlZ29yeUlEPTIzNiBmcmFtZUJvcmRlcj0iMCIgc2Nyb2xsaW5nPSJubyIgYWxsb3d0cmFuc3BhcmVuY3kgY2xhc3M9IkNlbnRlcklGcmFtZSIgbWFyZ2lud2lkdGg9IjAiIG1hcmdpbmhlaWdodD0iMCI%2BPC9JZnJhbWU%2BZAIHDw8WAh8ABRMg2LXZgdit2KkgIDEg2YXZhiA0ZGQCCQ8PFgQeD0hvcml6b250YWxBbGlnbgsqKVN5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuSG9yaXpvbnRhbEFsaWduAx4EXyFTQgKAgEBkZAILDw8WBh8ABQrYp9mE2KPZiNmEHgdFbmFibGVkaB4HVmlzaWJsZWhkZAINDw8WBh8ABQ7Yp9mE2LPZgNin2KjZgh8DaB8EaGRkAg8PDxYCHwAFDSDYp9mE2KrYp9mE2YlkZAIRDw8WAh8ABQzYp9mE2KPYrtmK2LFkZGRzggjfjGsHkD0DfqH18by0CveozJAFwXNN1JF76uLK0Q%3D%3D&__VIEWSTATEGENERATOR=2EAB73D3&__EVENTVALIDATION=%2FwEdAANl11PyWvGae9xDUoUcWbi6gWOkgugWB5Cq9dYD7toQNAN7CikXyVjnpcpNSgYVrOuA6l9LRvhQRJpUtulUezviXQ%2B9Nin0qH9fua1Cfz%2BB%2Bw%3D%3D'
    
    # custom scraper settings
    custom_settings = {
        # pass cookies along with headers
        'COOKIES_ENABLED': False
    }
    
    # crawler's entry point
    def start_requests(self):
        # make HTTP POST request to feedo API
        yield scrapy.Request(
            url=self.base_url,
            method='POST',
            headers=self.headers,
            body=self.form_data,
            callback=self.parse
        )
    
    # parse callback method
    def parse(self, response):
        print(response.text)
    
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Feedo)
    process.start()














