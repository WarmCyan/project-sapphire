#***************************************************************************
#
#  File: reuters_v1.py (sapphire.scrapers)
#  Date created: 05/17/2018
#  Date edited: 05/24/2018
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

    SOURCE = "reuters"
    TYPE = "rss"
    VERSION = "v1"

    subfeeds = {
        "business": "http://feeds.reuters.com/reuters/businessNews",
        "companynews": "http://feeds.reuters.com/reuters/companyNews",
        "entertainment": "http://feeds.reuters.com/reuters/entertainment",
        "environment": "http://feeds.reuters.com/reuters/environment",
        "healthnews": "http://feeds.reuters.com/reuters/healthNews",
        "mostread": "http://feeds.reuters.com/reuters/MostRead",
        "people": "http://feeds.reuters.com/reuters/peopleNews",
        "politics": "http://feeds.reuters.com/Reuters/PoliticsNews",
        "science": "http://feeds.reuters.com/reuters/scienceNews",
        "technology": "http://feeds.reuters.com/reuters/technologyNews",
        "topnews": "http://feeds.reuters.com/reuters/topNews",
        "usnews": "http://feeds.reuters.com/Reuters/domesticNews",
        "worldnews": "http://feeds.reuters.com/Reuters/worldNews"
    }

    def __init__(self):
        self.url = "" 
        self.feed = ""
        self.page = None # NOTE: the raw html from the scrape
        self.scrape_time = None
        self.articles = []
        
    def run(self, subfeed):
        self.subfeed = subfeed
        self.url = self.subfeeds[subfeed]
        
        self.scrape()
        self.extract()
        return self.articles

    def getSubfeeds(self): return self.subfeeds
    def getIdentifier(self): return self.SOURCE + "_" + self.TYPE + "_" + self.VERSION



    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.getIdentifier())

    # NOTE: returns the html
    def scrape(self):
        # scrape the RSS from the url
        self.log("Scraping '" + self.url + "' feed...")
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        page = response.read().decode('utf-8')
        self.page = page

        # get time of the scrape
        scrape_time_dt = datetime.datetime.now()
        scrape_time = sapphire.utility.getTimestamp(scrape_time_dt)
        self.scrape_time = scrape_time
        self.log("Feed scraping complete")
        
        # store the scrape
        filename = sapphire.utility.getFileTimeStamp(scrape_time_dt) + "_" + self.getIdentifier() + "_" + self.subfeed + ".xml"
        self.log("Storing raw scrape in '" + filename + "'...")
        with open(sapphire.utility.feed_scrape_raw_dir + "/" + filename, 'w') as f:
            f.write(page)
        self.log("File saved")
        
    def extract(self):
        self.log("Parsing scrape for items...")
        soup = BeautifulSoup(self.page, "xml") # NOTE: uses lxml-xml (is this available in apt repos for a pi?)
                
        items = soup.find_all('item')
        articles = []
        for item in items:
            self.log("Found item '" + item.title.text + "'", 'DEBUG')
            timestamp = datetime.datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z")
            
            article = Article()
            article.title = item.title.text
            article.description = item.description.text
            article.timestamp = sapphire.utility.getTimestamp(timestamp)
            article.link = item.link.text
            article.source_name = "Reuters"
            article.source_type = "RSS"
            article.source_sub = "World News"
            article.source_explicit = self.url
            article.meta_scrape_time

            articles.append(article)

        self.log("Finished parsing scrape")
        self.articles = articles

