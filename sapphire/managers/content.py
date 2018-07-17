#***************************************************************************
#
#  File: content.py (sapphire.managers)
#  Date created: 06/16/2018
#  Date edited: 07/17/2018
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
import sapphire.utility.stats

from sapphire.scrapers import reuters_v1


class ContentManager:

    IDENTIFIER = "Content Manager"

    reuters_ver = "v1"

    sources_list = {"Reuters": None} # TODO: fix capitalization somemhow

    def __init__(self):
        self.log("Initializing content manager...")
        self.sources_list["Reuters"] = reuters_v1.ContentScraper()
        self.log("Initialized")


    def scrape(self, article):
        self.log("Initiating scrape for source '" + article.source_name + "' - " + article.UUID)
        scraper = self.sources_list[article.source_name]
        content, scrape_time = scraper.run(article.link, article.UUID)
        self.log("Populating article data...")
        article.populateContent(content, scrape_time, scraper.getIdentifier())
        
        self.storeLocal(article)
        self.storeDB(article)


    def storeLocal(self, article):
        #basefilename = sapphire.utility.content_store_dir + sapphire.utility.getFileTimeStamp(sapphire.utility.getDT(article.content_scrape_time)) + "_" + article.content_scrape_identifier + "_" + article.UUID
        basefilename = sapphire.utility.content_store_dir + article.UUID + "_" + article.content_scrape_identifier
        
        self.log("Saving scraped content in '" + basefilename + "'...")
        with open(basefilename, 'w') as outfile:
            outfile.write(article.content)
            
        self.log("Local content stored")
        humansize, count, size = sapphire.utility.stats.updateFileStats("content_scrape_raw_dir", sapphire.utility.content_scrape_raw_dir)
        humansize2, count2, size2 = sapphire.utility.stats.updateFileStats("content_store_dir", sapphire.utility.content_store_dir)
        sapphire.utility.stats.updateTotalFileStats()
        
        self.log("Raw content scrape folder contains " + str(count) + " files and takes up " + humansize)
        self.log("Content store folder contains " + str(count2) + " files and takes up " + humansize2)

    def storeDB(self, article):
        self.log("Updating database with article content...")
        db = sapphire.managers.database.DatabaseManager()
        db.updateArticle(article)
        
    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)
