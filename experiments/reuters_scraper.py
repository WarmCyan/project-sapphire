from bs4 import BeautifulSoup
import urllib.request

import datetime
from pytz import timezone


# scraping part
url = "http://feeds.reuters.com/Reuters/worldNews"

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
page = response.read().decode('utf-8')

scrape_time = datetime.datetime.now()
scrape_time.astimezone(timezone('UTC'))
scrape_time = scrape_time.strftime("%Y-%m-%d %H:%M:%S")

# cleaning/extraction part
soup = BeautifulSoup(page, "xml") # NOTE: this is using lxml-xml

items = soup.find_all('item')

article_heads = []
for item in items:
    # format directives from https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")
    timestamp.astimezone(timezone('UTC'))
    
    article = { 
            "title": item.title.text,
            "description": item.description.text,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "link": item.origLink.text,

            
            "source": "reuters",
            "source_type": "rss",
            "source_sub": "WorldNews",
            "source_explicit": url,
            "scraped": scrape_time,
            
            "other": { "category": item.category.text }
            }

    article_heads.append(article)
