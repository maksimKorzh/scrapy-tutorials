##########################################
#
# Script to scrape Questions and Answers 
#     from https://answers.yahoo.com
#
#                   by
#
#            Code Monkey King
#
##########################################

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# q/a spider class
class YahooAnswers(scrapy.Spider):
    # scraper /spider name
    name = 'answers'
    
    # API URL
    api_url = 'https://answers.yahoo.com/_reservice_/'
    
    # API headers
    api_headers = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # HTTP PUT request payload
    payload = {
        "type": "CALL_RESERVICE",
        "payload": {
            # change the category ID to retrieve proper questions
            # e.g. you have URL: https://answers.yahoo.com/dir/index/discover?sid=396545443
            # so you need to look at "?sid=396545443" string query parameter
            # and extract the number 396545443 to use it as the "categoryId" below
            "categoryId": "396545443",
            "lang": "en-US",
            "count": 20,
            "offset": "pc00~p:0"
        },
        "reservice": {
            "name":"FETCH_DISCOVER_STREAMS_END",
            "start":"FETCH_DISCOVER_STREAMS_START",
            "state":"CREATED"
        }
    }
    
    # data offset
    data_offset = 0
    
    # crawler'a entry point
    def start_requests(self):
        # make HTTP PUT request to API URL
        yield scrapy.Request(
            url=self.api_url,
            method='PUT',
            headers=self.api_headers,
            body=json.dumps(self.payload),
            callback=self.parse_questions
        )
    
    # parse questions callback method
    def parse_questions(self, response):
        # parse response
        json_data = json.loads(response.text)
        
        # loop over available questions
        for item in json_data['payload']['questions']:
            # generate answer link
            answer_url = 'https://answers.yahoo.com/question/index?qid=' + item['qid']
            
            # make HTTP request to answer URL
            yield response.follow(
                url=answer_url,
                headers=self.headers,
                callback=self.parse_answer
            )
        
        # check if next bunch of data available
        if json_data['payload']['canLoadMore'] == True:
            # update data offset
            self.data_offset += 20
            
            # update payload offset
            self.payload['payload']['offset'] = 'pc' + str(self.data_offset) + '~p:0'
            
            # crawl next bunch of data
            yield scrapy.Request(
                url=self.api_url,
                method='PUT',
                headers=self.api_headers,
                body=json.dumps(self.payload),
                callback=self.parse_questions
            )
    
    # parse answers callback method
    def parse_answer(self, response):
        '''
        # store HTML content to local file
        with open('answer.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # open local HTML file
        with open('answer.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''
        
        # data extraction logic
        features = {
            'question': response.css('h1[class="Question__title___3_bQf"]::text')
                                .get(),
            
            'details': response.css('div[class="ExpandableContent__content___NoJJI"]')
                               .css('p::text')
                               .get(),
            
            'date': response.css('span[class="QAContent__updatedDetailTitle___1RvMm"]::text')
                            .get(),
            
            'answers': []
        }
        
        # extract answers
        for answer in response.css('ul[class="AnswersList__answersList___1GjcP"]').css('li'):
            # extract user name
            user_name = answer.css('div[class="UserProfile__userInfo___yViBh"] *::text').get()
            
            # append only available answers
            if user_name is not None:
                features['answers'].append({
                    'user_name': user_name,
                    
                    'answer': answer.css('div[class="ExpandableContent__content___NoJJI"] *::text')
                                      .get(),
                    
                    'comments': answer.css('p[class="Comment__text___3G8FQ"]::text')
                                      .getall(),
                    
                    'date': answer.css('div[class="Answer__subtitle___yrInO"]::text')
                                  .get(),
                    
                    'likes': answer.css('button[aria-label="Thumbs up for this answer."]')
                                   .css('span::text')
                                   .get(),
                    
                    'dislikes': answer.css('button[aria-label="Thumbs down for this answer."]')
                                   .css('span::text')
                                   .get()
                    
                })
        
        # write features to output JSONL file
        with open('answers.jsonl', 'a') as f:
            f.write(json.dumps(features, indent=2) + '\n')
    
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(YahooAnswers)
    process.start()
    
    # debug data extraction logic
    #YahooAnswers.parse_answer(YahooAnswers, '')

































