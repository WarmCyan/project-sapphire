#***************************************************************************
#
#  File: rss.py (sapphire.managers)
#  Date created: 05/24/2018
#  Date edited: 05/25/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: Handles running all of the various rss scrapers
#
#***************************************************************************

import time
import json
import os
import datetime

import sapphire.utility

from sapphire.scrapers import reuters_v1


class RSSManager:

    IDENTIFIER = "RSS Manager"

    reuters_ver = "v1"

    sources_list = {"reuters": None} # should be filled with the requiste RSS Scraper class

    def __init__(self):
        self.sources_list["reuters"] = reuters_v1.RSSScraper()

    # NOTE: scrapes ALL subfeeds
    def scrapeSource(self, source):
        self.log("Initiating scraper for source '" + source + "'...")
        
        scraper = self.sources_list[source]
        subfeeds = scraper.getSubfeeds()
        self.log("Scraper identifier: '" + scraper.getIdentifier() + "'")
        
        articles = []
        
        
        for subfeed in subfeeds:
            articles.extend(self.scrapeSourceSubfeed(source, subfeed))
            time.sleep(1)

        self.log("All " + source + " RSS subfeeds scraped")

        return articles

    def scrapeSourceSubfeed(self, source, subfeed):
        self.log("Running " + source + " scraper on subfeed '" + subfeed + "'...")

        scraper = self.sources_list[source]
        articles = scraper.run(subfeed)
        return articles

    def saveMetadata(self, articles):
        self.log("Preparing to save scrape metadata...")
        
        # put articles into dictionary so can be saved as json
        articleMetadata = []
        timestamp = datetime.datetime.now()

        for article in articles:
            articleMetadata.append(article.getMetadataDictionary())

        self.storeBackupMetadata(articleMetadata, timestamp)
        self.enqueueMetadata(articleMetadata, timestamp)
        self.log("All scrape metadata saved")
        

    # NOTE: auto increments a number at the end until finds filename that doesn't already exist
    def getMetadataFilename(self, filename):
        number = 0
        newfilename = filename + "_" + str(number)
        while os.path.isfile(newfilename):
            number += 1
            newfilename = filename + "_" + str(number)
        return newfilename           

    # NOTE: timestamp is a dt object
    # NOTE: articles should ALREADY BE DICTIONARY
    def storeBackupMetadata(self, articleMetadata, timestamp):
        # get filename
        basefilename = sapphire.utility.feed_scrape_tmp_dir + sapphire.utility.getFileTimeStamp(timestamp)
        filename = self.getMetadataFilename(basefilename)
        
        # write the data
        self.log("Saving scraped item metadata to a backup file '" + filename + "'...")
        with open(filename, 'w') as outfile:
            json.dump(articleMetadata, outfile)
        self.log("File saved")

    # NOTE: timestamp is a dt object
    # NOTE: articles should ALREADY BE DICTIONARY
    def enqueueMetadata(self, articleMetadata, timestamp):
        basefilename = sapphire.utility.metadata_queue_dir + sapphire.utility.getFileTimeStamp(timestamp)
        filename = self.getMetadataFilename(basefilename)
        
        # write the data
        self.log("Adding scraped item metadata to queue location, '" + filename + "'...")
        with open(filename, 'w') as outfile:
            json.dump(articleMetadata, outfile)
        self.log("File saved")


    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
        
        
