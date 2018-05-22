#***************************************************************************
#
#  File: reuters.py (sapphire.scrapers)
#  Date created: 05/17/2018
#  Date edited: 05/22/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Classes to handle scraping reuters RSS feeds and articles
#
#***************************************************************************

from bs4 import BeautifulSoup
import urllib.request

import datetime

import sapphire.utility
from sapphire.article import Article


class RSSScraper:

    def __init__(self):
        self.url = "http://feeds.reuters.com/Reuters/worldNews" # TODO: temp

    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source="Scraper::Reuters")

    # NOTE: returns the html
    def scrape(self):
        # scrape the RSS from the url
        self.log("Scraping '" + self.url + "' feed...")
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        page = response.read().decode('utf-8')

        scrape_time_dt = datetime.datetime.now()
        scrape_time = sapphire.utility.getTimestamp(scrape_time_dt)
        self.log("Feed scraping complete")
        
        # store the scrape
        filename = sapphire.utility.getFileTimeStamp(scrape_time_dt) + "_reuters_testscrape.xml" # TODO: or reverse order?
        self.log("Storing raw scrape in '" + filename + "'...")
        with open(sapphire.utility.feed_scrape_raw_dir + "/" + filename, 'w') as f:
            f.write(page)
        self.log("File saved")

        return page, scrape_time
        
    def extract(self, page, scrape_time):
        self.log("Parsing scrape for items...")
        soup = BeautifulSoup(page, "xml") # NOTE: uses lxml-xml (is this available in apt repos for a pi?)
                
        items = soup.find_all('item')
        articles = []
        for item in items:
            self.log("Found item '" + item.title.text + "'", 'DEBUG')
            timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")
            
            article = Article()
            article.title = item.title.text
            article.description = item.description.text
            article.timestamp = sapphire.utility.getTimestamp(timestamp)
            article.link = item.origLink.text
            article.source_name = "Reuters"
            article.source_type = "RSS"
            article.source_sub = "World News"
            article.source_explicit = self.url
            article.meta_scrape_time

            articles.append(article)

        self.log("Finished parsing scrape")
        return articles
            

        
        '''
        article_items = []
        for item in items:
            timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")

            # TODO: make this a class?
            article = { 
                    "title": item.title.text,
                    "description": item.description.text,
                    #"timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": sapphire.utility.getTimestamp(timestamp),
                    "link": item.origLink.text,


                    "source": "reuters",
                    "source_type": "rss",
                    "source_sub": "WorldNews",
                    "source_explicit": url,
                    "scraped": scrape_time,

                    "other": { "category": item.category.text }
                    }

            article_heads.append(article)

    
        pass
        '''

    # TODO: returns JSON
    # NOTE: make this "run" instead, and have scrape versus extract/parse separate functions?
    def run(self):

        page, time = self.scrape()
        articles = self.extract(page, time)




        '''

        #print(sapphire.utility.feed_scrape_raw_tmp_dir) # TODO: debug

        url = "http://feeds.reuters.com/Reuters/worldNews" # TODO: temp

        # scrape the RSS from the url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        page = response.read().decode('utf-8')

        scrape_time_dt = datetime.datetime.now()
        scrape_time = sapphire.utility.getTimestamp(scrape_time_dt)

        # store the scrape
        filename = sapphire.utility.getFileTimeStamp(scrape_time_dt) + "_reuters_testscrape.xml" # TODO: or reverse order?
        with open(sapphire.utility.feed_scrape_raw_tmp_dir + "/" + filename, 'w') as f:
            f.write(page)
        
        # parse the scrape
        soup = BeautifulSoup(page, "xml") # NOTE: using lxml-xml (is this available in apt repos for a pi?)

        items = soup.find_all('item')
        
        article_heads = []
        for item in items:
            timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")

            # TODO: make this a class?
            article = { 
                    "title": item.title.text,
                    "description": item.description.text,
                    #"timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": sapphire.utility.getTimestamp(timestamp),
                    "link": item.origLink.text,


                    "source": "reuters",
                    "source_type": "rss",
                    "source_sub": "WorldNews",
                    "source_explicit": url,
                    "scraped": scrape_time,

                    "other": { "category": item.category.text }
                    }

            article_heads.append(article)

        '''


