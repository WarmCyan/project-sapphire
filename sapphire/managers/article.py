#***************************************************************************
#
#  File: article.py (sapphire.managers)
#  Date created: 06/20/2018
#  Date edited: 06/20/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Ties all of the other managers together (primary point of contact
#    of the package for the backend scraper portion)
#
#***************************************************************************

import sapphire.utility
import sapphire.utility.logging

from sapphire.managers.rss import RSSManager
from sapphire.managers.content import ContentManager
from sapphire.managers.metadata import MetadataManager
from sapphire.managers.database import DatabaseManager

class ArticleManager:

    IDENTIFIER = "Article Manager"

    VERSION = "0.1.0"
    VERSION_DATE = "06/20/2018"
    COPYRIGHT = "Copyright © 2018 Digital Warrior Labs"

    # NOTE: config is the path + filename of json config file
    def __init__(self, config=None):
        if config is not None: self.configure(config)
        
        self.log("Initializing article manager...")
        self.log("===========================================")
        self.log("  Version: " + self.VERSION)
        self.log("  Date: " + self.VERSION_DATE)
        self.log("  " + self.COPYRIGHT)
        self.log("===========================================")
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
        articles = self.rss_man.scrapeSource('reuters')
        self.rss_man.saveMetadata(articles)
        self.log("Feed scrape complete")

    def consumeQueue(self):
        self.log("Consuming metadata queue...")
        self.meta_man.consumeQueue()
        self.log("Queue consumption complete")

    def scrapeNextArticle(self):
        self.log("Scraping next article...")
        db = DatabaseManager()
        article = db.getFirstLackingArticle()
        self.content_man.scrape(article)
        self.log("Article scrape complete")
