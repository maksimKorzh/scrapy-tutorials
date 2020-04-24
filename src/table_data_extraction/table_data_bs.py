# packages
import requests
from bs4 import BeautifulSoup
import json

# make HTTP request to the given URL
res = requests.get('https://www.enchantedlearning.com/wordlist/')

# parse response
content = BeautifulSoup(res.text, 'lxml')

# table extraction method 1: indexing (the most dumb way)
tables = content.find_all('table')
table_method1 = tables[4]

# table extraction method 2: specifying table's unique attributes
# and picking up the very first one of the list
table_method2 = content.find('table', {
                                          'border': 1,
                                          'cellpadding': 2,
                                          'cellspacing': 0
                                      })

# table date selector
row = table_method2.find('tr')
cols = row.find_all('td')
links_set = [col.find_all('a') for col in cols]
base_url = 'https://www.enchantedlearning.com'
data = [[{'title': link.text, 'href': base_url + link['href']} for link in links] for links in links_set]

# loop over columns (link sets)
for link_set in data:
    for link in link_set:
        #print(link['title'])
        print(link['href'])
        
        # make recursive HTTP GET request to each URL
        next_url = link['href']
        link_res = requests.get(next_url)
        
        # you can parse recursive response here
        link_content = BeautifulSoup(link_res.text, 'lxml')
        #print(link_res)
        print(link_content)
        
        
        
