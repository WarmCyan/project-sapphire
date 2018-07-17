#***************************************************************************
#
#  File: article.py (sapphire.managers)
#  Date created: 06/20/2018
#  Date edited: 07/16/2018
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

    # NOTE: this returns any new commands 
    # rate is the polling rate
    def handleCommand(self, cmd, poll=False, rate=0):
        parts = cmd.split(' ')
        
        if parts[0] == "scrape":
            if parts[1] == "feed":
                self.scrapeFeeds()

                nextCommands = []

                # get the next scrape time
                if "all" in sapphire.utility.feed_rates:
                    now = datetime.datetime.now()

                    if poll:
                        # determine if this is a specific time
                        if "times" in sapphire.utility.feed_rates["all"]:
                            nexttime = 0

                            # loop through each time, if the current time is greater than it, and the last poll was less than it, it was that specified time (or a freaky coincidence)
                            for time in sapphire.utility.feed_rates["all"]["times"]:
                                timeDT = sapphire.utility.getDTFromMilitary(str(time))
                                prevPollDT = now - datetime.timedelta(seconds=rate)
                                if now.timestamp() > timeDT.timestamp() and prevPollDT.timestamp() < timeDT.timestamp():
                                    #nextCommands.append(str(int(I
                                    nexttime = timeDT.timestamp()
                                    return [str(int(nexttime)) + " scrape feed", str(int(nexttime)) + " queue"]
                                    
                                    

                    
                    # old rate method (rather than time based)
                    #then = now + datetime.timedelta(0,sapphire.utility.feed_rates["all"])
                    #return [str(int(then.timestamp())) + " scrape feed", str(int(then.timestamp())) + " queue"]
                else:
                    self.log("Polling unavailable, no rates listed in config ('feed_rates')", "ERROR")
            elif parts[1] == "article":
                self.scrapeNextArticle()

                if sapphire.utility.content_rate is not None:
                    now = datetime.datetime.now()
                    then = now + datetime.timedelta(0,sapphire.utility.content_rate)
                    return [str(int(then.timestamp())) + " scrape article"]
                
        elif parts[0] == "queue":
            self.consumeQueue()

    def initiateSchedule(self, name):
        now = datetime.datetime.now()
        # TODO: note that this is only temporary
        if name == "feed":
            #self.log("Creating initial feed scraping schedule")
            #schedule = [str(int(now.timestamp())) + " scrape feed", str(int(now.timestamp())) + " queue"]
            #sapphire.utility.scheduler.writeSchedule(name, schedule)
            
            # find the first instances
            schedule = []
            for time in sapphire.utility.feed_rates["all"]["times"]:
                timedt = sapphire.utility.getDTFromMilitary(str(time))
                schedule.extend([str(int(timedt.timestamp())) + " scrape feed", str(int(timedt.timestamp())) + " queue"])
            sapphire.utility.scheduler.writeSchedule(name, schedule)
        elif name == "content":
            self.log("Creating initial content scraping schedule")
            schedule = [str(int(now.timestamp())) + " scrape article"]
            sapphire.utility.scheduler.writeSchedule(name, schedule)
            
        
    # NOTE: rate is in seconds
    def pollSchedule(self, name, rate):
        polling = True

        while polling:
            pollTime = sapphire.utility.getTimestamp(datetime.datetime.now())
            pollTimeS = str(int(datetime.datetime.now().timestamp()))
            print("Last polled at " + pollTime + " (" + pollTimeS + ")\r", end='')
            if self.name is not None:
                sapphire.utility.stats.updateLastTime(self.name + "_poll")
            
            schedule = sapphire.utility.scheduler.getSchedule(name)
            #print(schedule)
            runnableSchedule, remaining = sapphire.utility.scheduler.findRunnable(schedule)
            #print(runnableSchedule)
            for item in runnableSchedule:
                #print("Running " + str(item))
                if item[0] != 0:
                    readableTime = sapphire.utility.getTimestamp(datetime.datetime.fromtimestamp(int(item[0])))
                    self.log("Running '" + item[1] + "' scheduled for " + readableTime + "...")
                    newItems = self.handleCommand(item[1], True)

                    if newItems is not None: remaining.extend(newItems)
                    sapphire.utility.scheduler.writeSchedule(name, remaining)
                    print("Resuming poll...\r", end='')
            
            time.sleep(rate)
