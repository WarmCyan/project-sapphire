#***************************************************************************
#
#  File: article.py (sapphire.managers)
#  Date created: 06/20/2018
#  Date edited: 07/04/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Ties all of the other managers together (primary point of contact
#    of the package for the backend scraper portion)
#
#***************************************************************************

import time

import sapphire.utility
import sapphire.utility.logging
import sapphire.utility.scheduler

from sapphire.managers.rss import RSSManager
from sapphire.managers.content import ContentManager
from sapphire.managers.metadata import MetadataManager
from sapphire.managers.database import DatabaseManager

class ArticleManager:

    IDENTIFIER = "Article Manager"


    # NOTE: config is the path + filename of json config file
    def __init__(self, config=None):
        if config is not None: self.configure(config)
        
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

    # NOTE: this returns any new commands 
    def handleCommand(self, cmd, poll=False):
        parts = cmd.split(' ')
        
        if parts[0] == "scrape":
            if parts[1] == "feed":
                self.scrapeFeeds()

                # get the next scrape time
                if "all" in sapphire.utility.feed_rates:
                    now = datetime.datetime.now()
                    then = now + datetime.timedelta(0,sapphire.utility.feed_rates["all"])
                    return [str(int(then.timestamp())) + " scrape feed", str(int(then.timestamp())) + " queue"]
                else:
                    self.log("Polling unavailable, no rates listed in config ('feed_rates')", "ERROR")
            elif parts[1] == "article":
                self.scrapeNextArticle()
        elif parts[0] == "queue":
            self.consumeQueue()

    def initiateSchedule(self, name):
        self.log("Creating initial feed scraping schedule")
        schedule = [str(int(now.timestamp())) + " scrape feed", str(int(now.timestamp())) + " queue"]
        sapphire.utility.writeSchedule(name, schedule)
        
    # NOTE: rate is in seconds
    def pollSchedule(self, name, rate):
        polling = True

        while polling:
            pollTime = sapphire.utility.getTimestamp(datetime.datetime.now())
            print("Last polled at " + polltime + "\r", end='')
            
            schedule = sapphire.utility.scheduler.getSchedule(name)
            runnableSchedule, remaining = sapphire.utility.scheduler.findRunnable(schedule)
            for item in runnableSchedule:
                if item[0] != 0:
                    readableTime = sapphire.utility.getTimestamp(datetime.datetime.fromtimestamp(int(item[0])))
                    self.log("Running '" + item[1] + " scheduled for " + readableTime + "...")
                    newItems = handleCommand()

                    remaining.extend(newItems)
                    sapphire.utility.writeSchedule(name, remaining)
            
            time.sleep(rate)
