#***************************************************************************
#
#  File: article.py (sapphire.managers)
#  Date created: 06/20/2018
#  Date edited: 07/20/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Ties all of the other managers together (primary point of contact
#    of the package for the backend scraper portion)
#
#***************************************************************************

import time
import datetime

import sapphire.utility
import sapphire.utility.logging
import sapphire.utility.scheduler
import sapphire.utility.stats

from sapphire.managers.rss import RSSManager
from sapphire.managers.content import ContentManager
from sapphire.managers.metadata import MetadataManager
from sapphire.managers.database import DatabaseManager

class ArticleManager:

    IDENTIFIER = "Article Manager"


    # NOTE: config is the path + filename of json config file
    def __init__(self, name=None, config=None):
        if config is not None: self.configure(config)
        self.name = name
        
        self.log("Initializing article manager...")
        self.rss_man = RSSManager()
        self.content_man = ContentManager()
        self.meta_man = MetadataManager()
        self.log("Initialized")

    def configure(self, config):
        sapphire.utility.readConfig(config)

    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)

    def scrapeFeeds(self):
        self.log("Scraping all feeds...")
        sapphire.utility.stats.updateStatus(self.name, "Scraping feed...")
        sapphire.utility.stats.updateLastTime("scrape_feed")
        articles = self.rss_man.scrapeSource('reuters')
        self.rss_man.saveMetadata(articles)
        sapphire.utility.stats.updateStatus(self.name, "Idle")
        self.log("Feed scrape complete")

    def consumeQueue(self):
        self.log("Consuming metadata queue...")
        sapphire.utility.stats.updateStatus(self.name, "Handling queue...")
        sapphire.utility.stats.updateLastTime("queue")
        self.meta_man.consumeQueue()
        sapphire.utility.stats.updateStatus(self.name, "Idle")
        self.log("Queue consumption complete")

    def scrapeNextArticle(self):
        self.log("Scraping next article...")
        sapphire.utility.stats.updateStatus(self.name, "Scraping content...")
        sapphire.utility.stats.updateLastTime("scrape_content")
        db = DatabaseManager()
        article = db.getFirstLackingArticle()
        self.content_man.scrape(article)
        sapphire.utility.stats.updateStatus(self.name, "Idle")
        self.log("Article scrape complete")

    def testScrapeNextArticle(self):
        self.log("Testing content scraper on next article...")
        db = DatabaseManager()
        article = db.getFirstLackingArticle()
        self.content_man.testScraper(article)
