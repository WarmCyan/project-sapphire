from bs4 import BeautifulSoup
import urllib.request

import datetime
from pytz import timezone

import re


# scraping part
url = "https://www.reuters.com/article/us-australia-security-elections/australia-forms-task-force-to-guard-elections-from-cyber-attacks-idUSKCN1J506D?feedType=RSS&feedName=technologyNews&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+reuters%2FtechnologyNews+%28Reuters+Technology+News%29"

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
page = response.read().decode('utf-8')

scrape_time = datetime.datetime.now()
scrape_time.astimezone(timezone('UTC'))
scrape_time = scrape_time.strftime("%Y-%m-%d %H:%M:%S")

# cleaning/extraction part
soup = BeautifulSoup(page, "lxml")

#items = soup.find_all('item')


#print(page)
content_container = soup.find_all(attrs={"class":re.compile("container\w*\ content")}, limit=1)[0]

body = content_container.find_all(attrs={"class":re.compile("body")}, limit=1)[0]

paragraphs = body.find_all('p')[:-1] # don't include last, it's just reporting
for p in paragraphs:
    print(p.text)
    #print(p)
    print('\n')
