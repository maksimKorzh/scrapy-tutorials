###########################################
#
#    Script to scrape product details
#  from whatever category on hummart.com
#
#                   by
#
#            Code Monkey King
#
###########################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# hummart spider class
class HummartScraper(scrapy.Spider):
    # scraper / spider name
    name = 'hummart_scraper'
    
    # base URL (paste whatever hummart category URL below
    # it would then crawl through ALL the pages (infinite scroll) available
    # e.g. try this one 'https://hummart.com/noodles-sauces-instant-food' instead)
    base_url = 'https://hummart.com/baking-ingredients' 
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'hummart.csv',
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        #'DOWNLOAD_DELAY': 1
    }
    
    # current page counter
    current_page = 1
    
    # crawler's entry point
    def start_requests(self):
        # make HTTP request to base URL
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_links
        )

    # parse product links
    def parse_links(self, response):
        # loop over product cards
        for card in response.css('li[class="item product product-item"]'):
            # extract product URL
            product_url = card.css('a::attr(href)').get()

            # make HTTP request to product link URL
            yield response.follow(
                url=product_url,
                headers=self.headers,
                callback=self.parse_product
            )
        
        # try to crawl next pages (infinite scroll)
        try:
            # increment current page counter
            self.current_page += 1
            
            try:
                total_pages = max(list(filter(None, [
                    text.get().replace('\n', '').strip()
                    for text in response.css('ul[class="items pages-items"]').css('li *::text')
                    if text.get().replace('\n', '').strip().isdigit()
                ])))
            
            except:
                total_pages = 1
            
            # generate next page URL
            next_page = self.base_url + '?p=' + str(self.current_page)
            
            if self.current_page <= int(total_pages):
                # print debug info
                print('Crawling page %s' % self.current_page)
                
                # crawl next page
                yield response.follow(
                    url=next_page,
                    headers=self.headers,
                    callback=self.parse_links
                )
        
        except Exception as e:
            print('\n\nERROR during crawling next page:', e)
    
    # parse product details
    def parse_product(self, response):
        '''
        # store response HTML locally
        with open('product.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # open local HTML file
        with open('product.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''
        
        # extract product details
        features = {
            'Product name': response.css('span[itemprop="name"]::text')
                            .get(),

            'Category': '',
            
            'Option': response.css('td[data-th="Option"]::text')
                              .get(),
            
            'Brand': response.css('td[data-th="Brand"]::text')
                              .get(),
            
            'Sold by': response.css('td[data-th="Sold By"]::text')
                              .get(),
            
            'Country of Manufacture': response.css('td[data-th="Country of Manufacture"]::text')
                              .get(),
            
            'Express Shipping': response.css('td[data-th="Express Shipping"]::text')
                              .get(),
            
            'Return Policy': response.css('td[data-th="Return Policy"]::text')
                              .get(),
                              
            'Warranty': response.css('td[data-th="Warranty"]::text')
                              .get(),
          
            'Image URL': '',
            
            'Price': response.css('span[class="price"]::text')
                             .get(),
            
            'Special price': '',

            'Discount': '',
            
            'Quantity': '',

            'Description': ''.join(list(filter(None, [
                                       text.get().replace('\n', '').replace('\r', '').strip()
                                       for text in
                                       response.css('div[class="product attribute description"] *::text')
                                   ]))).replace('\n', '')
                                     .strip(),
            
            'Availability': '',
            
            'Product link': response.url
        }

        try:
            # extract additional info
            json_data = json.loads([
                script.get()
                for script in
                response.css('script::text')
                if 'Magento_GoogleTagManager/js/actions/product-detail' in script.get()
            ][0])
            
            # filter JSON data
            json_data = json_data['*']['Magento_GoogleTagManager/js/actions/product-detail']
            
            # append exact price
            features['Price'] += ' | Exact price: ' + json_data['Price'] + ' ' + json_data['Currency']
            
            # append special price
            features['Special price'] = json_data['SpecialPrice']
            
            # append image URL
            features['Image URL'] = json_data['ImagePath']
            
            # append availability
            features['Availability'] = json_data['avaibilty']
            
            # append discount
            features['Discount'] = json_data['Discount']
            
            # append quantity
            features['Quantity'] = json_data['Quantity']
            
            # append category name
            features['Category'] = json_data['CategoryName']
        
        except Exception as e:
            print('Additional date is not available!')

        # write features to CSV file
        yield features
        
        # print extracted data
        #print(json.dumps(features, indent=2))

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(HummartScraper)
    process.start()
    
    # debug data extraction logic
    #HummartScraper.parse_product(HummartScraper, '')




















